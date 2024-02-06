import pandas as pd 
import glob 
from src import merge_files_together , create_vstreet_lookup
import os 
import argparse 


vstreet_lookup = create_vstreet_lookup()    
def main(gas_elec, fuel_year):
    
    outfile = f'/Users/gracecolverd/New_dataset/data/4_post_process/{fuel_year}/{gas_elec}/merged_non_filtered_use'
    os.makedirs(os.path.dirname(outfile), exist_ok=True)   
    if not os.path.isfile(outfile+'_no_vstreet.csv'):
        files = glob.glob(f'/Users/gracecolverd/New_dataset/data/3_processed/{fuel_year}/non_filtered_use/{gas_elec}/{gas_elec}*.csv') 
        final_df = merge_files_together(files)
        final_df.to_csv(outfile+ '.csv') 
        final_df = final_df[~final_df['Postcode'].isin(vstreet_lookup['Postcode'])].copy()   
        final_df.to_csv(outfile+'_no_vstreet.csv') 

    outfile = f'/Users/gracecolverd/New_dataset/data/4_post_process/{fuel_year}/{gas_elec}/merged_filtered_use'
    os.makedirs(os.path.dirname(outfile), exist_ok=True)    

    if not os.path.isfile(outfile+'_no_vstreet.csv'):
        files = glob.glob(f'/Users/gracecolverd/New_dataset/data/3_processed/{fuel_year}/filtered_use/{gas_elec}/{gas_elec}*.csv') 
        final_df = merge_files_together(files)
        final_df.to_csv(outfile+'.csv')
        final_df = final_df[~final_df['Postcode'].isin(vstreet_lookup['Postcode'])].copy()   
        final_df.to_csv(outfile+'_no_vstreet.csv')   


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post process fuel data')
    parser.add_argument('--gas_elec', type=str, help='gas or elec')
    parser.add_argument('--fuel_year', type=int, help='Year of fuel data')
    args = parser.parse_args()
    main(args.gas_elec, fuel_year=args.fuel_year)


