import numpy as np 
import pandas as pd 
import geopandas as gpd 
import os 
from shapely.geometry import box 
from src.utils import check_merge_files
import concurrent.futures
from functools import partial

def process_postcode(pc, attr_function, data, input_gpk= '/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg', postcode_area=None  ): 
    # data is hte output from the find postcode for ONSUD file fn 
    
    try:
        uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
        if uprn_match.empty:
            return pc, 'Completed', 'No buildings found'  
        else:
            if postcode_area is not None:
                print('stassrting pc area') 
                attr_value = attr_function(df= uprn_match, pc_area=postcode_area)
            else:
                attr_value = attr_function(df= uprn_match)
            return pc, 'Completed', attr_value 
    except Exception as e:
        print('Error', str(e))
        return pc, 'Error' , str(e)
    

def gen_postcode_areas(data, lab ):
    """
    Generate areas of posstcodes for ONSUD data
    Inputs:
    data: ONSUD data laoded with postcode 
    lab: label for the data (EE etc, ONSUD label)
    base_dir: directory where github located 
    """
    out =  f'data/postcode_attributes/postcode_area'
    os.makedirs(out, exist_ok=True)
    outfile = os.path.join(out, f'{lab}_postcode_area.csv')  
    if os.path.exists(outfile):
        print('File already exists')
        postcodes_geom = pd.read_csv(outfile)   
        return postcodes_geom
    print('starting gen file')
    postcodes_geom = data[['PCDS', 'geometry' ]].drop_duplicates().copy() 
    postcodes_geom['pc_area'] = postcodes_geom['geometry'].apply(lambda x: x.area)  
    postcodes_geom.to_csv(outfile , index=False)
    if len(postcodes_geom)==0:
        raise ValueError('No postcodes found')  
    return  postcodes_geom



def find_postcode_for_ONSUD_file(path_to_onsud_file, path_to_pc_shp_folder='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'):
    """ Join ONSUD UPRN TO postcode mapping to postcode geofiles with shapefiles
    """
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
    """
    Find buildings based on UPRN match to the postcodes 
    """
    gd = gpd.GeoDataFrame(data[data['PCDS'] == pc].copy(), geometry='geometry')
    bbox = box(*gd.total_bounds)
    buildings = gpd.read_file(input_gpk, bbox=bbox)
    uprn_match = buildings[buildings['uprn'].isin(gd['UPRN'])].copy()
    return uprn_match


# def calc_med_attr(df):
#     """ Fn to calculate the median age band of a column for a df 
#     Inputs:
#     --df: dataframe containing only one postcode 
#     """
    
#     modal = calculate_median_age_band(df, modal_ignore = 'modal')
    
#     ignore = calculate_median_age_band(df, modal_ignore = 'ignore')
#     if modal != ignore:
#         return 'Unknown dates causing sway'
#     return modal


# def calculate_median_age_band(df, modal_ignore = 'modal'):
#     """
#     Calculate the median of a categorical column based on a specified ordering.

#     Parameters:
#     - df: pandas DataFrame containing the data.
#     - modal_ignore: str, whether to use the modal value for unknown dates ('modal') or ignore unknown dates ('ignore').

#     Returns:
#     - The category that represents the median.
#     """
#     category_order = [  'Pre 1919',
#                         '1919-1944',
#                         '1945-1959', 
#                         '1960-1979',
#                         '1980-1989',
#                         '1990-1999',
#                         'Post 1999' 
#                         ]
#     category_to_ordinal = {category: i for i, category in enumerate(category_order)}

    
#     if len(df[df['premise_age'] =='Unknown date'] ) / len(df) * 100  > 10:
#         # print('More than 10% of the data is missing premise age')
#         return 'Too many unknown ages'
# # alll variables pre 1919 updated to be one variable 
#     df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age'])
    
#     if modal_ignore == 'modal': 
#         df['premise_age_bucketed'] = df['premise_age_bucketed'].replace('Unknown date', df['premise_age_bucketed'].mode()[0])    
#     elif modal_ignore =='ignore':
#         df = df[df['premise_age_bucketed']!='Unknown date']  
    
