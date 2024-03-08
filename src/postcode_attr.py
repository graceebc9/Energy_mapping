import numpy as np 
import pandas as pd 
import geopandas as gpd 
import os 
from shapely.geometry import box 
from src import check_merge_files

def find_postcode_for_ONSUD_file(path_to_onsud_file, path_to_pc_shp_folder='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'):
    ee = pd.read_csv(path_to_onsud_file)
    ee['leading_letter'] = ee['PCDS'].str.extract(r'^([A-Za-z]{1,2})\d')
    ee= ee[~ee['PCDS'].isna() ] 
    ee['PCDS'] = ee['PCDS'].str.strip()
    
    whole_pc = [] 
    for pc in ee['leading_letter'].unique():
        if len(pc)==1:
            pc_path =os.path.join(path_to_pc_shp_folder,  f'one_letter_pc_code/{pc}/{pc}.shp'  )
            pc_shp = gpd.read_file(pc_path)    
        else:
            pc_path =os.path.join(path_to_pc_shp_folder,  f'two_letter_pc_code/{pc}.shp' ) 
            pc_shp = gpd.read_file(pc_path)    
        whole_pc.append(pc_shp)

    pc_df = pd.concat(whole_pc)
    pc_df['POSTCODE'] = pc_df['POSTCODE'].str.strip() 

    if len(pc_df.PC_AREA.unique().tolist()) != len(ee['leading_letter'].unique().tolist()):
        raise ValueError('Not all postcodes are present in the shapefile') 
    
    check_merge_files(pc_df, ee, 'POSTCODE', 'PCDS') 
    data = ee.merge(pc_df, left_on='PCDS', right_on='POSTCODE', how='inner')

    print('Len of missing rows ', len(data[data['PC_AREA'].isna()] ) ) 
    
    if len(data[data['PC_AREA'].isna()] ) > 0.1*len(data):
        raise ValueError('More than 10% of the data is missing')    
    return pc_df , data 


def find_data_pc(pc, data, input_gpk='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg'):
    gd = gpd.GeoDataFrame(data[data['PCDS'] == pc], geometry='geometry')
    bbox = box(*gd.total_bounds)
    buildings = gpd.read_file(input_gpk, bbox=bbox)
    uprn_match = buildings[buildings['uprn'].isin(gd['UPRN'])]
    return uprn_match


def calc_med_attr(df, col):
    """ Fn to calculate the median of a column for set of data and postcodes 
    """
    modal = calculate_median_age_band(df, modal_ignore = 'modal')
    ignore = calculate_median_age_band(df, modal_ignore = 'ignore')
    if modal != ignore:
        print('Modal and ignore are different')
        return 'Unknown dates causing sway'
    return modal

def calculate_median_age_band(df, modal_ignore = 'modal'):
    """
    Calculate the median of a categorical column based on a specified ordering.

    Parameters:
    - df: pandas DataFrame containing the data.
    - modal_ignore: str, whether to use the modal value for unknown dates ('modal') or ignore unknown dates ('ignore').

    Returns:
    - The category that represents the median.
    """
    category_order = [  'Pre 1919',
                        '1919-1944',
                        '1945-1959', 
                        '1960-1979',
                        '1980-1989',
                        '1990-1999',
                        'Post 1999' 
                        ]
    category_to_ordinal = {category: i for i, category in enumerate(category_order)}

    
    if len(df[df['premise_age'] =='Unknown date'] ) / len(df) * 100  > 10:
        # print('More than 10% of the data is missing premise age')
        return 'Too many unknown ages'
# alll variables pre 1919 updated to be one variable 
    df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age'])
    
    if modal_ignore == 'modal': 
        df['premise_age_bucketed'] = df['premise_age_bucketed'].replace('Unknown date', df['premise_age_bucketed'].mode()[0])    
    elif modal_ignore =='ignore':
        df = df[df['premise_age_bucketed']!='Unknown date']  
    
    # Replace categories with their ordinal numbers
    ordinal_values = df['premise_age_bucketed'].map(category_to_ordinal)
    
    # Calculate the median of these ordinal values
    median_ordinal = ordinal_values.median()
    
    # Find the category corresponding to the median ordinal value
    # Use np.round() to handle cases where the median is between two categories
    median_category = category_order[int(np.round(median_ordinal))]
    
    return median_category


def calculate_modal_age_band(df, col ):
    if len(df[df['premise_age'] =='Unknown date'] ) / len(df) * 100  > 10:
            print('More than 10% of the data is missing premise age')
            return 'Too many unknown ages'
    # alll variables pre 1919 updated to be one variable 
    df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age'])

    df = df[df['premise_age_bucketed']!='Unknown date']  
    mode = df['premimse_age_bucketed'].mode()[0]
    return  mode 
    


