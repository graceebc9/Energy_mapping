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

def process_fuel_batch(pc_batch, data, gas_df, elec_df, INPUT_GPK, process_batch_name, log_file):
    print('Starting batch processing...')
    # log_file = os.path.join(temp_dir, f'{process_batch_name}_log_file.csv')
    
    # Initialize an empty list to collect results
    results = []
    for pc in pc_batch:
        print('Processing postcode:', pc)
        pc_result = process_postcode_fuel(pc, data, gas_df, elec_df, INPUT_GPK)  # Assuming this function is defined elsewhere
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
        
        # Check if the log file already exists
        if not os.path.exists(log_file):
            print('Creating Log file')
            # If the file does not exist, write with header
            df.to_csv(log_file, index=False)
        else:
            # If the file exists, append without writing the header
            print('File already exists - append')
            df.to_csv(log_file, mode='a', header=False, index=False)

        print(f'Log file saved for batch: {process_batch_name}')




def run_fuel_calc(pcs_list, data, gas_df, elec_df, INPUT_GPK, temp_dir, batch_size, batch_label, log_file):
    # Ensure temporary directory exists
    temp_dir = os.path.join(temp_dir, 'fuel')
    os.makedirs(temp_dir, exist_ok=True)
    
    for i in range(0, len(pcs_list) , batch_size):
        batch = pcs_list[i:i+batch_size]
        process_fuel_batch(batch, data, gas_df, elec_df, INPUT_GPK,  temp_dir, batch_label, log_file)


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









