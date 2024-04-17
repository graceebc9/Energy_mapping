

import pandas as pd
import numpy as np
import os 


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
    # df['validated_fc'] = pd.to_numeric(df['premise_floor_count'], errors='coerce')
    df = update_avg_floor_count(df, fc_col, glob_av_df, 'FGA')
    # df['floor_count_element_av'] = df['premise_floor_count'].apply(handle_comma_separated_values)
    # df = update_avg_floor_count(df, 'floor_count_element_av', glob_av_df, 'FGA')
    return df


def create_height_bucket_col(df):
    """Bucket height into predefined categories."""
    # df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce').fillna(0) 
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
    print('starting merge') 
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
    print('starting update hegihts')
    highs['min_side'] = highs['geometry'].apply(min_side)
    highs['threex_minside'] = [x * 3 for x in highs['min_side']]
    highs['validated_height'] = np.where(highs[height_col] >= highs['threex_minside'],   np.nan,  highs[height_col])
    highs['validated_height'] = highs['validated_height'].fillna(0)
    print('start update heights')
    highs=update_height_with_average_flexifc(highs, 'validated_height', fc_col , glob_av_height, 'val' )
    highs['validated_fc'] = np.where(highs['height']< highs['threex_minside'] , np.nan, highs[fc_col])
    print('start update fc')
    highs = update_avg_floor_count(highs, 'validated_fc', glo_av_flc, 'val' ) 
    print('complete')
    # highs['corr_fl_height'] = highs['validated_height_glob_fill'] / highs['validated_fc_glob_fill']
    return highs 

def update_outbuildings(test):
    test.loc[(test['height']==3) & (test['premise_floor_count'] == '2') & (test['uprn_count'] == 0), 'premise_type'] = 'Domestic outbuilding'
    # test = create_height_bucket_col(test)
    return test



def pre_process_buildings(df):
    """
    Pre-process buildings by cleaning and updating heights and floor counts.
    Input df is the GPKG verisk building data with verisk_premise_id set as upn
    """

    excluded = df[(df['height'].isna())  &  ( df['premise_floor_count'].isna() ) & ( df['premise_use']=='Unknown') ]
    df = df[~df['upn'].isin(excluded.upn.unique().tolist() ) ].copy() 
    floor_av = load_avg_floor_count()
    glob_av_heights = get_average_heights_table() 
    df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce').fillna(0) 
    df['floor_count_numeric'] = pd.to_numeric(df['premise_floor_count'], errors='coerce')
    
    df = update_outbuildings(df)
    
    df = create_height_bucket_col(df)
    df =fill_premise_floor_types(df, floor_av )
    df = create_height_options( df  , glob_av_heights)
     
    df = update_height_ratio(df,glob_av_heights, floor_av ) 
    
    df = create_height_options( df  , glob_av_heights, height_col='validated_height_val')
    print(df.columns )

    df.drop(columns=[x for x in df.columns if 'Unnamed' in x], inplace=True )
    
    df = update_listed_type(df) 
    print('pre process complete')
    return df 