#     # Replace categories with their ordinal numbers
#     ordinal_values = df['premise_age_bucketed'].map(category_to_ordinal)
    
#     # Calculate the median of these ordinal values
#     median_ordinal = ordinal_values.median()
    
#     # Find the category corresponding to the median ordinal value
#     # Use np.round() to handle cases where the median is between two categories
#     median_category = category_order[int(np.round(median_ordinal))]
    
#     return median_category


# def calculate_modal_age_band(df ):
#     """ Fn to calculate the modal age band of a column for a df (needs contain all same postcodes)
#     Assumptions: less than 10% unknowns ignore, all varaibles pre 1919 to one variable 
#     """
#     perc_missing = len(df[df['premise_age'] =='Unknown date'] ) / len(df) 
#     if  perc_missing * 100  > 10:
#             return 'Too many unknown ages', perc_missing,  len(df) 
    
#     # alll variables pre 1919 updated to be one variable 
#     df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age'])

#     df = df[df['premise_age_bucketed']!='Unknown date']  
#     mode = df['premise_age_bucketed'].mode()[0]
#     return  mode , perc_missing,  len(df) 
    

############################ Batch Functions  ######################################## 

# # need batch fn in format batch_fn(item, data) where item is postcode 
# def postcode_median_age_batch_fn(pc, data ):
#     results = process_postcode(pc, calc_med_attr, data )
#     return results 


# def postcode_modal_batch_fn(pc, data): 
#     """ returns triple result of modal age, percent missing and num buildings.
#       to be used with result_cols = ['postcode', 'status', 'modal_age_perc_missing_num_buildings'] and then post process
#     """
#     results = process_postcode(pc, calculate_modal_age_band, data) 
#     return results 


########################### Area functions ########################################



# def fill_premise_floor_types_old(uprn):
#     # Ensure 'premise_floor_count' is numeric with NaN for non-numeric values
#     orig_len = len(uprn)
#     uprn['premise_floor_count'] = pd.to_numeric(uprn['premise_floor_count'], errors='coerce')
    
#     # Compute 'av_storey_height' only for non-NaN 'premise_floor_count'
#     valid_data = uprn.dropna(subset=['premise_floor_count'])
#     valid_data['av_storey_height'] = valid_data['height'] / valid_data['premise_floor_count'].astype(int)
    
#     # Calculate mean storey height from valid entries
#     mean_storey_height = valid_data['av_storey_height'].mean()
    
#     # Fill NaN 'premise_floor_count' by dividing 'height' by mean storey height and TAKING FLOOR to ensure never higher that heated vol 
#     uprn['premise_floor_count'].fillna(uprn['height'] / mean_storey_height, inplace=True)
#     uprn['premise_floor_count'] = np.floor(uprn['premise_floor_count']).astype('Int64')
#     if len(uprn)!= orig_len:
#         raise Exception('Fill_premise_floor_types has dropped or increased rows, orig_len: ', orig_len, 'new len: ', len(uprn))
#     return uprn



# def calc_area_vars(df, pc_area):
#     num_buildings = len(df)
#     if num_buildings < 2:
#         return [-999] * 15

#     total_floor_area = df['premise_area'].sum()
#     build_floor_area_per_pc_area = total_floor_area / pc_area
#     num_buildings_per_m2_pc_area = num_buildings / pc_area
    
#     prob_cols = df.columns[df.isna().mean() > 0.15].tolist()
#     # for col in prob_cols:
#         # print(f'Warning: {col} has more than 15% missing values')

#     df = fill_premise_floor_types(df)
    
#     perc_missing_premise_floor_count = df['premise_floor_count'].isna().mean()
#     perc_residential, residential_floor_area = -999, -999
#     if 'premise_use' not in prob_cols:
#         residential_data = df[df['premise_use'] == 'Residential'].copy()
#         perc_residential = len(residential_data) / num_buildings
#         residential_floor_area = residential_data['premise_area'].sum()
    
#     vars_out = calc_vars(df, prob_cols)
#     res_vars_out = calc_vars(df[df['premise_use'] == 'Residential'], prob_cols) if perc_residential != 1 else vars_out

