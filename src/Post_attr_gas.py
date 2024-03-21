import os
import sys
import time
import geopandas as gpd 
import pandas as pd 
import glob 
import re
import numpy as np 
import matplotlib.pyplot as plt 
from shapely.geometry import Point, Polygon
from shapely.geometry import box
sys.path.append('/Users/gracecolverd/New_dataset')

from src import find_postcode_for_ONSUD_file, find_data_pc, calc_med_attr 

# from src import run_batching, merge_temp_logs_to_main , generate_batch_list, calc_med_attr    

from src import process_postcode, postcode_median_age_batch_fn , run_batching, find_data_pc
from src import calculate_modal_age_band, calc_med_attr , postcode_modal_batch_fn, gen_postcode_areas
from src import postcode_area_vars_batch_fn , fill_premise_floor_types, check_merge_files

res_use_types = ['Residential',  'Residential with retail below', 'Retail below office or residential' ] 



def calc_residential_fuel(df, total_fuel, avg_heights):
    """
    Calculate fuel metrics for residential premises.
    
    Parameters:
    - df: DataFrame containing premise data.
    - total_fuel: Total fuel consumption.
    
    Returns:
    Tuple containing calculated fuel metrics.
    """
    if len(avg_heights) ==0:
        raise Exception('Avg heights df empty')

    print('pre process')       
    # Preprocess DataFrame with floor types
    df = fill_premise_floor_types(df)
    df = update_height_with_average(df, avg_heights)
    
    df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age']) 
    
    # Filter DataFrame for residential use
    residential_df = df[df['premise_use'] == 'Residential'].copy()
    percentage_residential = len(residential_df) / len(df)
    
    # Filter DataFrame for expanded residential use
    expanded_residential_df = df[df['premise_use'].isin(res_use_types)].copy()
    percentage_expanded_residential = len(expanded_residential_df) / len(df)
    
    print('calc fuel')
    # Handle case where total fuel is None
    if total_fuel is None:
        b_metric_res, b_metric_exp_res =  calc_building_metrics(residential_df), calc_building_metrics(expanded_residential_df)
        return initialize_fuel_metrics_with_error_value(percentage_residential, percentage_expanded_residential, b_metric_res, b_metric_exp_res  )

    # Calculate fuel metrics for residential premises
    residential_metrics = calc_fuel_metric(residential_df, total_fuel)
    
    # Calculate fuel metrics for expanded residential, depending on percentage_residential
    if percentage_residential == 1:
        expanded_residential_metrics = residential_metrics
    else:
        expanded_residential_metrics = calc_fuel_metric(expanded_residential_df, total_fuel)
    
    return (percentage_residential, percentage_expanded_residential, total_fuel ) + residential_metrics + expanded_residential_metrics




def initialize_fuel_metrics_with_error_value(percentage_residential, percentage_expanded_residential, b_metric_res, b_metric_exp_res  ):
    """
    Initializes fuel metrics with a placeholder error value when total fuel is None.
    
    Parameters:
    - percentage_residential: Percentage of residential premises.
    
    Returns:
    Tuple containing initialized metrics with error value.
    """
    # total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement  = b_metrics
    error_value = -333
    metrics = (error_value,) * 6
    return (percentage_residential, percentage_expanded_residential, -333) + metrics +  b_metric_res + metrics  + b_metric_exp_res  


def calc_building_metrics(df, build_perc_val = 0.85):

    # if height is 0, no build vol
    df['build_vol'] = np.where(df['height'] == 0, None , df['premise_area'] * df['height'])
    df['base_floor'] = df['basement'].apply(lambda x: 1 if x in ['Basement confirmed', 'Basement likely'] else 0)
    
    df['build_vol_inc_basement'] =df.apply(lambda row: row['build_vol']  + (row['base_floor'] * 2.4 ), axis=1) 

    
    df['heated_vol'] = df.apply(lambda row: row['premise_area'] * int(row['premise_floor_count']) * get_val_from_age_band(row), axis=1)
    df['heated_vol_inc_basement'] =df.apply(lambda row: row['heated_vol']  + (row['base_floor'] * 2.4), axis=1) 
    
    
    total_build_volume = df['build_vol'].sum()
    total_build_volume_inc_basement = df['build_vol_inc_basement'].sum()
    total_heated_volume = df['heated_vol'].sum()
    total_heated_volume_inc_basement = df['heated_vol_inc_basement'].sum()


    # Take the smaller of heated_volume or 80% of total_volume, and assign it to a new column
    total_heated_optimal_volume = np.minimum(    total_build_volume * build_perc_val, total_heated_volume) 
    total_heated_optimal_volume_inc_basement = np.minimum(    total_build_volume_inc_basement * build_perc_val, total_heated_volume_inc_basement) 

    return total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement, total_heated_optimal_volume, total_heated_optimal_volume_inc_basement




