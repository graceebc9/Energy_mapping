import pandas as pd
import os
import glob
import concurrent.futures
# Removed unused import statement
import os 
import argparse
from src.utils import check_merge_files, join_pc_map_three_pc_two, join_pc_map_three_pc

# def check_merge_files(df1, df2, col1, col2):
#     # Check if the files are empty
#     if df1.empty or df2.empty:
#         print("Error: One or both files are empty.")
#         return False
    
#     # Check if the columns to be merged on exist
#     if col1 not in df1.columns or col2 not in df2.columns:
#         print("Error: One or both columns to be merged on do not exist.")
#         return False
    
#     return True


# def join_pc_map_three_pc(df, df_col,  pc_map  ):
#     # merge on any one of three columns in pc_map 
#     final_d = [] 
#     for col in ['pcd7', 'pcd8', 'pcds']:
        
#         d = pc_map.merge(df, left_on = col, right_on = df_col  )
#         final_d.append(d)

    
#     print('starting merge') 
#     # Concatenate the results
#     merged_final = pd.concat(final_d ).drop_duplicates()
    
#     if len(df) != len(merged_final):
#         print('Warning: some postcodes not matched')
#     return merged_final 


# def join_pc_map_three_pc_two(df, df_col1, dfcol2,  pc_map  ):
#     # merge on any one of three columns in pc_map 
#     final_d = [] 
#     for col in ['pcd7', 'pcd8', 'pcds']:
#         for dcol in [df_col1, dfcol2]:
            
#             d = pc_map.merge(df, left_on = col, right_on = dcol  )
#             final_d.append(d)
#     # Concatenate the results
#     merged_final = pd.concat(final_d ).drop_duplicates()
    
#     if len(df) != len(merged_final):
#         print('Warning: some postcodes not matched')
#     return merged_final 

def process_uprn_df(uprn_df):
    print('Starting to format uprn')
    uprn_df['pcds_2'] = uprn_df['PCDS'].str.strip()
    # Check for non-numeric values in the 'UPRN' column
    non_numeric = pd.to_numeric(uprn_df['UPRN'], errors='coerce').isna()
    if non_numeric.any():
        print("Non-numeric values found in 'UPRN' column. These rows will be dropped.")
        # checek how many rows to be dropped 
        if len(uprn_df[non_numeric]) > 1000:
            print(len(uprn_df[non_numeric]))
            print('Warning: more than 1000 rows will be dropped')
            raise ValueError('Too many rows to drop')
        # Optionally, handle these rows: drop, fill, etc.
        uprn_df = uprn_df[~non_numeric]
    # Now convert the 'UPRN' column to integers
    uprn_df['UPRN'] = uprn_df['UPRN'].astype(int)
    print('Process uprn complete')
    return uprn_df 


def merge_save_fuel_link_uprn(lab, uprn_df, link, raw_fuel_pc_lk, out_file):
    print('Starting merge and save for', lab)   
    if uprn_df['UPRN'].dtype != link['uprn'].dtype:
        print('Warning: postcode columns not same type')
    if not check_merge_files(uprn_df, link, 'UPRN', 'uprn'): 
        raise ValueError('Merge files error')
    uprn_df_link = uprn_df.merge(link, left_on='UPRN', right_on='uprn')
    if len(uprn_df_link) == 0:
        raise ValueError('No overlapping data for uprn and link file ', lab)
    elec_df_uprn = join_pc_map_three_pc_two(uprn_df_link, 'PCDS', 'pcds_2', raw_fuel_pc_lk)
    if len(elec_df_uprn) == 0:
        raise ValueError('No overlapping data for uprn and elec file ', lab)
    print('Starting ONS output save')
    print(out_file)
    if len(elec_df_uprn) == 0:
        raise ValueError('No data for', lab)
    try:
        elec_df_uprn.to_csv(out_file)
    except Exception as e:
        print(f'Error: Could not save file. {e}')
    print('Complete file saved for', lab)

