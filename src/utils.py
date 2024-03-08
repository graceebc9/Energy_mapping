import pandas as pd
import glob 
import os  

def join_pc_map_three_pc(df, df_col,  pc_map  ):
    # merge on any one of three columns in pc_map 
    final_d = [] 
    for col in ['pcd7', 'pcd8', 'pcds']:
        d = df.merge(pc_map , right_on = col, left_on = df_col  )
        final_d.append(d)
    # Concatenate the results
    merged_final = pd.concat(final_d ).drop_duplicates()
    
    if len(df) != len(merged_final):
        print('Warning: some postcodes not matched')
    return merged_final 


def join_pc_map_three_pc_two(df, df_col1, dfcol2,  pc_map  ):
    # merge on any one of three columns in pc_map 
    final_d = [] 
    for col in ['pcd7', 'pcd8', 'pcds']:
        for dcol in [df_col1, dfcol2]:
            d = pc_map.merge(df, left_on = col, right_on = dcol  )
            final_d.append(d)

    print('starting merge') 
    # Concatenate the results
    merged_final = pd.concat(final_d ).drop_duplicates()
    
    if len(df) != len(merged_final):
        print('Warning: some postcodes not matched')
    return merged_final 


def process_uprn_df(uprn_df):
    # remove trailing space pcds 
    uprn_df['pcds_2'] = uprn_df['PCDS'].str.strip()
    # Check for non-numeric values in the 'UPRN' column
    non_numeric = pd.to_numeric(uprn_df['UPRN'], errors='coerce').isna()
    if non_numeric.any():
        print("Non-numeric values found in 'UPRN' column. These rows will be dropped.")
        # checek how many rows to be dropped 
        if len(uprn_df[non_numeric]) > 1000:
            print('Warning: more than 1000 rows will be dropped')
            raise ValueError('Too many rows to drop')
        # Optionally, handle these rows: drop, fill, etc.
        uprn_df = uprn_df[~non_numeric]
    # Now convert the 'UPRN' column to integers
    uprn_df['UPRN'] = uprn_df['UPRN'].astype(int)
    return uprn_df 


def create_vstreet_lookup(postcode_shapefile_path):
    if os.path.isfile('data/mappings/vstreet_lookup.csv'):
        print('Vstreet lookup exists')
        vstreet_lookup = pd.read_csv('data/mappings/vstreet_lookup.csv')
    else:
        fin = [] 
        for file in glob.glob(postcode_shapefile_path):
            df = pd.read_csv(file, header=None)
            fin.append(df)
        vstreet_lookup = pd.concat(fin) 
        vstreet_lookup['Postcode'] = vstreet_lookup[0].str.strip() 
        vstreet_lookup.to_csv('data/mappings/vstreet_lookup.csv')
        print('lookup saved') 
    return vstreet_lookup



def merge_files_together(folder_glob):

    final = [] 
    for f in folder_glob:
        df = pd.read_csv(f)
        final.append(df)
    final_df = pd.concat(final)
    return final_df


def check_merge_files(df1, df2, col1, col2):
    # Check if the files are empty
    if df1.empty or df2.empty:
        print("Error: One or both files are empty.")
        return False
    
    # Check if the columns to be merged on exist
    if col1 not in df1.columns or col2 not in df2.columns:
        print("Error: One or both columns to be merged on do not exist.")
        return False
    # Check columns are same type 
    if df1[col1].dtype != df2[col2].dtype:
        print('Warning: columns not same type')
    # If one column int, convert toher to int
    
    return True 