#     df.loc[:, 'listed'] = df['listed_grade'].apply(lambda x: 1 if x is not None else 0)
#     perc_listed_buildings = df['listed'].mean()

#     return [perc_residential, total_floor_area, residential_floor_area, perc_missing_premise_floor_count] + \
#            list(vars_out) + [build_floor_area_per_pc_area, num_buildings_per_m2_pc_area, perc_listed_buildings] + \
#            list(res_vars_out)


# def calc_vars(df, prob_cols):
#     if 'premise_area' in prob_cols or 'height' in prob_cols:
#         return [-999, -999, -999, -999]
#     df['build_vol'] = df['premise_area'] * df['height']
#     total_build_volume = df['build_vol'].sum()
    
#     df['base_floor'] = df['basement'].apply(lambda x: 1 if x in ['Basement confirmed', 'Basement likely'] else 0)
#     total_build_volume_inc_basement = (df['build_vol'] + 2.3 * df['base_floor'] * df['premise_area']).sum()
    
#     if 'premise_floor_count' not in prob_cols and 'basement' not in prob_cols:
#         df['heated_vol'] = df['premise_area'] * df['premise_floor_count'].astype(int) * 2.3
#         df['heated_vol_inc_basement'] = df['heated_vol'] + 2.3 * df['base_floor'] * df['premise_area']
#         total_heated_volume = df['heated_vol'].sum()
#         total_heated_volume_inc_basement = df['heated_vol_inc_basement'].sum()
#     else:
#         return [total_build_volume, total_build_volume_inc_basement, -999, -999]

#     return [total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement]




# def postcode_area_vars_batch_fn(pc, data, area):
#     results = process_postcode(pc= pc, attr_function = calc_area_vars , data = data, postcode_area = area )
#     return results   



# def fill_premise_floor_types(uprn): 
#     if len(uprn[uprn['premise_floor_count'].isna()]) ==0 :
#         return uprn 
#     data = uprn[uprn['premise_floor_count'].notna() ]
#     data['av_storey_hewight'] = data['height'] / data['premise_floor_count'].astype(int)
#     mean_storey_height= data['av_storey_hewight'].mean()

#     # fill null values using mean storey heigh , rounded to nearest int 
#     uprn['premise_floor_count'] = uprn['premise_floor_count'].fillna(  uprn['height'] / mean_storey_height)
#     uprn['premise_floor_count'] = np.round(uprn['premise_floor_count'].astype(float) )
#     return uprn 

# def calc_area_vars(df, pc_area ):
#     """ 
#     """
#     num_buildings = len(df) 
#     if num_buildings <2:
#         return -999, -999, -999, -999, -999, -999, -999, -999, -999 
    
#     total_floor_area = df['premise_area'].sum() 
#     build_floor_area_per_pc_area  = total_floor_area / pc_area 
    
#     num_buildings_per_m2_pc_area = num_buildings / pc_area 
    
    
#     # check missing values 
#     prob_cols = [] 
#     for col in ['premise_use', 'premise_area', 'height', 'premise_floor_count', 'basement']:
#         if len(df[df[col].isna() ]) / len(df) >0.15:
#             print(f'Warning: {col} has more than 15% missing values') 
#             prob_cols.append(col)

#     perc_missing_premise_flood_count = len(df[df['premise_floor_count'].isna()]) / len(df)  
#     df = fill_premise_floor_types(df)

#     if 'premise_use' not in prob_cols:
#         perc_residential = len( df[df['premise_use']=='Residential']) / len(df)
#         residential_floor_area = df[df['premise_use']=='Residential']['premise_area'].sum() 
#     else:
#         perc_residential = -999
#         residential_floor_area = -999

    
#     total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement  = calc_vars(df, prob_cols)
#     if perc_residential != 1: 
#         print('not all res')
#         res =df[df['premise_use']=='Residential'].copy() 
#         res_build_volume, res_build_volume_inc_basement, res_heated_volume, res_heated_volume_inc_basement = calc_vars(res, prob_cols)
#     else:
#         res_build_volume, res_build_volume_inc_basement, res_heated_volume, res_heated_volume_inc_basement = total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement 
    
    
#     df['listed'] = df['listed_grade'].apply(lambda x: 1 if x != None else 0)
#     perc_listed_buildings = df['listed'].sum() / len(df)

