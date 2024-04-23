
import pandas as pd
import numpy as np
import os 



# ============================================================
# Constants
# ============================================================
BUILD_PERC_VAL = 0.85
BASEMENT_HEIGHT = 2.4
BASEMENT_PERCENTAGE_OF_PREMISE_AREA = 1
DEFAULT_FLOOR_HEIGHT = 2.3
MAX_THRESHOLD_FLOOR_HEIGHT = 5.3
MIN_THRESH_FL_HEIGHT = 2.2
# ============================================================
# Data Loading Functions
# ============================================================

# current using not age split floor count 
def load_avg_floor_count():
    """Load the average floor count data from a CSV file."""
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'global_avs' , 'global_total_average_fc.csv')
    # csv_path = os.path.join(current_dir, 'global_avs' , 'global_average_fc_byage.csv')
    
    return pd.read_csv(csv_path)

def get_average_heights_table():
    """Load a CSV file containing average heights grouped by criteria."""
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'global_avs' , 'avg_heights_whole_uk.csv')
    df = pd.read_csv(csv_path)
    df = df[df['map_simple_use']=='Residential']
    df['premise_floor_count'] = pd.to_numeric(df['premise_floor_count'])
    return df 


# ============================================================
# Height and Floor Count functions & Pre processing of columns 
# ============================================================
def update_avg_floor_count(df, input_col, avg_table, suffix):
    """Update DataFrame column with average floor count values based on criteria."""
    if (df[input_col] == 0).any():
        raise ValueError('Some floor counts are set to 0, expecting NaN for missing values.')
    # df = pd.merge(df, avg_table, on=['premise_age', 'height_bucket', 'map_simple_use'], how='left')
    df = pd.merge(df, avg_table, on=[ 'height_bucket', 'map_simple_use'], how='left')
    df[f'{input_col}_{suffix}'] = np.where(df[input_col].isna(), df['weighted_average_floor_count'], df[input_col])
    df.drop('weighted_average_floor_count', axis=1, inplace=True)
    return df

def fill_premise_floor_types(df, glob_av_df, fc_col='floor_count_numeric' ):
    """Fill missing premise floor types with global averages."""
    
    df = update_avg_floor_count(df, fc_col, glob_av_df, 'FGA')

    return df



def creat_age_buckets(df):
    df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age'])
    return df 

def create_height_bucket_col(df):
    """Bucket height into predefined categories."""
    df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce').fillna(0) 
    height_bins = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 200]
    height_labels = [f"{b}-{height_bins[i+1]}m" for i, b in enumerate(height_bins[:-1])]
    df['height_bucket'] = pd.cut(df['height_numeric'], bins=height_bins, labels=height_labels, right=False)
    return df


def update_height_with_average(df, input_col, avg_table, suffix):
    """Update the height column with averages based on age, floor count, and use."""
    # Merge with the average table
    df = pd.merge(df, avg_table, left_on = ['premise_age', 'floor_count_numeric', 'map_simple_use'] , right_on=['premise_age', 'premise_floor_count', 'map_simple_use'], how='left')
    # df = pd.merge(df, avg_table, on=['premise_floor_count', 'map_simple_use'], how='left')
    
    # Update heights with averages where applicable
    update_col_name = f'{input_col}_{suffix}'
    df[update_col_name] = np.where(df[input_col] == 0, df['weighted_average_height'], df[input_col])
    
    # Drop the temporary column
    df.drop('weighted_average_height', axis=1, inplace=True)
    return df


def update_height_with_average_flexifc(df, input_col, fc_col, avg_table, suffix):
    """Update the height column with averages based on age, floor count, and use."""
    # Merge with the average table
    
    df = pd.merge(df, avg_table, left_on = ['premise_age', fc_col, 'map_simple_use'], right_on=['premise_age', 'premise_floor_count', 'map_simple_use'], how='left')
    
    # Update heights with averages where applicable
    update_col_name = f'{input_col}_{suffix}'
    df[update_col_name] = np.where(df[input_col] == 0, df['weighted_average_height'], df[input_col])
    
    # Drop the temporary column
    df.drop('weighted_average_height', axis=1, inplace=True)
    return df

def create_height_options(df,  glob_av_df, height_col='height_numeric'):
    """Fill in missing or zero heights with global averages."""
    # Convert 'height' to numeric, filling non-convertible values with 0
    df[height_col] = pd.to_numeric(df['height'], errors='coerce').fillna(0)
    
    # Check for unexpected NaN values after conversion
    if df[height_col].isna().any():
        raise ValueError('Unexpected NaN values found in height_numeric.')
    
    # Update heights using the global averages table
    df = update_height_with_average(df, height_col, glob_av_df, 'FGA')
    return df

