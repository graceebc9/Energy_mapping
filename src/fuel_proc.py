import concurrent.futures
import pandas as pd
import tempfile
import os
from src.fuel_calc import process_postcode_fuel
import threading
import geopandas as gpd 

thread_local = threading.local()

from src.multi_thread import merge_temp_logs_to_main, generate_batch_list
from src.utils  import check_merge_files 


def find_postcode_for_ONSUD_file(path_to_onsud_file, path_to_pc_shp_folder):
    """ Join ONSUD UPRN TO postcode mapping to postcode geofiles with shapefiles
    """
    ee = pd.read_csv(path_to_onsud_file)
    ee['leading_letter'] = ee['PCDS'].str.extract(r'^([A-Za-z]{1,2})\d')
    ee= ee[~ee['PCDS'].isna() ] 
    ee['PCDS'] = ee['PCDS'].str.strip()
    
    whole_pc = [] 
    for pc in ee['leading_letter'].unique():
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

    if len(pc_df.PC_AREA.unique().tolist()) != len(ee['leading_letter'].unique().tolist()):
        raise ValueError('Not all postcodes are present in the shapefile') 
    
    check_merge_files(pc_df, ee, 'POSTCODE', 'PCDS') 
    data = ee.merge(pc_df, left_on='PCDS', right_on='POSTCODE', how='inner')

    print('Len of missing rows ', len(data[data['PC_AREA'].isna()] ) ) 
    
    if len(data[data['PC_AREA'].isna()] ) > 0.1*len(data):
        raise ValueError('More than 10% of the data is missing')    
    return pc_df , data 


def process_batch(pc_batch, data, gas_df, elec_df, INPUT_GPK, temp_dir):

    log_file = os.path.join(temp_dir, 'log_file.csv' )
    # Collect results from processing each postcode into a list
    results = []
    for pc in pc_batch:
        
        pc_result = process_postcode_fuel(pc, data, gas_df, elec_df, INPUT_GPK)
        results.append(pc_result)
    
    # Only proceed if we have results
    if results:
        df = pd.DataFrame(results)
        
        temp_file_path, is_first_write = get_thread_temp_file(log_file)
        # print('temp file path is ' , temp_file_path )
        # Open the file with 'a' mode to append and ensure headers are written correctly
        with open(temp_file_path, 'a') as f:
            df.to_csv(f, header=is_first_write, index=False)
        
        # Update the flag to indicate the header should not be written next time
        if is_first_write:
            thread_local.temp_file_first_write = False

        # print('temp file saved for batch')

def get_thread_temp_file(log_file):
    if not hasattr(thread_local, 'temp_file'):
        temp_dir = os.path.dirname(log_file)

        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.csv', prefix='temp_log_', dir=temp_dir)        

        thread_local.temp_file = temp_file.name
        thread_local.temp_file_first_write = True
    return thread_local.temp_file, thread_local.temp_file_first_write



def run_fuel_calc(pcs_list, data, gas_df, elec_df, INPUT_GPK, temp_dir, max_workers, batch_size):
    # Ensure temporary directory exists
    os.makedirs(temp_dir, exist_ok=True)
    
    # # Split pcs_list into batches for parallel processing
    # pcs_batches = [pcs_list[i:i+batch_size] for i in range(0, len(pcs_list), batch_size)]


    # with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers) as executor:
    #     futures = [executor.submit(process_batch, batch, data, gas_df, elec_df, temp_dir) for batch in pcs_batches]
    #     for future in concurrent.futures.as_completed(futures):
    #         temp_file_path = future.result()

    with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers ) as executor:
        # Store futures if you need to wait for them or check for exceptions
        futures = []
        for i in range(0, len(pcs_list), batch_size):
            batch = pcs_list[i:i+batch_size]
    
            future= executor.submit(process_batch, batch, data, gas_df, elec_df, INPUT_GPK,  temp_dir )
            futures.append(future)
        concurrent.futures.wait(futures)

        # Check for exceptions in the completed futures
        for future in futures:
            if future.exception() is not None:
                # Handle the exception
                print(f"Exception occurred in thread: {future.exception()}")
            else:
                # Process result if needed (or acknowledge successful completion)
                None 




def load_fuel_data(gas_path, elec_path):
    # gas_path =  f'/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_{fuel_year}.csv' #gas by postcode 
    gas_df = pd.read_csv(gas_path) 

    # elec_path = f'/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_{fuel_year}.csv'
    elec_df = pd.read_csv(elec_path) 

    # log = '/Users/gracecolverd/New_dataset/postcode_attrs/temp_files/log_file.csv' 
    return  gas_df, elec_df


def load_onsud_data(path_to_onsud_file, path_to_pcshp, ):
    
    print(f'Finding data for ONSUD file')
    
    _  , onsud_data = find_postcode_for_ONSUD_file(path_to_onsud_file= path_to_onsud_file, path_to_pc_shp_folder= path_to_pcshp)


    return onsud_data 

def get_pcs_to_process(onsud_data, log):
    pcs_list =  onsud_data.PCDS.unique().tolist()
    merge_temp_logs_to_main(log)
    pc_list = generate_batch_list(pcs_list, log , 'postcode')
    return pc_list 
    


