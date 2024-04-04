import os 
import pandas as pd
import geopandas as gpd
from shapely.geometry import box 
from src.multi_thread import merge_temp_logs_to_main, generate_batch_list
from src.utils  import check_merge_files 


def find_data_pc(pc, data, input_gpk):
    """
    Find buildings based on UPRN match to the postcodes 
    """
    gd = gpd.GeoDataFrame(data[data['PCDS'] == pc].copy(), geometry='geometry')
    
    bbox = box(*gd.total_bounds)
    buildings = gpd.read_file(input_gpk, bbox=bbox)
    uprn_match = buildings[buildings['uprn'].isin(gd['UPRN'])].copy()
    return uprn_match




def check_duplicate_primary_key(df, primary_key_column):
    # print('checking dupes')
    is_duplicate = df[primary_key_column].duplicated().any()
    return is_duplicate



def load_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        ids = file.read().splitlines()
    return ids

def get_onsud_path(onsud_dir, onsud_data  ,label ):

    # DATA_DIR='/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022'
    # date = onsud_dir.split('/')[-1].split('ONSUD_')[-1]
    filepath = os.path.join(onsud_dir, f'Data/ONSUD_{onsud_data}_{label}.csv' ) 
    return filepath

def get_onsud_path_batches(onsud_dir, onsud_data  ,label ):

    
    
    filepath = os.path.join(onsud_dir, f'Data/ONSUD_{onsud_data}_{label}.csv' ) 
    return filepath



def load_onsud_data(path_to_onsud_file, path_to_pcshp, ):
    if path_to_onsud_file is None: 
        return None 
    label = path_to_onsud_file.split('/')[-1].split('.')[0].split('_')[-1]
    print(f'Finding data for ONSUD file ', label )
    onsud_df = pd.read_csv(path_to_onsud_file)
    _  , onsud_data = find_postcode_for_ONSUD_file(onsud_file= onsud_df, path_to_pc_shp_folder= path_to_pcshp)

    return onsud_data 

def get_pcs_to_process(onsud_data, log):
    pcs_list =  onsud_data.PCDS.unique().tolist()
    merge_temp_logs_to_main(log)
    pc_list = generate_batch_list(pcs_list, log , 'postcode')
    return pc_list 
    

def find_postcode_for_ONSUD_file(onsud_file, path_to_pc_shp_folder):
    """ Join ONSUD UPRN TO postcode mapping to postcode geofiles with shapefiles
    onsud file is raw onsud file
    """
    onsud_file['leading_letter'] = onsud_file['PCDS'].str.extract(r'^([A-Za-z]{1,2})\d')
    onsud_file= onsud_file[~onsud_file['PCDS'].isna() ] 
    onsud_file['PCDS'] = onsud_file['PCDS'].str.strip()
    
    whole_pc = [] 
    for pc in onsud_file['leading_letter'].unique():
        pc= pc.lower()
        if len(pc)==1:
            pc_path =os.path.join(path_to_pc_shp_folder,  f'one_letter_pc_code/{pc}/{pc}.shp'  )
            pc_shp = gpd.read_file(pc_path)    
        else:
            pc_path =os.path.join(path_to_pc_shp_folder,  f'two_letter_pc_code/{pc}.shp' ) 
            pc_shp = gpd.read_file(pc_path)    
        whole_pc.append(pc_shp)

    pc_df = pd.concat(whole_pc)
    pc_df['POSTCODE'] = pc_df['POSTCODE'].str.strip() 
      
    if len(pc_df.PC_AREA.unique().tolist()) != len(onsud_file['leading_letter'].unique().tolist()):
        raise ValueError('Not all postcodes are present in the shapefile') 

    check_merge_files(pc_df, onsud_file, 'POSTCODE', 'PCDS') 

    data = onsud_file.merge(pc_df, left_on='PCDS', right_on='POSTCODE', how='inner')
    print(len(data))
    print('Len of missing rows ', len(data[data['PC_AREA'].isna()] ) ) 
    
    if len(data[data['PC_AREA'].isna()] ) > 0.1*len(data):
        raise ValueError('More than 10% of the data is missing')    
    
    return pc_df , data 