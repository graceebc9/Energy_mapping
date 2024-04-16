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
    
    









def create_global_heights(bbox_list, input_gpk, output_path):
    # Initialize a dictionary to store intermediate results
    intermediate_dict = {'map_simple_use': [], 'premise_age': [], 'premise_floor_count': [], 'mean_height': [], 'count': [], 'weighted_height': []}

    for bbox in bbox_list:
        print('Processing bounding box:', bbox)
        subset = gpd.read_file(input_gpk, bbox=bbox)
        if subset.empty:
            print('Empty subset for bounding box:', bbox)
            continue

        # Calculate both mean height and count in one go and add weighted_height calculation
        stats = subset.groupby(['map_simple_use', 'premise_age', 'premise_floor_count'])['height'].agg(mean_height='mean', count='size').reset_index()
        stats['weighted_height'] = stats['mean_height'] * stats['count']
        
        # Store the results in the dictionary
        for col in intermediate_dict.keys():
            intermediate_dict[col].extend(stats[col].tolist())

    # Convert the dictionary to a DataFrame
    intermediate_df = pd.DataFrame(intermediate_dict)

    # Calculate total counts and sum of weighted heights for each group across all subsets
    total_stats = intermediate_df.groupby(['map_simple_use', 'premise_age', 'premise_floor_count']).agg(
        total_count=('count', 'sum'),
        sum_weighted_height=('weighted_height', 'sum')).reset_index()
    
    # Calculate weighted mean height for each group
    total_stats['weighted_mean'] = total_stats['sum_weighted_height'] / total_stats['total_count']

    # Cleanup before returning
    total_stats = total_stats.drop(columns=['total_count', 'sum_weighted_height'])
    total_stats = total_stats.rename(columns={'weighted_mean': 'global_average_height'})

    # Save the result to CSV
    total_stats.to_csv(f'{output_path}_global_average_heights.csv', index=False)
    print('File saved')
    


def create_global_average_floor_height(bbox_list, input_gpk, output_path):
    # Initialize a dictionary to store intermediate results
    intermediate_dict = {'map_simple_use': [], 'premise_age': [], 'height_bucket': [], 'mean_fc': [], 'count': [], 'weighted_fc': []}

    for bbox in bbox_list:
        print('Processing bounding box:', bbox)
        subset = gpd.read_file(input_gpk, bbox=bbox)
        if subset.empty:
            print('Empty subset for bounding box:', bbox)
            continue

        # Calculate both mean height and count in one go and add weighted_height calculation
        stats = subset.groupby(['map_simple_use', 'premise_age', 'premise_floor_count'])['height'].agg(mean_height='mean', count='size').reset_index()
        stats['weighted_height'] = stats['mean_height'] * stats['count']
        
        # Store the results in the dictionary
        for col in intermediate_dict.keys():
            intermediate_dict[col].extend(stats[col].tolist())

    # Convert the dictionary to a DataFrame
    intermediate_df = pd.DataFrame(intermediate_dict)

    # Calculate total counts and sum of weighted heights for each group across all subsets
    total_stats = intermediate_df.groupby(['map_simple_use', 'premise_age', 'premise_floor_count']).agg(
        total_count=('count', 'sum'),
        sum_weighted_height=('weighted_height', 'sum')).reset_index()
    
    # Calculate weighted mean height for each group
    total_stats['weighted_mean'] = total_stats['sum_weighted_height'] / total_stats['total_count']

    # Cleanup before returning
    total_stats = total_stats.drop(columns=['total_count', 'sum_weighted_height'])
    total_stats = total_stats.rename(columns={'weighted_mean': 'global_average_height'})

    # Save the result to CSV
    total_stats.to_csv(f'{output_path}_global_average_heights.csv', index=False)
    print('File saved')