# def process_data_improved(data, attribute, attr_function, attr_col=None, base_dir='/Users/gracecolverd/New_dataset', input_gpk='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg', checkpoint_interval=100):
#     """
#     Process data to calculate a specified attribute for each postcode.
#     Inputs: 
#     - data: pandas DataFrame containing the data (this is the ONSUD UPRN PC file matched with postcode shapefiles, calcualted in fn find_postcode_for_ONSUD_file)
#     - attribute: str, the name of the attribute to calculate (used to name attr and output file)
#     - attr_function: function, the function to calculate the attribute from the data.
#     - attr_col: str, the name of the column in the data to be input into attr_function 
#     - base_dir: str, the base directory for the directory 
#     - input_gpk: str, the path to the GeoPackage containing the building data. 
#     """
#     # Initialize result and log DataFrames
#     pc_list = data['PCDS'].unique()

#     output_folder = os.path.join(base_dir, f'data/postcode_attributes/{attribute}' )
#     os.makedirs(output_folder, exist_ok=True)
#     # check if log file already exists 
#     log_path = os.path.join(output_folder, f'{attribute}_process_log.csv' ) 
#     checkpoint_path = os.path.join(output_folder, f'{attribute}_checkpoint.csv') 

#     if os.path.exists(log_path):
#         print('Resuming process')
#         log_df = pd.read_csv(log_path)
#         results_df = pd.read_csv(checkpoint_path)
        
#     else:
#         print('Starting new process')
#         log_df = pd.DataFrame(columns=['Postcode', 'Status', 'Details'])
#         results_df = pd.DataFrame(index=pc_list, columns=[attribute])


#     # Process data
#     for idx, pc in enumerate(pc_list):
#         # check if postcode already processed 
#         if pc in log_df['Postcode'].tolist():
#             if log_df[log_df['Postcode']==pc]['Status'].unique() == 'Processed':

#                 continue
#         try:
#             uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
#             if uprn_match.empty:
#                 log_df.loc[len(log_df)] = [pc, 'Processed', 'Failure - No buildings found']
#                 continue

#             attr_value = attr_function(uprn_match, attr_col)
#             results_df.loc[pc, attribute] = attr_value
            
#             log_df.loc[len(log_df)] = [pc, 'Processed', 'Success']

#             # Save checkpoint every checkpoint_interval postcodes
#             if (idx + 1) % checkpoint_interval == 0:
#                 results_df.to_csv(checkpoint_path  ) 
#                 log_df.to_csv( log_path, index=False )
#                 print(f'Checkpoint saved at {idx+1} postcodes')

#         except Exception as e:
#             log_df.loc[len(log_df)] = [pc, 'Error', str(e)]

#     # Save final results and log
#     results_df.to_csv(os.path.join(output_folder, f'{attribute}_final_results.csv'),  ) 
#     log_df.to_csv(os.path.join(output_folder, f'{attribute}_process_log_final.csv') , index=False ) 

#     return results_df

import os
import pandas as pd
import concurrent.futures
from functools import partial

def process_postcode(pc, data, attr_function, attr_col, input_gpk):
    """
    Helper function to process a single postcode.
    """
    try:
        uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
        if uprn_match.empty:
            return pc, 'Processed', 'Failure - No buildings found', None

        attr_value = attr_function(uprn_match, attr_col)
        return pc, 'Processed', 'Success', attr_value

    except Exception as e:
        return pc, 'Error', str(e), None

# def process_data_improved(data, attribute, attr_function, attr_col=None, base_dir='/Users/gracecolverd/New_dataset', input_gpk='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg', checkpoint_interval=100, max_workers=20):
#     """
#     Process data to calculate a specified attribute for each postcode using multi-threading.
#     """
#     pc_list = data['PCDS'].unique()

#     output_folder = os.path.join(base_dir, f'data/postcode_attributes/{attribute}')
#     os.makedirs(output_folder, exist_ok=True)
#     log_path = os.path.join(output_folder, f'{attribute}_process_log.csv')
#     checkpoint_path = os.path.join(output_folder, f'{attribute}_checkpoint.csv')

#     if os.path.exists(log_path):
#         print('Resuming process')
#         log_df = pd.read_csv(log_path)
#         results_df = pd.read_csv(checkpoint_path)
#     else:
#         print('Starting new process')
#         log_df = pd.DataFrame(columns=['Postcode', 'Status', 'Details'])
#         results_df = pd.DataFrame(index=pc_list, columns=[attribute]).reset_index()
#         results_df = results_df.rename(columns={'index':'Postcode'})

