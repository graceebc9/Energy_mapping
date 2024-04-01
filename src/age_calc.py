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

def calculate_modal_age_band(df ):
    """ Fn to calculate the modal age band of a column for a df (needs contain all same postcodes)
    Assumptions: less than 10% unknowns ignore, all varaibles pre 1919 to one variable 
    """

    df = df[df['premise_age_bucketed']!='Unknown date']  
    mode = df['premise_age_bucketed'].mode()[0]
    return  mode 
    
def calc_range_age(df):
    """ Fn to calculate the range of the age band of a column for a df (needs contain all same postcodes)
    Assumptions: all varaibles pre 1919 to one variable 
    """
    # alll variables pre 1919 updated to be one variable 

    min_age = df['ordinal_age'].min()
    max_age = df['ordinal_age'].max()
    distinct_ages = df['ordinal_age'].nunique()

    
    return min_age, max_age, distinct_ages 

def calculate_median_age_band(df):
    """
    Calculate the median of a categorical column based on a specified ordering.

    Parameters:
    - df: pandas DataFrame containing the data.
    - modal_ignore: str, whether to use the modal value for unknown dates ('modal') or ignore unknown dates ('ignore').

    Returns:
    - The category that represents the median.
    """
    def calc_med(df):
        ordinal_values = df['premise_age_bucketed'].map(category_to_ordinal)
        median_ordinal = ordinal_values.median()
        median_category = category_order[int(np.round(median_ordinal))]
        return median_category

    def calc_iqr(df):
        q1 =  df['ordinal_age'].quantile(0.25)
        q3 = df['ordinal_age'].quantile(0.75)
        iqr = q3 - q1
        return iqr 

    category_to_ordinal, _ , category_order = age_mapping() 
    df_ignore  = df[df['premise_age_bucketed']!='Unknown date'].copy() 

    df['premise_age_bucketed'] = df['premise_age_bucketed'].replace('Unknown date', df['premise_age_bucketed'].mode()[0])    

    ignore_median = calc_med(df_ignore)
    modal_median = calc_med(df)

    ignore_iqr = calc_iqr(df_ignore)
    modal_iqr = calc_iqr(df)


        

    return ignore_median, modal_median, ignore_iqr, modal_iqr
        


def calc_age_attributes(df):
    """ Fn to calculate the median age band of a column for a df 
    Inputs:
    --df: dataframe containing only one postcode 
    """
    
    ignore_median, modal_median,  ignore_iqr, modal_iqr = calculate_median_age_band(df )
    modal_age  = calculate_modal_age_band(df)

    min_age, max_age, distinct_ages   = calc_range_age(df)

    range_age = max_age - min_age

    _, ord_to_cat, _  = age_mapping() 

    min_age = ord_to_cat[min_age  ]
    max_age = ord_to_cat[max_age]
    


    return  ignore_median, modal_median, modal_age , min_age, max_age, range_age,  distinct_ages,  ignore_iqr, modal_iqr



def process_postcode_age(pc, data, INPUT_GPK):
    """Process one postcode, deriving building attributes and electricity and fuel info."""
   
    uprn_match = find_data_pc(pc, data, input_gpk=INPUT_GPK)
    
    # Generate building metrics, clean and test
    df  = pre_process_buildings(uprn_match)    
    if df is not None:
        if check_duplicate_primary_key(df, 'upn'):
            raise Exception('Duplicate primary key found for upn')
    
    df = bucket_age(df)
    count_unknown = df[df['premise_age_bucketed']=='Unknown date'].shape[0]


    dc_full = {'postcode': pc, 'count_unknown_age': count_unknown  } 
    cols = [ 'ignorefill_median_age', 'modalfill_median_age', 'modal_age', 'min_age', 'max_age', 'range_age', 'distinct_ages', 'ignorefill_iqr_age', 'modalfill_iqr_age']
    
    dicc= {} 
    dc = calc_age_attributes(df)
    for i, col in enumerate(cols ) :
        dicc[col] = dc[i]

    dc_full.update(dicc )
            
    return dc_full 


 