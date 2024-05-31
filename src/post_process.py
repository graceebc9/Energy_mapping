import numpy as np 
from src.pre_process_buildings import * 
import pandas as pd 
import os
import glob
import numpy as np
from src.postcode_utils import load_ids_from_file

PERC_RANGE_METERS_UPRN = 20
PERC_UNKNOWN_RES_ALLOWED = 10

pc_excl_ovrlap = load_ids_from_file('/Users/gracecolverd/New_dataset/overlapping_pcs.txt')
pc_excl_ovrlap = [x.strip() for x in pc_excl_ovrlap]

######################### Load from downloaded data ######################### 

# Function to load and process directory log file
def load_proc_dir_log_file(path, ):

    folder = glob.glob(os.path.join(path, '*/*csv'))

    full_dict = []  # Use more descriptive variable names
    
    for file_path in folder:
        
        df = pd.read_csv(file_path)
        df.drop_duplicates(inplace=True )
        
        # region = os.path.basename(os.path.dirname(file_path)) 
        region = file_path.split('/')[-2]
        batch = os.path.basename(file_path).split('_')[0]
        data_len = len(df)
        
        # Dictionary creation simplified
        full_dict.append({
            'path': file_path,
            'region': region,
            'batch': batch,
            'len': data_len,
            'memory': 'norm'
        })
    
    log_df = pd.DataFrame(full_dict)
    return log_df

def load_fromLog(log ):
    fin = [] 
    fin_df=pd.DataFrame()
    for x , region in zip(log.path, log.region):
        
        f= pd.read_csv(x)
        f['region'] = [region  for i in range(len(f)) ]
        # check for dups on postcode
        f.drop_duplicates(inplace=True )

        if f.groupby('postcode').size().max()>1:
            print(x)
            print('dups')
        fin.append(f)
    fin_df = pd.concat(fin)

    data = fin_df[~fin_df['postcode'].isin(pc_excl_ovrlap)].copy() 
    
    return data 


######################### Post process type ######################### 


def validate_and_calculate_percentages_type(df):
    """
    Validates if the sum of counts across building type columns matches 'len_res' for each row.
    Also calculates the percentage contribution of each type to 'len_res'.

    Parameters:
    df (pd.DataFrame): DataFrame containing building counts and a total count 'len_res'.

    Returns:
    pd.DataFrame: Updated DataFrame with percentage columns for each building type.
    """

    # List of building type columns (exclude 'postcode' and 'len_res')
    building_types = df.columns.difference(['postcode', 'len_res', 'region'])
    df['len_res'] = df['len_res'].fillna(0)
    # Calculate the sum of all building types for each row
    df['sum_buildings'] = df[building_types].fillna(0).sum(axis=1)

    # Check if the sum matches 'len_res'
    if not (df['sum_buildings'] == df['len_res']).all():
        print(df[df['sum_buildings'] != df['len_res'] ][['sum_buildings', 'len_res']] ) 
        raise ValueError("Sum of building types does not match 'len_res' for some rows")

    # Calculate percentages for each building type and create new columns
    for column in building_types:
        df[f'{column}_pct'] = (df[column] / df['len_res']) * 100

    # Optionally, you might want to remove the 'sum_buildings' column if it's no longer needed
    df.drop(columns=['sum_buildings'], inplace=True)

    return df

def check_percentage_ranges(df):
    """
    Checks that all percentage values in the DataFrame are between 0 and 100.

    Parameters:
    df (pd.DataFrame): DataFrame with percentage columns.

    Raises:
    ValueError: If any percentage value is not within the range 0 to 100.
    """

    # Identifying columns that likely contain percentage values
    df=df.fillna(0)
    percentage_cols = [col for col in df.columns if '_pct' in col]

    # Check each percentage column for values outside the range 0 to 100
    for col in percentage_cols:
        if not df[col].between(0, 100).all():
            # Optional: Print out or log the problematic entries
            problematic_entries = df[~df[col].between(0, 100)]
            print(f"Problematic entries in column {col}:\n{problematic_entries}")

            raise ValueError(f"Values in column {col} are outside the range 0 to 100")

    print("All percentages are within the acceptable range.")


def call_type_checks(df):
    df=validate_and_calculate_percentages_type(df)

    check_percentage_ranges(df)
    return df 


######################### Post process fuel ######################### 


