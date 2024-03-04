# Imports
import pandas as pd
import glob
import os
import argparse

# Constants
# RAW_GAS_FILES_PATH = '/Volumes/T9/postcode_data/data/raw_gas_link_buildings/*'

# Categories
ALL_CATEGORIES = [
    'AGRICULTURAL - UNCLASSIFIED', 'COMMUNITY - EDUCATIONAL', 'COMMUNITY - EMERGENCY SERVICES',
    'COMMUNITY - GOVERNMENTAL (CENTRAL AND LOCAL)', 'COMMUNITY - HEALTH',
    'COMMUNITY - INSTITUTIONAL AND COMMUNAL ACCOMMODATION', 'COMMUNITY - RELIGIOUS',
    'DEFENCE', 'GENERAL COMMERCIAL - MIXED USE', 'GENERAL COMMERCIAL - MIXED USE - DERELICT',
    'INDUSTRY - MANUFACTURING/PROCESSING', 'OFFICE ONLY', 'OFFICE WITH RETAIL ON GROUND FLOOR',
    'RECREATION AND LEISURE', 'RETAIL - PETROL STATION', 'RETAIL - VACANT/DERELICT',
    'RETAIL - WITH MORE RECENT EXTENSIONS OF DIFFERENT TYPE CONSTRUCTION/AGE', 'RETAIL ONLY',
    'STORAGE/WAREHOUSING', 'STORAGE/WAREHOUSING WITH LINKED OFFICE BLOCK', 'TRANSPORT',
    'UNCLASSIFIED', 'UTILITIES', 'RESIDENTIAL ONLY', 'RESIDENTIAL WITH RETAIL ON GROUND FLOOR',
    'RETAIL WITH OFFICE/RESIDENTIAL ABOVE'
]
RESIDENTIAL = ['RESIDENTIAL ONLY', 'RESIDENTIAL WITH RETAIL ON GROUND FLOOR', 'RETAIL WITH OFFICE/RESIDENTIAL ABOVE']
PURE_RESIDENTIAL = ['RESIDENTIAL ONLY']
COMMERCIAL_INDUSTRY = [
    'DEFENCE', 'GENERAL COMMERCIAL - MIXED USE', 'GENERAL COMMERCIAL - MIXED USE - DERELICT',
    'INDUSTRY - MANUFACTURING/PROCESSING', 'OFFICE ONLY', 'OFFICE WITH RETAIL ON GROUND FLOOR',
    'RECREATION AND LEISURE', 'RETAIL - PETROL STATION', 'RETAIL - VACANT/DERELICT',
    'RETAIL - WITH MORE RECENT EXTENSIONS OF DIFFERENT TYPE CONSTRUCTION/AGE', 'RETAIL ONLY',
    'STORAGE/WAREHOUSING', 'STORAGE/WAREHOUSING WITH LINKED OFFICE BLOCK', 'TRANSPORT', 'UTILITIES'
]
COMMUNITY = [
    'COMMUNITY - EDUCATIONAL', 'COMMUNITY - EMERGENCY SERVICES', 'COMMUNITY - GOVERNMENTAL (CENTRAL AND LOCAL)',
    'COMMUNITY - HEALTH', 'COMMUNITY - INSTITUTIONAL AND COMMUNAL ACCOMMODATION', 'COMMUNITY - RELIGIOUS'
]
UNCLASSIFIED = ['UNCLASSIFIED']
AGRICULTURAL = ['AGRICULTURAL - UNCLASSIFIED']

def read_and_process_gas_files(files_path):
    """Read gas files, process them and return a concatenated DataFrame."""
    final_pivot = []
    gas_files = glob.glob(files_path)
    for gf in gas_files:
        print(gf)
        gas_builds = pd.read_csv(gf).drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y']).drop_duplicates()
        pivot_table = gas_builds.pivot_table(index='Postcode', columns='Use', aggfunc='size', fill_value=0)
        final_pivot.append(pivot_table)
    return pd.concat(final_pivot)

def calculate_percentages(pivot_table):
    """Calculate and append percentage columns to the pivot table."""
    pivot_table['residential_count'] = pivot_table[RESIDENTIAL].sum(axis=1)
    pivot_table['residential_perc'] = pivot_table[RESIDENTIAL].sum(axis=1) / pivot_table[ALL_CATEGORIES].sum(axis=1) * 100
    pivot_table['residential_only_perc'] = pivot_table[PURE_RESIDENTIAL].sum(axis=1) / pivot_table[ALL_CATEGORIES].sum(axis=1) * 100
    pivot_table['commerical_industry_perc'] = pivot_table[COMMERCIAL_INDUSTRY].sum(axis=1) / pivot_table[ALL_CATEGORIES].sum(axis=1) * 100
    pivot_table['community_perc'] = pivot_table[COMMUNITY].sum(axis=1) / pivot_table[ALL_CATEGORIES].sum(axis=1) * 100
    pivot_table['unclassified_perc'] = pivot_table[UNCLASSIFIED].sum(axis=1) / pivot_table[ALL_CATEGORIES].sum(axis=1) * 100
    pivot_table['agricultural_perc'] = pivot_table[AGRICULTURAL].sum(axis=1) / pivot_table[ALL_CATEGORIES].sum(axis=1) * 100

    pivot_table['total_perc'] = pivot_table[['residential_perc', 'commerical_industry_perc', 'community_perc', 'unclassified_perc', 'agricultural_perc']].sum(axis=1)
    pivot_table = pivot_table.round(0)

    if pivot_table[pivot_table['total_perc'] != 100].empty:
        print("Total percentages are correct.")
    else:
        raise ValueError('Total percentage not equal to 100')

    return pivot_table

def main(fuel_path, root_dir, fuel_year, gas_elec, rerun ):

    """Main function to process gas files and generate the final CSV."""
    print('Starting calculation of postcode makeups')
    fuel_folder_path = os.path.join(fuel_path, '*') 
    output_path = os.path.join(root_dir, f'data/mappings/{fuel_year}_{gas_elec}_postcode_makeups.csv' )
    if rerun == True:
        if os.path.isfile(output_path):
            print('Postcode makeup file already exists ile exists')
            return None 
        
    pivot_table = read_and_process_gas_files(fuel_folder_path)
    pivot_table = calculate_percentages(pivot_table)
    pivot_table.to_csv(output_path)
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('--fuel_path', type=str, required=True, help='Path to fuel processed folder')
    parser.add_argument('--gas_elec', type=str, required=True, help='Gas or Electric')
    parser.add_argument('--fuel_year', type=int, required=True, help='Year of fuel data') 
    parser.add_argument('--root_dir', type=str, required=True, help='Working directory')
    parser.add_argument('--rerun', type=bool, required =False, help='if True then re create the postcode makeups')
    args = parser.parse_args()

    main(fuel_path = args.fuel_path, root_dir = args.root_dir, gas_elec = args.elec_gas, rerun = args.rerun)
