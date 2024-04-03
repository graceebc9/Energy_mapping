import pandas as pd
import sys 
import numpy as np  
from src.old.postcode_attr import find_data_pc
from src.pre_process_buildings import pre_process_buildings 
from src.fuel_calc import check_duplicate_primary_key 


def age_mapping():
    category_order = [  'Pre 1919',
                        '1919-1944',
                        '1945-1959', 
                        '1960-1979',
                        '1980-1989',
                        '1990-1999',
                        'Post 1999' 
                        ]
    category_to_ordinal = {category: i for i, category in enumerate(category_order)}
    ordinal_to_category = {i: category for i, category in enumerate(category_order)}    
    return category_to_ordinal, ordinal_to_category, category_order 


def bucket_age(df):
    df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age'])

    category_to_ordinal, _, _  = age_mapping()

    df['ordinal_age'] = df['premise_age_bucketed'].map(category_to_ordinal)
    
    return df 

def calculate_modal_age_band(df , age_col):
    """ Fn to calculate the modal age band of a column for a df (needs contain all same postcodes)
    Assumptions: less than 10% unknowns ignore, all varaibles pre 1919 to one variable 
    """
    # df = df[df['premise_age_bucketed']!='Unknown date']  
    mode = df[age_col].mode()[0]

    return  mode 
    
def calc_range_age(df, ord_col):
    """ Fn to calculate the range of the age band of a column for a df (needs contain all same postcodes)
    Assumptions: all varaibles pre 1919 to one variable 
    """
    # alll variables pre 1919 updated to be one variable 

    min_age = df[ord_col].min()
    max_age = df[ord_col].max()
    distinct_ages = df[ord_col].nunique()

    return min_age, max_age, distinct_ages 

def calculate_median_age_band(df, age_col, ord_col):
    """
    Calculate the median of a categorical column based on a specified ordering.
    """
    def calc_med(df):
        ordinal_values = df[age_col].map(category_to_ordinal)
        median_ordinal = ordinal_values.median()
        median_category = category_order[int(np.round(median_ordinal))]
        return median_category

    def calc_iqr(df):
        q1 =  df[ord_col].quantile(0.25)
        q3 = df[ord_col].quantile(0.75)
        iqr = q3 - q1
        return iqr 

    category_to_ordinal, _ , category_order = age_mapping() 

    iqr = calc_iqr(df)
    median = calc_med(df)

    return median, iqr 


def calc_age_attributes(df, prefix):
    """ Fn to calculate the median age band of a column for a df 
    Inputs:
    --df: dataframe containing only one postcode 
    """
    

    if prefix =='localfill':
        age_col = 'loc_fill_age'
        ord_col = 'loc_ordinal'
    elif prefix =='globalfill':    
        age_col = 'global_fill_age'
        ord_col = 'global_ordinal'

    median,  iqr  = calculate_median_age_band(df , age_col= age_col, ord_col= ord_col)
    modal_age  = calculate_modal_age_band(df, age_col)

    min_age, max_age, distinct_ages   = calc_range_age(df, ord_col=ord_col)
    range_age = max_age - min_age

    _, ord_to_cat, _  = age_mapping() 

    min_age = ord_to_cat[min_age  ]
    max_age = ord_to_cat[max_age]
    
    return  median, modal_age , min_age, max_age, range_age,  distinct_ages,  iqr



def process_postcode_age_residential(pc, data, INPUT_GPK, premise_dict):
    """Process one postcode, """
    
    def all_unknowns(df):   
        if len(df[df['premise_type'].isnull()])==len(df):
            print('All unknowns')
            dc = generate_nulls(cols, pc, prefixes)
            return dc
        else:
            dicc= {} 
            print('All unknowns but some type')    
            df['global_fill_age'] = np.where(df['premise_age_bucketed'] == 'Unknown date', df['premise_type'].map(premise_dict), df['premise_age_bucketed'])
            df['global_ordinal'] = df['global_fill_age'].map(category_to_ordinal)   
            dc = calc_age_attributes(df, 'globalfill')
            for i, col in enumerate(cols ) :
                dicc[f'globalfill_{col}'] = dc[i]
            dc_local = generate_nulls(cols, pc, ['localfill'])
            for i , col in enumerate(cols):
                dicc[f'localfill_{col}'] = dc_local[i]
            return dicc
    
    def normal_df(df):
        df['loc_fill_age'] = np.where(df['premise_age_bucketed'] == 'Unknown date', df['premise_age_bucketed'].mode()[0], df['premise_age_bucketed'])
        df['loc_ordinal'] = df['loc_fill_age'].map(category_to_ordinal)
        df['global_fill_age'] = np.where(df['premise_age_bucketed'] == 'Unknown date', df['premise_type'].map(premise_dict), df['premise_age_bucketed'])
        df['global_ordinal'] = df['global_fill_age'].map(category_to_ordinal)   
        dicc= {} 
        for prefix in prefixes:
            dc = calc_age_attributes(df, prefix)
            for i, col in enumerate(cols ) :
                dicc[f'{prefix}_{col}'] = dc[i]
        return dicc
    
    cols = [ 'median_age', 'modal_age', 'min_age', 'max_age', 'range_age', 'distinct_ages', 'iqr_age' ]
    prefixes = ['localfill', 'globalfill']
    

    category_to_ordinal, _, _  = age_mapping()
    
    uprn_match = find_data_pc(pc, data, input_gpk=INPUT_GPK)
    
    if uprn_match is None or uprn_match.empty:
        dc= generate_nulls(cols, pc, prefixes)
        return dc 
       
    # Generate building metrics, clean and test
    df  = pre_process_buildings(uprn_match)    
    # only calc for wholly residential 
    if len(df[df['premise_use']=='Residential']) != len(df):
        print('Not wholly residential')
        return generate_nulls(cols, pc, prefixes)

    if check_duplicate_primary_key(df, 'upn'):
        raise Exception('Duplicate primary key found for upn')
    
    if df.empty or len(df)==1:
        dc= generate_nulls(cols, pc, prefixes)
        return dc
    
    df = bucket_age(df)
    count_unknown = df[df['premise_age_bucketed']=='Unknown date'].shape[0]
    dc_full = {'postcode': pc, 'count_unknown_age': count_unknown  }     

    if len(df[df['premise_age_bucketed']=='Unknown date']) == len(df):
        print('Starting all unknown postcode')
        dicc = all_unknowns(df)
    else:
        dicc= normal_df(df)
        

    dc_full.update(dicc )
   
    return dc_full 


