
import pandas as pd
import numpy as np
local=True 
# ============================================================
# Constants
# ============================================================
BUILD_PERC_VAL = 0.85
BASEMENT_HEIGHT = 2.4
BASEMENT_PERCENTAGE_OF_PREMISE_AREA = 1
DEFAULT_FLOOR_HEIGHT = 2.3

# ============================================================
# Data Loading Functions
# ============================================================

def load_avg_floor_count():
    """Load the average floor count data from a CSV file."""
    if local is True:
        path = '/Users/gracecolverd/New_dataset/src/mapping/avg_floor_counts_whole_uk.csv'
    else:
        path = 'src/mapping/avg_floor_counts_whole_uk.csv'
    return pd.read_csv(path)

def get_average_heights_table():
    """Load a CSV file containing average heights grouped by criteria."""
    if local==True:
        path = '/Users/gracecolverd/New_dataset/src/mapping/avg_heights_whole_uk.csv'
    else:
        path = 'src/mapping/avg_heights_whole_uk.csv'
    return pd.read_csv(path)



# ============================================================
# Height and Floor Count functions & Pre processing of columns 
# ============================================================
def update_avg_floor_count(df, input_col, avg_table, suffix):
    """Update DataFrame column with average floor count values based on criteria."""
    if (df[input_col] == 0).any():
        raise ValueError('Some floor counts are set to 0, expecting NaN for missing values.')
    df = pd.merge(df, avg_table, on=['premise_age', 'height_bucket', 'map_simple_use'], how='left')
    df[f'{input_col}_{suffix}'] = np.where(df[input_col].isna(), df['weighted_average_floor_count'], df[input_col])
    df.drop('weighted_average_floor_count', axis=1, inplace=True)
    return df

def fill_premise_floor_types(df, glob_av_df):
    """Fill missing premise floor types with global averages."""
    df['floor_count_numeric'] = pd.to_numeric(df['premise_floor_count'], errors='coerce')
    df = update_avg_floor_count(df, 'floor_count_numeric', glob_av_df, 'FGA')
    df['floor_count_element_av'] = df['premise_floor_count'].apply(handle_comma_separated_values)
    df = update_avg_floor_count(df, 'floor_count_element_av', glob_av_df, 'FGA')
    return df

def create_height_bucket_col(df):
    """Bucket height into predefined categories."""
    height_bins = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 18, 20, 30, 40, 50, 100, 200]
    height_labels = [f"{b}-{height_bins[i+1]}m" for i, b in enumerate(height_bins[:-1])]
    df['height_bucket'] = pd.cut(df['height_numeric'], bins=height_bins, labels=height_labels, right=False)
    return df

def update_height_with_average(df, input_col, avg_table, suffix):
    """Update the height column with averages based on age, floor count, and use."""
    # Merge with the average table
    df = pd.merge(df, avg_table, on=['premise_age', 'premise_floor_count', 'map_simple_use'], how='left')
    
    # Update heights with averages where applicable
    update_col_name = f'{input_col}_{suffix}'
    df[update_col_name] = np.where(df[input_col] == 0, df['weighted_average_height'], df[input_col])
    
    # Drop the temporary column
    df.drop('weighted_average_height', axis=1, inplace=True)
    return df

def create_height_options(df, glob_av_df):
    """Fill in missing or zero heights with global averages."""
    # Convert 'height' to numeric, filling non-convertible values with 0
    df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce').fillna(0)
    
    # Check for unexpected NaN values after conversion
    if df['height_numeric'].isna().any():
        raise ValueError('Unexpected NaN values found in height_numeric.')
    
    # Update heights using the global averages table
    df = update_height_with_average(df, 'height_numeric', glob_av_df, 'FGA')
    return df

def update_listed_type(df):
    df.loc[:, 'listed_bool'] = df['listed_grade'].apply(lambda x: 1 if x is not None else 0)
    return df 



# ============================================================
# Utility Functions
# ============================================================
def handle_comma_separated_values(val):
    """Handle comma-separated floor count values."""
    acceptable_combinations = ['1,2', '2,3', '3,4', '1,3', '4,5', '3,5', '5,6', '4,6', '5,7', '6,7', '6,8', '7,8', '8,9', '9,10', '8,10', '7,9']
    if val =='' or val == None:
        return np.nan
    if val in acceptable_combinations:
        parts = [int(part) for part in val.split(',')]
        return np.mean(parts)
    try:
        return float(val)
    except ValueError:
        return np.nan


def pre_process_buildings(df):
    """
    Pre-process buildings by cleaning and updating heights and floor counts.
    Input df is the GPKG verisk building data with verisk_premise_id set as upn
    """

    excluded = df[(df['height'].isna())  &  ( df['premise_floor_count'].isna() ) & ( df['premise_use']=='Unknown') ]
    df = df[~df['upn'].isin(excluded.upn.unique().tolist() ) ].copy() 
    floor_av = load_avg_floor_count()
    df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce').fillna(0) 
    df['floor_count_numeric'] = pd.to_numeric(df['premise_floor_count'], errors='coerce')
    df = create_height_bucket_col(df) 

    df = update_avg_floor_count(df , 'floor_count_numeric',  floor_av , 'FGA')
    df['floor_count_element_av'] = df['premise_floor_count'].apply(handle_comma_separated_values)
    df = update_avg_floor_count(df , 'floor_count_element_av',  floor_av , 'FGA')
    glob_av_heights = get_average_heights_table() 
    df = create_height_options( df  , glob_av_heights)
    df.drop(columns=[x for x in df.columns if 'Unnamed' in x], inplace=True )
    
    df = update_listed_type(df) 
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
    return filtered_df,  invalid

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
    assert_larger(df, 'heated_vol_inc_basement_EA_FGA', 'heated_vol_EA_FGA')

    metrics_columns = [
        'height_bucket', 'floor_count_numeric_FGA', 'floor_count_element_av_FGA',
        'height_numeric_FGA', 'build_vol_FGA', 'base_floor',
        'build_vol_inc_basement_FGA', 'heated_vol_EA_FGA', 'heated_vol_FGA',
        'heated_vol_inc_basement_EA_FGA', 'heated_vol_inc_basement_FGA'
    ]

    for col in metrics_columns:
        check_nulls_percent(df, col)

    # print('DF passed tests')

                 
# ============================================================
# Building metric fns 
# ============================================================     

def calculate_volume_metrics(df):
    """Calculate various volume metrics based on building data."""

    # Calculate building volume, considering height and area
    df['build_vol_FGA'] = df['premise_area'] * df['height_numeric_FGA']

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

    df['heated_vol_EA_FGA'] = df['premise_area'] * df['floor_count_element_av_FGA'] * DEFAULT_FLOOR_HEIGHT  
    df['heated_vol_FGA'] = df['premise_area'] * df['floor_count_numeric_FGA'] * DEFAULT_FLOOR_HEIGHT 

    df['heated_vol_inc_basement_EA_FGA'] = df['heated_vol_EA_FGA'] + basement_height_adjustment
    df['heated_vol_inc_basement_FGA'] = df['heated_vol_FGA'] + basement_height_adjustment

    return df

# ============================================================
# Action functions
# ============================================================
def pre_process_building_data(build):
    
    """Calculate and validate building metrics from verisk data."""
    # print("Pre-processing building data...")
    processed_df = pre_process_buildings(build)

    # print("Calculating volume metrics...")
    processed_df = calculate_volume_metrics(processed_df)

    # print("Producing clean building data...")
    clean_df , num_invalid = produce_clean_building_data(processed_df)
    # print('Pre process of building data complete')
    return clean_df, num_invalid
