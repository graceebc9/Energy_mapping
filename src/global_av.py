import geopandas as gpd
import pandas as pd
from scipy.stats import mode

def compute_global_modal_age(bbox_list, input_gpk, output_PATH):
    # Function to find the modal premise age for each premise_type
    def find_modal_ages(df):
        # Group by 'premise_use', 'premise_type' and find the index of the maximum 'verisk_building_id' for each group
        idx = df.groupby(['premise_use', 'premise_type'])['count'].idxmax()
        
        # Use the index to select the rows corresponding to the modal ages
        modes_df = df.loc[idx].reset_index(drop=True)
        
        # Select only the columns of interest
        modes_df = modes_df[['premise_use', 'premise_type', 'premise_age', 'count']]

        return modes_df

    def get_age_counts(df):
        data = df[( df['premise_use']=='Residential') &(  df['premise_age']!='Unknown date')].copy() 
        return data.groupby(['premise_use', 'premise_type', 'premise_age']).size().reset_index().rename(columns={0:'count'})
    
    # Dictionary to accumulate ages for each group
    age_data = {'premise_use':[], 'premise_type': [], 'premise_age': [], 	'count': [] } 

    for bbox in bbox_list:
   
        # Read subset within the current bbox
        subset = gpd.read_file(input_gpk, bbox=bbox)
        # Filter out 'Unknown date'
        subset = subset[(subset['premise_age'] != 'Unknown date') & (subset['premise_use']=='Residential')]

        # Skip empty subsets
        if subset.empty:
            continue
        print('Calc subset')
        subset = get_age_counts(subset)
        for col in age_data.keys():
            age_data[col].extend(subset[col].tolist())   

    print('Starting union')
    age_df = pd.DataFrame(age_data)
    age_df= age_df.groupby(['premise_use', 'premise_type', 'premise_age']).sum('count').reset_index()
    age_df.to_csv(f'{output_PATH}/age_df_raw.csv', index=False)
    
    age_df = find_modal_ages(age_df)
    age_df.to_csv(f'{output_PATH}/age_df_mode.csv', index=False)
    
    