def generate_nulls(cols, pc, prefixes):
    dc = {'postcode': pc, 'count_unknown_age': np.nan  }
    for prefix in prefixes:
        for col in cols:
            dc[f'{prefix}_{col}'] = np.nan 
    return dc

 


        



# def calc_age_attributes(df, global_df):
#     """ Fn to calculate the median age band of a column for a df 
#     Inputs:
#     --df: dataframe containing only one postcode 
#     """
#     if len(df)==1:
#         print('Only one building')
#         age = df['premise_age'].values[0]
#         if age =='Unknown date':
#             if df['premise_type'].values[0] == None :
#                 print('Unknown date and none type')
#                 return np.nan, np.nan, age, age, age, 0, 1, np.nan, np.nan
#             else: 
#                 df.merge(global_df, on =['premise_use', 'premise_use'])
#         return np.nan, np.nan, age, age, age, 0, 1, np.nan, np.nan
    
#     ignore_median, modal_median,  ignore_iqr, modal_iqr = calculate_median_age_band(df )
#     modal_age  = calculate_modal_age_band(df)

#     min_age, max_age, distinct_ages   = calc_range_age(df)

#     range_age = max_age - min_age

#     _, ord_to_cat, _  = age_mapping() 

#     min_age = ord_to_cat[min_age  ]
#     max_age = ord_to_cat[max_age]
    


#     return  ignore_median, modal_median, modal_age , min_age, max_age, range_age,  distinct_ages,  ignore_iqr, modal_iqr





# def process_postcode_age_residential(pc, data, INPUT_GPK):
#     """Process one postcode, """
#     cols = [ 'ignorefill_median_age', 'modalfill_median_age', 'modal_age', 'min_age', 'max_age', 'range_age', 'distinct_ages', 'ignorefill_iqr_age', 'modalfill_iqr_age']
    
#     uprn_match = find_data_pc(pc, data, input_gpk=INPUT_GPK)
    
#     if uprn_match is None or len(uprn_match) == 0:
#         dc= generate_nulls(cols, pc)
#         return dc 
       
#     # Generate building metrics, clean and test
#     df  = pre_process_buildings(uprn_match)    
#     # only calc for wholly residential 
#     if len(df[df['premise_use']=='Residential']) != len(df):
#         print('Not wholly residential')
#         dc= generate_nulls(cols, pc)
#         return dc

    
#     if check_duplicate_primary_key(df, 'upn'):
#         raise Exception('Duplicate primary key found for upn')

#     df = bucket_age(df)
#     count_unknown = df[df['premise_age_bucketed']=='Unknown date'].shape[0]

#     dc_full = {'postcode': pc, 'count_unknown_age': count_unknown  }     
    
#     dicc= {} 
#     dc = calc_age_attributes(df)
#     for i, col in enumerate(cols ) :
#         dicc[col] = dc[i]

#     dc_full.update(dicc )
            
#     return dc_full 


# def calculate_median_age_band(df):
#     """
#     Calculate the median of a categorical column based on a specified ordering.

#     Parameters:
#     - df: pandas DataFrame containing the data.
#     - modal_ignore: str, whether to use the modal value for unknown dates ('modal') or ignore unknown dates ('ignore').

#     Returns:
#     - The category that represents the median.
#     """
#     def calc_med(df):
#         ordinal_values = df['premise_age_bucketed'].map(category_to_ordinal)
#         median_ordinal = ordinal_values.median()
#         median_category = category_order[int(np.round(median_ordinal))]
#         return median_category

#     def calc_iqr(df):
#         q1 =  df['ordinal_age'].quantile(0.25)
#         q3 = df['ordinal_age'].quantile(0.75)
#         iqr = q3 - q1
#         return iqr 

#     category_to_ordinal, _ , category_order = age_mapping() 
#     df_ignore  = df[df['premise_age_bucketed']!='Unknown date'].copy() 

#     df['premise_age_bucketed'] = df['premise_age_bucketed'].replace('Unknown date', df['premise_age_bucketed'].mode()[0])    

#     if len(df_ignore) == 0:
#         print('No data for ignore')
#         ignore_median = np.nan 
#     else:
#         ignore_median = calc_med(df_ignore)

#     if len(df) == 0:
#         modal_median = np.nan
#     else:
#         modal_median = calc_med(df)

#     ignore_iqr = calc_iqr(df_ignore)
#     modal_iqr = calc_iqr(df)

#     return ignore_median, modal_median, ignore_iqr, modal_iqr
        