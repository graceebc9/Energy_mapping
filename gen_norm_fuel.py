res_use_types = ['RESIDENTIAL ONLY', 'RETAIL WITH OFFICE/RESIDENTIAL ABOVE', 'RESIDENTIAL WITH RETAIL ON GROUND FLOOR'] 

import geopandas as gpd
import pandas as pd
import glob
import os 
import re
import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
import argparse



def has_duplicates(df, column_name):
    """
    Check if a DataFrame column has any duplicates.

    Parameters:
    - df: pandas DataFrame
    - column_name: str, the name of the column to check for duplicates

    Returns:
    - True if duplicates exist, False otherwise
    """
    return df[column_name].duplicated().any()


def calc_residential_building_volume(row):
    """
    ASSUMPTIONS: one floor = 2.3m ; update with average value or adjust for historic buildings 
    """
    if row['Use'] == 'RESIDENTIAL WITH RETAIL ON GROUND FLOOR':
        if row['Height'] /  2.3 > 1 : 
            new_height = row['Height'] - 2.3 
            vol = new_height * row['Property_Area']
        else:
            vol= 0 
        
    elif row['Use'] == 'RETAIL WITH OFFICE/RESIDENTIAL ABOVE':
        if row['Height'] >  2.3: 
            new_height = row['Height'] - 2.3 
            vol = new_height * row['Property_Area']
        else:
            vol= 0 
        return vol
    elif row['Use'] == 'RESIDENTIAL ONLY':
        return row['Height'] * row['Property_Area']

    else:
        return row['Height'] * row['Property_Area']
    

def calc_building_volume(row):
    return row['Height'] * row['Property_Area']



def calc_postcode_building_residential_volume(df, outfile = None, filter_use=True ):
    """
    Calculate the total volume of residential buildings in each postcode area.
    """
    df = df[['Postcode', 'Unique_Building_Number','Unique_Property_Number', 'Property_Area', 'Building_Area','Mapping_Block_Number',	'Height', 	'Age', 	'Use', 'LSOA21CD', 'LAD22CD_y', 'RGN22CD_x' ]].drop_duplicates()
    if filter_use ==True:
        df=df[df['Use'].isin(res_use_types) ]
    else:
        print('Not filtering use types')
    df['res_b_vol'] = df.apply(calc_residential_building_volume, axis=1)
    df = df.groupby('Postcode').agg({'res_b_vol': [ 'sum']}).reset_index()
    if outfile:
        df.to_csv(outfile)
    return df 

def calc_normalised_elec_per_postcode(df, gas_elec, outfile = None ):
    if gas_elec =='elec':
        elec= pd.read_csv('/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_2021.csv')
    elif gas_elec =='gas':
        elec = pd.read_csv('/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_2021.csv') 

    df = df.merge(elec, left_on = 'Postcode', right_on ='Postcode')

    df[f'norm_total_{gas_elec}_kwh/m^3)'] = df['Total_cons_kwh'] / df['res_b_vol', 'sum']
    if outfile: 
        df.to_csv(outfile)
    
    return df 



# Function to process each file
def process_file(file_path, elec):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            print(f"File {file_path} is empty.")
            return None
        d = df.merge(elec, left_on='Unique_Property_Number', right_on='upn')
        # print(f"Finished processing file: {file_path}")
        return d
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None



def main(gas_elec, filtered, fuel_year, building_file_directory):
    print('Starting to calculate normalised fuel use')
    files = glob.glob(f'data/fuel_{fuel_year}/1_{gas_elec}_link/*.csv')
    if len(files) == 0:
        raise ValueError(f"No files found, check if prior step ran. ")

    labels = [ x.split('/')[-1].split('.')[0].split('_')[-1] for x in files]

    
    for f, label in zip(files, labels):
        if label =='SC' or label == 'SW':
            print(label)
            print('Starting ', label)
            fuel = pd.read_csv(f)
            fuel = fuel.drop(columns=[col for col in fuel.columns if 'Unnamed' in col]).drop_duplicates()
            # elec = elec.drop(columns=['Unnamed: 0']).drop_duplicates()
            if filtered == True: 
                outdir = f'data/fuel_{fuel_year}/2_processed/filtered_use/{gas_elec}'
            elif filtered ==False:
                outdir = f'data/fuel_{fuel_year}/2_processed/non_filtered_use/{gas_elec}'
            os.makedirs(outdir, exist_ok=True)
            outfile = os.path.join(outdir, f'{gas_elec}_norm_{label}.csv' ) 

            if os.path.isfile(outfile):
                print('file exists')
                continue

            # Initialize parameters
            cols = ['Unique_Property_Number', 'Unique_Building_Number', 'Property_Area', 'Building_Area', 'Mapping_Block_Number', 'Height', 'Age', 'Use', 'DATA_LEVEL']
            
            file_paths = [os.path.join(building_file_directory, f) for f in os.listdir(building_file_directory) if f.endswith('.csv')]
            if len(file_paths) == 0:
                raise ValueError(f"No files found in {building_file_directory}")
            print('num of files to loop over ', len(file_paths))

            # Use ThreadPoolExecutor to process files in parallel
            processed_files_count = 0
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_file, file_path, fuel, cols) for file_path in file_paths]

            # Collect results
            print(label , ": Collecting results from processed files...")
            merged = []
            for future in futures:
                result = future.result()
                if result is not None:
                    merged.append(result)
                    processed_files_count += 1

            print(f"Total processed files: {processed_files_count} / {len(file_paths)}")
            
            if not merged:
                print(label, " No files were processed. Exiting.")
                continue

            df = pd.concat(merged)
            print("All files processed. Merging completed.")
            print('len of file: ', len(df))

            df_resb = calc_postcode_building_residential_volume(df, filter_use = filtered )
            df_elec_norm = calc_normalised_elec_per_postcode(df_resb, gas_elec)

            df_elec_norm.to_csv(outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('--gas_elec', type=str, required=True, help='Gas or Electric')
    parser.add_argument('--filtered', type=bool, required=True, help='True or False')
    parser.add_argument('--fuel_year', type=int, required=True, help='Year of fuel data')   
    parser.add_argument('--building_file_directory', type=str, required=True, help='Directory containing building data files')
    args = parser.parse_args()
    main(gas_elec  =  args.gas_elec, filtered = args.filtered, fuel_year = args.fuel_year, building_file_directory = args.building_file_directory)