def test_data(df):
    print('starting testes')
    assert_larger(df , 'all_res_heated_vol_fc_total', 'clean_res_heated_vol_fc_total')
    assert_larger(df , 'all_res_heated_vol_fc_total', 'outb_res_heated_vol_fc_total')
    assert_larger(df , 'total_gas', 'avg_gas')
    assert_larger(df , 'total_elec', 'avg_elec')
    assert_larger(df , 'clean_res_heated_vol_fc_total', 'outb_res_heated_vol_fc_total')
    assert_larger(df , 'all_res_gross_area_total', 'all_res_premise_area_total')
    assert_larger(df , 'clean_res_gross_area_total', 'clean_res_premise_area_total')
    
    if not df[(df['clean_res_total_buildings'] ==df['all_res_total_buildings'] )& ( df[ 'all_res_premise_area_total']!=df['clean_res_premise_area_total']) ].empty:
        raise Exception('Error in sum of res buildings - clean and all not matching when building count same ')
    

    print('test passed')

def validate_vol_per_uprn(df):
    excl = df[df['max_vol_per_uprn']<100][df['diff_gas_meters_uprns_res']>6]
    return  df[~df.index.isin(excl.index)]



def post_proc_new_fuel(df):
    df['outcode'] = df['postcode'].apply(lambda x: str(x).split(' ')[0])
    df['tot'] = df['all_res_total_buildings'].fillna(0) + df['comm_alltypes_count'].fillna(0) + df['mixed_total_buildings'].fillna(0) + df['unknown_alltypes'].fillna(0)


    if not df[df['tot']!=df['all_types_total_buildings'].fillna(0)][['tot', 'all_types_total_buildings']].empty:
        print('Error - count of buildings not adding up')
        raise Exception('Error  - count of builds not adding up')
        

    df['percent_residential'] = df['all_res_total_buildings'] / df['all_types_total_buildings']
    df['max_heated_vol'] = np.maximum(df['clean_res_heated_vol_fc_total'], df['clean_res_heated_vol_h_total'])
    df['min_heated_vol']= np.minimum(df['clean_res_heated_vol_fc_total'], df['clean_res_heated_vol_h_total'])
    df['range_heated_vol'] = np.abs(df['clean_res_heated_vol_fc_total'] - df['clean_res_heated_vol_h_total']) 

    df['min_gas_per_vol'] = df['total_gas'] / df ['max_heated_vol'] 
    df['max_gas_per_vol'] = df['total_gas'] / df ['min_heated_vol'] 

    df['perc_all_res' ]  = df['all_res_total_buildings'] /  df ['all_types_total_buildings']
    df['perc_clean_res'] = df['clean_res_total_buildings'] /  df ['all_types_total_buildings']
    
    ob_cols = [x for x in df.columns if x.startswith('outb') ]

    for c in ob_cols:
        df[c] = df[c].fillna(0)
    # df['outb_res_heated_vol_fc_total'] = df['outb_res_heated_vol_fc_total'].fillna(0)
    # df['outb_res_total_buildings'] = df['outb_res_total_buildings'].fillna(0)
    
    df['perc_all_res_basement'] = df['clean_res_base_floor_total']/  df ['all_types_total_buildings']
    df['perc_all_res_listed'] = df['all_res_listed_bool_total'] / df ['all_types_total_buildings']

    df['max_vol_per_uprn' ] =  df['max_heated_vol'] / df['clean_res_uprn_count_total']
    df['min_vol_per_uprn' ] =  df['min_heated_vol'] / df['clean_res_uprn_count_total']
    df['diff_gas_meters_uprns_res'] = np.abs(df['num_meters_gas'] - df['all_res_uprn_count_total']) / df['num_meters_gas'] * 100 

    clean = df[df['diff_gas_meters_uprns_res']<=40].copy() 
    data = clean[clean['percent_residential']==1].copy() 


    return df, data 


def deal_unknown_res(data):
    """
    Remove those with more than threshold value of unknwon residentails builds
    remove those with more volume of outbiilding than res (should only be a few rows )
    """
    og_len = len(data)
    data['unkn_res'] = data['all_res_total_buildings'] - data['clean_res_total_buildings'] - data['outb_res_total_buildings']
    data['perc_unk_res'] = data['unkn_res'] / data['all_res_total_buildings'] * 100 
    data['perc_unk_res'] = data['perc_unk_res'].fillna(0)
    
    data= data[data['clean_res_heated_vol_fc_total'] > data['outb_res_heated_vol_fc_total'].fillna(0) ] 
    if len(data) / og_len * 100  < 0.9:
        raise Exception('More than 10% filtered out')
    return  data[data['perc_unk_res']< PERC_UNKNOWN_RES_ALLOWED ]


def call_post_process_fuel(df):
    df, data = post_proc_new_fuel(df)
    data=deal_unknown_res(data)

    test_data(data)
    return df, data 