def update_listed_type(df):
    df.loc[:, 'listed_bool'] = df['listed_grade'].apply(lambda x: 1 if x is not None else 0)
    return df 

# ============================================================
# Premise Use Fns 
# ============================================================

def one_hot_encode_premise_type(df):
    pre_cols = df.columns.tolist()
    one_hot = pd.get_dummies(df['premise_type'], 'premusetype')
    df = pd.concat([df, one_hot], axis=1)
    post_cols = df.columns.tolist()
    new_cols = [col for col in post_cols if col not in pre_cols]
    return df, new_cols 


# ============================================================
# Scaling functions 
# ============================================================
# from shapely.geometry import Polygon
# from shapely.geometry.polygon import orient



def min_side(polygon):

    # Minimum rotated rectangle
    min_rect = polygon.minimum_rotated_rectangle

    # Extract the points of the rectangle to calculate side lengths
    x, y = min_rect.exterior.coords.xy

    # Calculate distances between consecutive points (sides of the rectangle)
    distances = [np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2) for i in range(1, len(x))]

    # The least width is the minimum side length of the rectangle
    least_width = min(distances)
    return least_width 

def update_height_ratio(highs, glob_av_height, glo_av_flc, height_col = 'height_numeric_FGA' , fc_col = 'floor_count_numeric_FGA'):
    highs['min_side'] = highs['geometry'].apply(min_side)
    highs['threex_minside'] = [x * 3 for x in highs['min_side']]
    highs['validated_height'] = np.where(highs[height_col] >= highs['threex_minside'],   np.nan,  highs[height_col])
    highs['validated_height'] = highs['validated_height'].fillna(0)
    
    highs=update_height_with_average_flexifc(highs, 'validated_height', fc_col , glob_av_height, 'FGA' )
    highs['av_fl_height'] = highs['validated_height_FGA'] / highs['floor_count_numeric']

    highs['validated_fc'] = np.where(((highs['av_fl_height']>= MAX_THRESHOLD_FLOOR_HEIGHT )| (highs['av_fl_height'] <= MIN_THRESH_FL_HEIGHT )) & (highs['height']< highs['threex_minside']) , np.nan, highs[fc_col])
    
    highs = update_avg_floor_count(highs, 'validated_fc', glo_av_flc, 'FGA' ) 
    
    # highs['corr_fl_height'] = highs['validated_height_glob_fill'] / highs['validated_fc_glob_fill']
    return highs 

def update_outbuildings(test):
    test.loc[(test['height']==3) & (test['premise_floor_count'] == '2') & (test['uprn_count'] == 0), 'premise_type'] = 'Domestic outbuilding'
    # test = create_height_bucket_col(test)
    return test

# ============================================================
# Utility Functions
# ============================================================
# def handle_comma_separated_values(val):
#     """Handle comma-separated floor count values."""
#     acceptable_combinations = ['1,2', '2,3', '3,4', '1,3', '4,5', '3,5', '5,6', '4,6', '5,7', '6,7', '6,8', '7,8', '8,9', '9,10', '8,10', '7,9']
#     if val =='' or val == None:
#         return np.nan
#     if val in acceptable_combinations:
#         parts = [int(part) for part in val.split(',')]
#         return np.mean(parts)
#     try:
#         return float(val)
#     except ValueError:
#         return np.nan


def pre_process_buildings(df):
    """
    Pre-process buildings by cleaning and updating heights and floor counts.
    Input df is the GPKG verisk building data with verisk_premise_id set as upn
    """
    floor_av = load_avg_floor_count()
    glob_av_heights = get_average_heights_table() 
    df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce').fillna(0) 
    df['floor_count_numeric'] = pd.to_numeric(df['premise_floor_count'], errors='coerce')
    
    df = update_outbuildings(df)
    
    df = create_height_bucket_col(df)
    df =fill_premise_floor_types(df, floor_av )
    df = create_height_options( df  , glob_av_heights)
     
    df = update_height_ratio(df,glob_av_heights, floor_av ) 


    df.drop(columns=[x for x in df.columns if 'Unnamed' in x], inplace=True )
    
    df = update_listed_type(df) 
    print('pre process complete')

    if not df[~df['premise_use'].isna()][df['premise_use']!='Unknown'][df['premise_use']!='None'][df['validated_height']==0][df['validated_fc'].isna()].empty:
        print('Wierd entry which failed both validations on height and Floor count ')
        
        print(df[df['validated_height']==0][df['validated_fc'].isna()][['premise_type', 'height', 'premise_floor_count']] )
        raise Exception('Both validations should not have failed - investigate')
    
    return df 