#     return perc_residential, total_floor_area, residential_floor_area, perc_missing_premise_flood_count, total_build_volume, total_heated_volume, total_heated_volume_inc_basement, build_floor_area_per_pc_area, num_buildings_per_m2_pc_area, perc_listed_buildings, total_build_volume_inc_basement, res_build_volume, res_build_volume_inc_basement, res_heated_volume, res_heated_volume_inc_basement


# def calc_vars(df, prob_cols):
#     if 'premise_area' not in prob_cols and 'height' not in prob_cols:
#         df['build_vol'] = df['premise_area'] * df['height']  
#         total_build_volume = df['build_vol'].sum()
#         df ['base_floor'] = df['basement'].apply(lambda x: 1 if ((x == 'Basement confirmed') or (x=='Basement likely')) else 0)
#         total_build_vol_inc_basement = (2.3 * df['base_floor'] * df['premise_area']) + df['build_vol']
#         total_build_volume_inc_basement = total_build_vol_inc_basement.sum()
#         if 'premise_floor_count' not in prob_cols and 'basement' not in prob_cols :
#             df['heated_vol'] = df['premise_area'] * df['premise_floor_count'].astype(int) * 2.3
#             df['heated_vol_inc_basement'] = df['premise_area'] * ( (df['premise_floor_count'].astype(int) + df['base_floor'].astype(int)) ) * 2.3
#             total_heated_volume = df['heated_vol'].sum()
#             total_heated_volume_inc_basement = df['heated_vol_inc_basement'].sum()
#         else:
#             total_heated_volume = -999
#             total_heated_volume_inc_basement = -999
#     else:
#         total_build_volume = -999
#         total_heated_volume = -999
#         total_heated_volume_inc_basement = -999
#         total_build_volume_inc_basement = -999
#     return total_build_volume, total_build_volume_inc_basement, total_heated_volume, total_heated_volume_inc_basement 


# def postcode_area_vars_batch_fn(pc, data, area):
#     results = process_postcode(pc= pc, attr_function = calc_area_vars , data = data, postcode_area = area )
#     return results   





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


# def process_postcode(pc, data, attr_function, attr_col, input_gpk):
#     """
#     Helper function to process a single postcode.
#     """
#     try:
#         uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
#         if uprn_match.empty:
#             return pc, 'Processed', 'Failure - No buildings found', None

#         attr_value = attr_function(uprn_match, attr_col)
#         return pc, 'Processed', 'Success', attr_value

#     except Exception as e:
#         return pc, 'Error', str(e), None

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
    


# def process_postcode_batch(postcode_batch, data, attr_function, attr_col, input_gpk):
#     """
#     Process a batch of postcodes and return a list of results.
#     """
    
#     batch_results = []
#     for pc in postcode_batch:
#         try:
#             uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
#             if uprn_match.empty:
#                 batch_results.append((pc, 'Failure - No buildings found', None))
#             else:
#                 attr_value = attr_function(uprn_match, attr_col)
#                 batch_results.append((pc, 'Completed', attr_value))
#         except Exception as e:
#             batch_results.append((pc, str(e), None))
#     return batch_results


# def process_data_improved(data, attribute, attr_function, attr_col=None, base_dir='/Users/gracecolverd/New_dataset', input_gpk='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg', checkpoint_interval=1000, max_workers=10, batch_size=10):
#     pc_list = data['PCDS'].unique()
#     output_folder = os.path.join(base_dir, f'data/postcode_attributes/{attribute}')
#     os.makedirs(output_folder, exist_ok=True)
#     checkpoint_path = os.path.join(output_folder, f'{attribute}_checkpoint.csv')

#     if os.path.exists(checkpoint_path):
#         print('Resuming process')
#         results_df = pd.read_csv(checkpoint_path)
#     else:
#         print('Starting new process')
#         results_df = pd.DataFrame(columns=['Postcode', attribute, 'status'])