def calc_fuel_metric(df, total_fuel):
    """
    Calculate various fuel metrics based on the DataFrame and total fuel.
    
    Parameters:
    - df: DataFrame of premises.
    - total_fuel: Total fuel consumption.
    
    Returns:
    Tuple containing fuel metrics.
    """
    # Calculate building and heated volumes
    total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement , total_heated_optimal_volume, total_heated_optimal_volume_inc_basement  = calc_building_metrics(df)
    b_metrics = total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement,  total_heated_optimal_volume, total_heated_optimal_volume_inc_basement

    # Calculate fuel metrics
    if total_heated_volume ==0:
        gas_per_heated_vol , gas_per_heated_vol_inc_basement= -777 , -777
    else:
        gas_per_heated_vol = total_fuel /  total_heated_volume
        gas_per_heated_vol_inc_basement = total_fuel / total_heated_volume_inc_basement  
        gas_per_optimal_vol = total_fuel /total_heated_optimal_volume 
        gas_per_optimal_vol_inc_basemenet = total_fuel / total_heated_optimal_volume_inc_basement
    if total_build_volume ==0:
        gas_per_total_vol ,gas_per_total_vol_inc_basement , gas_per_optimal_vol, gas_per_optimal_vol_inc_basemenet = -777, -777 , -777 , -777 
    else:
        gas_per_total_vol = total_fuel / total_build_volume 
        gas_per_total_vol_inc_basement = total_fuel / total_build_volume_inc_basement
    
    return (  gas_per_heated_vol, gas_per_heated_vol_inc_basement, gas_per_optimal_vol,  gas_per_optimal_vol_inc_basemenet, gas_per_total_vol, gas_per_total_vol_inc_basement,  ) + b_metrics 




def get_val_from_age_band(row):
    age_band = row['premise_age']
    if age_band == 'Pre 1919':
        val = 3
    elif age_band == '1919-1944':
        val = 2.9
    elif age_band == '1945-1959':
        val = 2.8
    elif age_band == '1960-1979':
        val = 2.2
    elif age_band == '1980-1989':
        val = 2.2
    elif age_band == '1990-1999':
        val = 2.2
    elif age_band == 'Post 1999':
        val = 2.4
    else:
        val = 2.3
    return val

 

def correct_floor_counts(df):
    """
    Corrects 'premise_floor_count' in the dataframe to ensure all values are integers.
    Non-integer values are rounded to the nearest integer.

    Parameters:
    - df: DataFrame containing the 'premise_floor_count' column.

    Returns:
    - DataFrame with corrected 'premise_floor_count'.
    """
    # Ensure 'premise_floor_count' is numeric and round to nearest integer if not already an integer
    df['premise_floor_count'] = pd.to_numeric(df['premise_floor_count'], errors='coerce').fillna(0)
    df['premise_floor_count'] = np.round(df['premise_floor_count']).astype(int)
    
    return df



def get_average_heights_table():
    """
    Create average heights grouping by age, floor count and use (residential, commerical, mixed) 
    TODO fix hard code csv
    """
    df = pd.read_csv('/Users/gracecolverd/New_dataset/data/mappings/abg_heights_whole_uk.csv' )
    df= df[df['map_simple_use']=='Residential'] 
    df['premise_floor_count'] = df['premise_floor_count'].astype(int)
    return df 

def update_height_with_average(df, avg_heights):
    """ 
    Update height of df with average from avg_heights, joining on age, floor count and map simple use 
    """
    
    # Merge the average heights back into the original dataframe
    check_merge_files(df, avg_heights, 'premise_floor_count', 'premise_floor_count')
    df['premise_floor_count']= df['premise_floor_count'].astype('int')
    df = pd.merge(df, avg_heights, on=['premise_age', 'premise_floor_count', 'map_simple_use'], how='left')

    # Update 'height' where it is 0 with the 'avg_height' from the same 'premise_age' and 'premise_floor_count' combination
    df['height'] = np.where(df['height'] == 0, df['weighted_average_height'], df['height'])

    # Drop the 'avg_height' column as it's no longer needed
    df.drop('weighted_average_height', axis=1, inplace=True)

    return df




def postcode_fuel_vars_batch_fn(pc, data, merge_fuel, avg_heights):
    input_gpk= '/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg'

    fuel = merge_fuel[merge_fuel['Postcode']==pc ]
    if len(fuel)==0:
        total_fuel = None
    else:
        total_fuel = fuel['Total_cons_kwh'].values[0]
    if len(fuel) >1:
        raise ValueError('Too many fuel values found')
   
    uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
    if uprn_match.empty:
        return pc, 'Completed', 'No buildings found'  
    
    attr_value = calc_residential_fuel(uprn_match, total_fuel, avg_heights )
    
    return pc, 'Completed', attr_value 
    