def process_ons_file(ons_file, link, raw_fuel_pc_lk, gas_elec, fuel_year):
    lab = ons_file.split('_')[-1].split('.')[0]
    print('Starting to process ONS file ', lab)

    out_dir = f'data/fuel_{fuel_year}/{gas_elec}_link'
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        print(f'Error: Could not create directory. {e}')
    out_file = os.path.join(out_dir, f'{fuel_year}_{gas_elec}_uprn_link_{lab}.csv')
    if os.path.isfile(out_file):
        print('ONS processed file already exists, exiting')
        return None
    uprn_df = pd.read_csv(ons_file)
    uprn_df = process_uprn_df(uprn_df)
    merge_save_fuel_link_uprn(lab, uprn_df, link, raw_fuel_pc_lk, out_file)
    
    


def main(gas_elec, raw_elec, raw_gas, pc_map, link, lk, onsud, fuel_year ):

    raw_elec = pd.read_csv(raw_elec) 
    link = pd.read_csv(link)
    pc_map = pd.read_csv(pc_map, encoding = 'latin-1')
    lk = pd.read_csv(lk)
    raw_gas = pd.read_csv(raw_gas)

    os.makedirs(f'data/mappings/fuel_{fuel_year}', exist_ok=True)   
    if gas_elec =='gas':
        print('STARTING GAS')
        gas_file = f'data/mappings/fuel_{fuel_year}/raw_gas21_pc_map21_region21.csv'
        if os.path.isfile(gas_file):
            print('Gas mapping to region exists')
            raw_fuel_pc_lk = pd.read_csv(gas_file) 
        else:
            print('Generating gas mapping to region ')
            raw_gas_pc = join_pc_map_three_pc(raw_gas, 'Postcode',  pc_map)
            if len(raw_gas_pc) == 0:
                raise ValueError('No gas data')
            if len(lk) == 0:
                raise ValueError('No lookup data')
            if 'lsoa21cd' not in raw_gas_pc.columns:
                raise ValueError('No lsoa21cd column in gas data')
            if 'LSOA21CD' not in lk.columns:
                raise ValueError('No LSOA21CD column in lookup data')
            raw_fuel_pc_lk = raw_gas_pc.merge(lk, left_on = 'lsoa21cd', right_on = 'LSOA21CD' , how='left' ) 
            raw_fuel_pc_lk.to_csv(gas_file)

    elif gas_elec=='elec':
        elec_file = f'data/mappings/fuel_{fuel_year}/raw_elec21_pc_map21_region21.csv'
        if os.path.isfile(elec_file) :
            print('Elec mapping to region exists')
            raw_fuel_pc_lk = pd.read_csv(elec_file)
        else:
            print('generating elec mapping to region ')
            raw_elec_pc = join_pc_map_three_pc(raw_elec, 'Postcode',  pc_map)
            raw_fuel_pc_lk = raw_elec_pc.merge(lk, left_on = 'lsoa21cd', right_on = 'LSOA21CD' , how='left' ) 
            raw_fuel_pc_lk.to_csv(elec_file) 

    files = glob.glob(os.path.join(onsud, '*.csv'))
    
    if len(files) != 11:
           raise ValueError('Not all ONSUD files present')
        
    with concurrent.futures.ThreadPoolExecutor(max_workers = 1) as executor:
        futures = [executor.submit(process_ons_file, ons_file, link, raw_fuel_pc_lk, gas_elec, fuel_year) for ons_file in files]

    # Wait for all threads to complete
    concurrent.futures.wait(futures)
    print("All files processed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('--gas_elec', type=str, required=True, help='Gas or Electric')
    parser.add_argument('--raw_elec', type=str, required=True, help='Path to raw electricity data')
    parser.add_argument('--raw_gas', type=str, required=True, help='Path to raw gas data')
    parser.add_argument('--pc_map', type=str, required=True, help='Path to postcode mapping')
    parser.add_argument('--link', type=str, required=True, help='Path to link file')
    parser.add_argument('--lk', type=str, required=True, help='Path to lookup file')
    parser.add_argument('--onsud', type=str, required=True, help='Path to ONSUD data')
    parser.add_argument('--fuel_year', type=int, required=True, help='Year of fuel data')

    
    args = parser.parse_args()
    main(gas_elec=args.gas_elec, raw_elec= args.raw_elec, raw_gas=args.raw_gas, pc_map=args.pc_map, link=args.link, lk=args.lk, onsud=args.onsud  , fuel_year=args.fuel_year  )