#     processed_pc = set(results_df['Postcode'].unique())
#     pc_to_process = [pc for pc in pc_list if pc not in processed_pc]
#     postcode_batches = [pc_to_process[i:i + batch_size] for i in range(0, len(pc_to_process), batch_size)]

#     process_function = partial(process_postcode_batch, data=data, attr_function=attr_function, attr_col=attr_col, input_gpk=input_gpk)

#     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#         for batch in postcode_batches:
#             batch_results = executor.submit(process_function, batch).result()
#             temp_results = pd.DataFrame(batch_results, columns=['Postcode', 'Status', attribute])
#             results_df = pd.concat([results_df, temp_results], ignore_index=True)

#             if len(results_df) % checkpoint_interval < batch_size:
#                 results_df.to_csv(checkpoint_path, index=False)
#                 print(f'Checkpoint saved at {len(results_df)} postcodes')

#     results_df.to_csv(os.path.join(output_folder, f'{attribute}_final_results.csv'), index=False)
#     print('Processing complete.')

#     return results_df


############################################# Confidence fns #############################################


# def process_postcode_batch_confidence(postcode_batch, data, attr_function, attr_col, input_gpk):
#     """
#     Process a batch of postcodes and return a list of results.
#     """
#     batch_results = []
#     for pc in postcode_batch:
#         try:
#             uprn_match = find_data_pc(pc, data, input_gpk=input_gpk)
#             if uprn_match.empty:
#                 batch_results.append((pc, 'Processed', 'Failure - No buildings found', None))
#             else:
#                 attr_value, confidence = attr_function(uprn_match, attr_col)
#                 batch_results.append((pc, 'Processed', 'Success', attr_value, confidence))
#         except Exception as e:
#             batch_results.append((pc, 'Error', str(e), None))
#     return batch_results

# def process_data_improved_confidence(data, attribute, attr_function, conf_attr,  attr_col=None, base_dir='/Users/gracecolverd/New_dataset', input_gpk='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/new_verisk_2022.gpkg', checkpoint_interval=100, max_workers=20, batch_size=10):
#     """
#     Process data to calculate a specified attribute for each postcode using multi-threading with batch processing.
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
#         processed_pc = results_df['Postcode'].tolist() 
        
#     else:
#         print('Starting new process')
#         log_df = pd.DataFrame(columns=['Postcode', 'Status', 'Details'])
#         results_df = pd.DataFrame(columns=['Postcode', attribute, conf_attr])
#         processed_pc = set()

#     pc_to_process = [pc for pc in pc_list if pc not in processed_pc]
#     postcode_batches = [pc_to_process[i:i + batch_size] for i in range(0, len(pc_to_process), batch_size)]

#     process_function = partial(process_postcode_batch, data=data, attr_function=attr_function, conf_attr=conf_attr, attr_col=attr_col, input_gpk=input_gpk)

#     with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
#         future_to_batch = {executor.submit(process_function, batch): batch for batch in postcode_batches}
#         for future in concurrent.futures.as_completed(future_to_batch):
#             batch_results = future.result()
#             for pc, status, details, attr_value, conf_value in batch_results:
#                 log_df = pd.concat([log_df, pd.DataFrame([[pc, status, details]], columns=log_df.columns)], ignore_index=True)
#                 if attr_value is not None:
#                     results_df = pd.concat([results_df, pd.DataFrame([[pc, attr_value, conf_value]], columns=results_df.columns)], ignore_index=True)
                
#             if len(log_df) % checkpoint_interval < batch_size:  # Adjust for batch size
#                 results_df.to_csv(checkpoint_path, index=False)
#                 log_df.to_csv(log_path, index=False)
#                 print(f'Checkpoint saved at {len(log_df)} postcodes')

#     results_df.to_csv(os.path.join(output_folder, f'{attribute}_final_results.csv'), index=False)
#     log_df.to_csv(os.path.join(output_folder, f'{attribute}_process_log_final.csv'), index=False)

#     return results_df