def produce_clean_building_data(df):
    """Filter and test building data."""
    # print("Filtering non-commercial derelict premises...")
    print('len df ', len(df))
    if len(df)==0:
        print('No data to process')
        return None, None 
    filtered_df = df[df['premise_use'] != 'Commercial - derelict'].copy()
    filtered_df = filtered_df[~filtered_df['build_vol_FGA'].isna()].copy()
    invalid = len(df) - len(filtered_df)

    test_building_metrics(filtered_df)
    return df,  invalid

# ============================================================
# Validation and Testing Functions
# ============================================================
def assert_larger(df, col1, col2):
    """Ensure values in col1 are larger than those in col2 where columns are not null."""
    df = df[~df[col1].isna() & ~df[col2].isna()].copy()
    assert (df[col1] >= df[col2]).all(), f"Found rows where {col1} is not larger than {col2}."

def assert_perc(df, col):
    """Ensure values in col are between 0 and 1."""
    assert ((df[col] >= 0) & (df[col] <= 1)).all(), f"Found rows where {col} is not between 0 and 1."

def assert_equal(df, col1, col2):
    """Ensure values in col1 are equal to those in col2."""
    assert (df[col1] == df[col2]).all(), f"For df, found rows where {col1} does not equal {col2}."

def check_nulls_percent(df, col, threshold=0.5):
    """Check if the percentage of nulls in col exceeds a threshold."""
    if df[col].isna().mean() > threshold:
        raise Exception(f'Nulls in {col} are greater than {threshold*100}%.')

  

def test_building_metrics(df):
    """Run various assertions on building metrics."""
    assert_larger(df, 'build_vol_inc_basement_FGA', 'build_vol_FGA')
    assert_larger(df, 'heated_vol_inc_basement_FGA', 'heated_vol_FGA')
    # assert_larger(df, 'heated_vol_inc_basement_EA_FGA', 'heated_vol_EA_FGA')

    metrics_columns = [
        'height_bucket', 'floor_count_numeric_FGA',
        'height_numeric_FGA', 'build_vol_FGA', 'base_floor',
        'build_vol_inc_basement_FGA', 
          'heated_vol_FGA',
        'heated_vol_inc_basement_FGA'
    ]

#  if validated_height ==0 then 
#           validated_height_FGA must be > height
        # validated_fc_FGA == floor_count_numeric_FGA
# if validated_fc.isna() 
# then 

                 
# ============================================================
# Building metric fns 
# ============================================================     

def calculate_volume_metrics(df):
    """Calculate various volume metrics based on building data."""

    # Calculate building volume, considering height and area
    df['build_vol_FGA'] = df['premise_area'] * df['validated_height_FGA']

    # Efficiently determine the presence of a basement
    basement_conditions = [
        df['basement'].isin(['Basement confirmed', 'Basement likely']),
        ~df['basement'].isin(['Basement confirmed', 'Basement likely'])
    ]
    basement_choices = [1, 0]
    df['base_floor'] = np.select(basement_conditions, basement_choices, default=0)

    # Calculate building and heated volumes including basement adjustments
    basement_height_adjustment = df['base_floor'] *  df['premise_area'] * BASEMENT_HEIGHT * BASEMENT_PERCENTAGE_OF_PREMISE_AREA 
    df['build_vol_inc_basement_FGA'] = df['build_vol_FGA'] + basement_height_adjustment

    # df['heated_vol_EA_FGA'] = df['premise_area'] * df['floor_count_element_av_FGA'] * DEFAULT_FLOOR_HEIGHT  
    df['heated_vol_FGA'] = df['premise_area'] * df['validated_fc_FGA'] * DEFAULT_FLOOR_HEIGHT 

    # df['heated_vol_inc_basement_EA_FGA'] = df['heated_vol_EA_FGA'] + basement_height_adjustment
    df['heated_vol_inc_basement_FGA'] = df['heated_vol_FGA'] + basement_height_adjustment

    return df

# ============================================================
# Action functions
# ============================================================
def pre_process_building_data(build):
    
    """Calculate and validate building metrics from verisk data."""
    # print("Pre-processing building data...")
    processed_df = pre_process_buildings(build)

    print("Calculating volume metrics...")
    processed_df = calculate_volume_metrics(processed_df)

    print('Cleaning data')
    clean_df , num_invalid = produce_clean_building_data(processed_df)
    
    return clean_df, num_invalid