#     processed_pc = set(log_df['Postcode'].tolist())
#     pc_to_process = [pc for pc in pc_list if pc not in processed_pc]

#     # Define partial function for passing additional arguments
#     process_function = partial(process_postcode, data=data, attr_function=attr_function, attr_col=attr_col, input_gpk=input_gpk)

#     print('Starting multi thread')
#     # Use ThreadPoolExecutor for parallel processing
#     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#         future_to_pc = {executor.submit(process_function, pc): pc for pc in pc_to_process}
#         for future in concurrent.futures.as_completed(future_to_pc):
#             pc, status, details, attr_value = future.result()
#             log_df.loc[len(log_df)] = [pc, status, details]
#             if attr_value is not None:
#                 results_df.loc[pc, attribute] = attr_value

#             # Save checkpoint every checkpoint_interval postcodes
#             if len(log_df) % checkpoint_interval == 0:
#                 results_df.to_csv(checkpoint_path, index = False )
#                 log_df.to_csv(log_path, index=False)
#                 print(f'Checkpoint saved at {len(log_df)} postcodes')

#     # Save final results and log
#     results_df.to_csv(os.path.join(output_folder, f'{attribute}_final_results.csv'))
#     log_df.to_csv(os.path.join(output_folder, f'{attribute}_process_log_final.csv'), index=False)
    
import os
import pandas as pd
import concurrent.futures
from functools import partial

def process_postcode_batch(postcode_batch, data, attr_function, attr_col, input_gpk):
    """
    Process a batch of postcodes and return a list of results.
    """
    batch_results = []
    for pc in postcode_batch:
        try:
            uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
            if uprn_match.empty:
                batch_results.append((pc, 'Processed', 'Failure - No buildings found', None))
            else:
                attr_value = attr_function(uprn_match, attr_col)
                batch_results.append((pc, 'Processed', 'Success', attr_value))
        except Exception as e:
            batch_results.append((pc, 'Error', str(e), None))
    return batch_results

def process_data_improved(data, attribute, attr_function, attr_col=None, base_dir='/Users/gracecolverd/New_dataset', input_gpk='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg', checkpoint_interval=100, max_workers=20, batch_size=10):
    """
    Process data to calculate a specified attribute for each postcode using multi-threading with batch processing.
    """
    pc_list = data['PCDS'].unique()

    output_folder = os.path.join(base_dir, f'data/postcode_attributes/{attribute}')
    os.makedirs(output_folder, exist_ok=True)
    log_path = os.path.join(output_folder, f'{attribute}_process_log.csv')
    checkpoint_path = os.path.join(output_folder, f'{attribute}_checkpoint.csv')

    if os.path.exists(log_path):
        print('Resuming process')
        log_df = pd.read_csv(log_path)
        results_df = pd.read_csv(checkpoint_path)
    else:
        print('Starting new process')
        log_df = pd.DataFrame(columns=['Postcode', 'Status', 'Details'])
        results_df = pd.DataFrame(columns=['Postcode', attribute])
        processed_pc = set()

    pc_to_process = [pc for pc in pc_list if pc not in processed_pc]
    postcode_batches = [pc_to_process[i:i + batch_size] for i in range(0, len(pc_to_process), batch_size)]

    process_function = partial(process_postcode_batch, data=data, attr_function=attr_function, attr_col=attr_col, input_gpk=input_gpk)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_batch = {executor.submit(process_function, batch): batch for batch in postcode_batches}
        for future in concurrent.futures.as_completed(future_to_batch):
            batch_results = future.result()
            for pc, status, details, attr_value in batch_results:
                log_df = pd.concat([log_df, pd.DataFrame([[pc, status, details]], columns=log_df.columns)], ignore_index=True)
                if attr_value is not None:
                    results_df = pd.concat([results_df, pd.DataFrame([[pc, attr_value]], columns=results_df.columns)], ignore_index=True)
                
            if len(log_df) % checkpoint_interval < batch_size:  # Adjust for batch size
                results_df.to_csv(checkpoint_path, index=False)
                log_df.to_csv(log_path, index=False)
                print(f'Checkpoint saved at {len(log_df)} postcodes')

    results_df.to_csv(os.path.join(output_folder, f'{attribute}_final_results.csv'), index=False)
    log_df.to_csv(os.path.join(output_folder, f'{attribute}_process_log_final.csv'), index=False)

    return results_df
