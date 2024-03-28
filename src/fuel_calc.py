import pandas as pd
import sys 
import numpy as np  
from src.postcode_attr import find_data_pc
from src.pre_process_buildings import pre_process_building_data 

import numpy as np

def calc_df_sum_attribute(df, cols, prefix=''):
    """Takes input df with only one postcode and calcs attributes based on summing the building columns."""

    attr_dict = {}
    attr_dict[prefix + 'total_buildings'] = len(df)
    for col in cols:
        # Use .sum(min_count=1) to return NaN if there are no valid values to sum (all are NaN)
        attr_dict[prefix + col + '_total'] = df[col].sum(min_count=1)
    return attr_dict

# def calculate_postcode_attr(df):
#     print(len(df))

#     df = df.reset_index(drop=True)  # Reset index to ensure alignment

#     cols = ['build_vol_FGA', 'base_floor', 'build_vol_inc_basement_FGA', 'heated_vol_EA_FGA', 
#             'heated_vol_FGA', 'heated_vol_inc_basement_EA_FGA', 'heated_vol_inc_basement_FGA', 'listed_bool'
#             'premusetype_2 storeys terraces with t rear extension',
#  'premusetype_3-4 storey and smaller flats',
#  'premusetype_Domestic outbuilding',
#  'premusetype_Large detached',
#  'premusetype_Large semi detached',
#  'premusetype_Linked and step linked premises',
#  'premusetype_Medium height flats 5-6 storeys',
#  'premusetype_Planned balanced mixed estates',
#  'premusetype_Semi type house in multiples',
#  'premusetype_Small low terraces',
#  'premusetype_Standard size detached',
#  'premusetype_Standard size semi detached',
#  'premusetype_Tall flats 6-15 storeys',
#  'premusetype_Tall terraces 3-4 storeys',
#  'premusetype_Very large detached',
#  'premusetype_Very tall point block flats']
    

#     dc = calc_df_sum_attribute(df, cols, 'all_types_')

#     res_df = df[df['map_simple_use'] == 'Residential'].copy()
#     dc_res = calc_df_sum_attribute(res_df, cols, 'res_') if not res_df.empty else {prefix + 'total_buildings': np.nan for prefix in ['res_'] + [f'res_{col}_total' for col in cols]}

#     mixed_use_df = df[df['map_simple_use'] == 'Mixed Use'].copy()
#     dc_mixed = calc_df_sum_attribute(mixed_use_df, cols, 'mixed_') if not mixed_use_df.empty else {prefix + 'total_buildings': np.nan for prefix in ['mixed_'] + [f'mixed_{col}_total' for col in cols]}

#     comm_use = df[df['map_simple_use'] == 'Commercial'].copy()
#     dc_comm = calc_df_sum_attribute(comm_use, cols, 'comm_') if not comm_use.empty else {prefix + 'total_buildings': np.nan for prefix in ['comm_'] + [f'comm_{col}_total' for col in cols]}

#     dc.update(dc_res)
#     dc.update(dc_mixed)
#     dc.update(dc_comm)
#     return dc


def generate_null_attributes(prefix, cols):
    """
    Generate a dictionary with all column names prefixed as specified, 
    with np.nan values, for the case where there's no data.
    
    Parameters:
    - prefix: The prefix to be applied to each column name ('all_types_', 'res_', 'mixed_', or 'comm_').
    - cols: The list of column names that are expected in the non-null case.

    Returns:
    - A dictionary with keys as the prefixed column names and np.nan as all values.
    """

    null_attributes= {f'{prefix}total_buildings': np.nan}

    # Add entries for each column in cols, prefixed and set to np.nan
    for col in cols:
        null_attributes[f'{prefix}{col}_total'] = np.nan
    
    return null_attributes


