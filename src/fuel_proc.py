import concurrent.futures
import pandas as pd
import tempfile
import os
from src.fuel_calc import process_postcode_fuel
import threading
import geopandas as gpd 

# from .postcode_utils import find_postcode_for_ONSUD_file 

# thread_local = threading.local()



def load_fuel_data(gas_path, elec_path):
    gas_df = pd.read_csv(gas_path) 

    elec_df = pd.read_csv(elec_path) 
    return  gas_df, elec_df



###################################################  Overlap fns  ###################################################

def run_fuel_calc_main_overlap(pcs_list, INPUT_GPK, batch_size, batch_label, log_file, gas_df, elec_df, overlap, batch_dir, path_to_pcshp  ):
    """ main fn called from pc_main to run fuel calc with overlap
    """
    onsud_data=None 
    for i in range(0, len(pcs_list) , batch_size):
        batch = pcs_list[i:i+batch_size]
        print(batch)
        process_fuel_batch_overlap(batch, onsud_data, gas_df, elec_df, INPUT_GPK, batch_label, log_file, overlap, batch_dir, path_to_pcshp )

def process_fuel_batch_overlap( pc_batch, data, gas_df, elec_df, INPUT_GPK, process_batch_name, log_file, overlap, batch_dir , path_to_pcshp):
    """calls base fn with process fn"""
    process_fuel_batch_base(process_postcode_fuel, pc_batch, data, gas_df, elec_df, INPUT_GPK, process_batch_name, log_file, overlap, batch_dir , path_to_pcshp )


###################################################  Normal fns  ###################################################

def process_fuel_batch_main( pc_batch, data, gas_df, elec_df, INPUT_GPK, process_batch_name, log_file):
    """Sub process called by run_fuel_calc_main to process the bathces, uses the base fn called with the processing fn"""
    process_fuel_batch_base(process_postcode_fuel, pc_batch, data, gas_df, elec_df, INPUT_GPK, process_batch_name, log_file )

def run_fuel_calc_main(pcs_list, onsud_data,  INPUT_GPK, batch_size, batch_label, log_file, gas_df, elec_df):
    """Called b pc-main to, runs pc list in batches 
    """
    for i in range(0, len(pcs_list) , batch_size):
        batch = pcs_list[i:i+batch_size]
        process_fuel_batch_main(batch, onsud_data, gas_df, elec_df, INPUT_GPK, batch_label, log_file)


###################################################  base fns  ###################################################

def process_fuel_batch_base(process_fn, pc_batch, data, gas_df, elec_df, INPUT_GPK, process_batch_name, log_file, overlap=None, batch_dir=None , path_to_pcshp=None):
    print('Starting batch processing...')
    
    # Initialize an empty list to collect results
    results = []
    for pc in pc_batch:
        print('Processing postcode:', pc)
        pc_result = process_fn(pc, data, gas_df, elec_df, INPUT_GPK, overlap, batch_dir, path_to_pcshp)  # Assuming this function is defined elsewhere
        if pc_result is not None:
            results.append(pc_result)
    
    print(f'Number of processed results: {len(results)}')
    
    # Only proceed if we have results
    if results:
        df = pd.DataFrame(results)
        # check dups in postcode 
        if df.groupby('postcode').size().max() > 1:
            print('Duplicate postcodes found in the batch')
            raise ValueError('Duplicate postcodes found in the batch')

        print('Saving results to log file...')
        if not os.path.exists(log_file):
            print('Creating log file')
            df.to_csv(log_file, index=False)
        else:
            print('Checking file structure compatibility...')
            with open(log_file, 'r') as file:
                existing_header = file.readline().strip().split(',')
                if existing_header != list(df.columns):
                    # find wrong columns 
                    
                    raise ValueError('Header mismatch between DataFrame and existing CSV file')
            print('File structure compatible - appending')
            
            df = df[existing_header]
            df.to_csv(log_file, mode='a', header=False, index=False)

        print(f'Log file saved for batch: {process_batch_name}')        
        # # Check if the log file already exists
        # if not os.path.exists(log_file):
        #     print('Creating Log file')
        #     # If the file does not exist, write with header
        #     df.to_csv(log_file, index=False)
        # else:
        #     # If the file exists, append without writing the header
        #     print('File already exists - append')
        #     df.to_csv(log_file, mode='a', header=False, index=False)

        # print(f'Log file saved for batch: {process_batch_name}')





# def process_fuel_batch(pc_batch, data, gas_df, elec_df, INPUT_GPK, process_batch_name, log_file):
#     print('Starting batch processing...')
    
    
#     # Initialize an empty list to collect results
#     results = []
#     for pc in pc_batch:
#         print('Processing postcode:', pc)
#         pc_result = process_postcode_fuel(pc, data, gas_df, elec_df, INPUT_GPK)  # Assuming this function is defined elsewhere
#         if pc_result is not None:
#             results.append(pc_result)
    
#     print(f'Number of processed results: {len(results)}')
    
#     # Only proceed if we have results
#     if results:
#         df = pd.DataFrame(results)
#         # check dups in postcode 
#         if df.groupby('postcode').size().max() > 1:
#             print('Duplicate postcodes found in the batch')
#             raise ValueError('Duplicate postcodes found in the batch')

#         print('Saving results to log file...')
        
#         # Check if the log file already exists
#         if not os.path.exists(log_file):
#             print('Creating Log file')
#             # If the file does not exist, write with header
#             df.to_csv(log_file, index=False)
#         else:
#             # If the file exists, append without writing the header
#             print('File already exists - append')
#             df.to_csv(log_file, mode='a', header=False, index=False)

#         print(f'Log file saved for batch: {process_batch_name}')





# def run_fuel_calc_multi_thread(pcs_list, data, gas_df, elec_df, INPUT_GPK, temp_dir, max_workers, batch_size):
#     # Ensure temporary directory exists
#     os.makedirs(temp_dir, exist_ok=True)

#     print('starting fuel calc, bout to run batches')
#     with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers ) as executor:
#         # Store futures if you need to wait for them or check for exceptions
#         futures = []
#         for i in range(0, len(pcs_list), batch_size):
#             batch = pcs_list[i:i+batch_size]
    
#             future= executor.submit(process_batch, batch, data, gas_df, elec_df, INPUT_GPK,  temp_dir )
#             futures.append(future)
#         concurrent.futures.wait(futures)

#         # Check for exceptions in the completed futures
#         for future in futures:
#             if future.exception() is not None:
#                 # Handle the exception
#                 print(f"Exception occurred in thread: {future.exception()}")
#             else:
#                 # Process result if needed (or acknowledge successful completion)
#                 None 