def generate_null_attributes_full( prefix, cols ):
    """
    Generate a dictionary with all column names prefixed as specified, 
    with np.nan values, for the case where there's no data.
    
    Parameters:
    - prefix: The prefix to be applied to each column name ('all_types_', 'res_', 'mixed_', or 'comm_').
    - cols: The list of column names that are expected in the non-null case.

    Returns:
    - A dictionary with keys as the prefixed column names and np.nan as all values.
    """
    # null_attributes={'postcode':pc, 'num_invalid_builds': np.nan }
    null_attributes= {} 

    for p in prefix:
        # Initialize the dictionary with the total_buildings count set to np.nan
        null_attributes[f'{p}total_buildings']=  np.nan 
        # Add entries for each column in cols, prefixed and set to np.nan
        for col in cols:
            null_attributes[f'{p}{col}_total'] = np.nan
        
    return null_attributes

def calculate_postcode_attr_with_null_case(df ):
    
    # Define the columns to summarize
    cols = ['build_vol_FGA', 'base_floor', 'build_vol_inc_basement_FGA', 'heated_vol_EA_FGA', 
            'heated_vol_FGA', 'heated_vol_inc_basement_EA_FGA', 'heated_vol_inc_basement_FGA', 'listed_bool', 'uprn_count' 
            ]
    
    prefix = ['all_types_', 'res_', 'mixed_', 'comm_']

    if df is None:
        return generate_null_attributes_full( prefix, cols )
    
    # Generate attributes for all types
    dc = calc_df_sum_attribute(df, cols, 'all_types_')

    # Generate attributes for Residential, Mixed Use, and Commercial or set to null if no data
    res_df = df[df['map_simple_use'] == 'Residential'].copy()
    dc_res = calc_df_sum_attribute(res_df, cols, 'res_') if not res_df.empty else generate_null_attributes('res_', cols)

    mixed_use_df = df[df['map_simple_use'] == 'Mixed Use'].copy()
    dc_mixed = calc_df_sum_attribute(mixed_use_df, cols, 'mixed_') if not mixed_use_df.empty else generate_null_attributes('mixed_', cols)

    comm_use = df[df['map_simple_use'] == 'Commercial'].copy()
    dc_comm = calc_df_sum_attribute(comm_use, cols, 'comm_') if not comm_use.empty else generate_null_attributes('comm_', cols)

    # Merge the dictionaries
    dc.update(dc_res)
    dc.update(dc_mixed)
    dc.update(dc_comm)

    return dc



def get_fuel_vars(pc, f , fuel_df):
    # print('getting fuel vars')
    dc_fuel={}
    pc_fuel = fuel_df[fuel_df['Postcode']==pc].copy()
    if len(pc_fuel)==0: 
        # print(f'No fuel data found for postcode {pc}')
        dc_fuel = {f'total_{f}':np.nan, f'avg_{f}':np.nan, f'median_{f}':np.nan, f'num_meters_{f}':np.nan}
        return dc_fuel
    else:
        dc_fuel[f'num_meters_{f}'] = pc_fuel['Num_meters'].values[0]  
        dc_fuel[f'total_{f}'] = pc_fuel['Total_cons_kwh'].values[0]
        dc_fuel[f'avg_{f}'] = pc_fuel['Mean_cons_kwh'].values[0]
        dc_fuel[f'median_{f}'] = pc_fuel['Median_cons_kwh'].values[0] 

    return dc_fuel


def check_duplicate_primary_key(df, primary_key_column):
    # print('checking dupes')
    is_duplicate = df[primary_key_column].duplicated().any()
    return is_duplicate






def process_postcode_fuel(pc, data, gas_df, elec_df, INPUT_GPK):
    """Process one postcode, deriving building attributes and electricity and fuel info."""
    print(pc)
    uprn_match = find_data_pc(pc, data, input_gpk=INPUT_GPK)
    
    # Generate building metrics, clean and test
    df , num_invalid = pre_process_building_data(uprn_match)    

    dc_full = {'postcode': pc, 'num_invalid_builds': num_invalid }
    dc = calculate_postcode_attr_with_null_case(df)
    dc_full.update(dc)
    if df is not None:
        if check_duplicate_primary_key(df, 'upn'):
            print('Duplicate primary key found for upn')
            sys.exit()
 

    dc_gas = get_fuel_vars(pc, 'gas', gas_df)
    dc_elec = get_fuel_vars(pc, 'elec', elec_df)
    dc_full.update(dc_gas)
    dc_full.update(dc_elec)

    return dc_full
