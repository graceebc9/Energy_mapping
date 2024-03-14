
import geopandas as gpd
import glob 
import pandas as pd
import os
import concurrent.futures
from osgeo import ogr
import pandas as pd
import os
import shutil 
import tempfile
import threading

# Ensure thread_local is defined at the global level
thread_local = threading.local()


def generate_batch_list(full_list, log, col_name ): 
    print('Start generate list')
    if os.path.exists(log):
        log = pd.read_csv(log)
        complete = log[col_name].unique().tolist() 
        batch_list = [x for x in full_list if str(x) not in complete] 
    
    else:
        batch_list = full_list
    print('num to process ',   len(batch_list) ) 
    return batch_list 



def run_batching(whole_batch_list, batch_fn, data, result_cols, log_file, pc_area=None, batch_size = 5, max_workers=6):
    if pc_area is not None:
        whole_batch_list , pc_area_list = zip(*whole_batch_list)
    with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers ) as executor:
        # Store futures if you need to wait for them or check for exceptions
        futures = []
        for i in range(0, len(whole_batch_list), batch_size):
            batch = whole_batch_list[i:i+batch_size]
            if pc_area is not None:
                pc_area = pc_area_list[i:i+batch_size]
                future = executor.submit(process_batch, batch, batch_fn, data,  result_cols, log_file, pc_area)
            else:
                future= executor.submit(process_batch, batch, batch_fn, data,  result_cols, log_file, pc_area)
            futures.append(future)
        # Optionally wait for all futures if needed
        concurrent.futures.wait(futures)

def process_batch(batch_list, batch_fn, data, results_cols, log_file, pc_area):
    print('Starting batch')
    results = []
    if pc_area is not None:
        for item , area in zip(batch_list, pc_area):
            item_results = batch_fn(item, data, area)
    else:
        for item in batch_list:
            item_results = batch_fn(item, data)
    results.append(item_results)
    df = pd.DataFrame(results, columns=results_cols )
    print('Results done, starting save')
    # Get the temp file path and whether it's the first write operation
    temp_file_path, is_first_write = get_thread_temp_file(log_file)
    print('temp file path is ' , temp_file_path )
    # Open the file with 'a' mode to append and ensure headers are written correctly
    with open(temp_file_path, 'a') as f:
        df.to_csv(f, header=is_first_write, index=False)
    
    # Update the flag to indicate the header should not be written next time
    if is_first_write:
        thread_local.temp_file_first_write = False

    print('temp file saved for batch')



def get_thread_temp_file(log_file):
    if not hasattr(thread_local, 'temp_file'):
        temp_dir = os.path.dirname(log_file)

        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.csv', prefix='temp_log_', dir=temp_dir)        

        thread_local.temp_file = temp_file.name
        thread_local.temp_file_first_write = True
    return thread_local.temp_file, thread_local.temp_file_first_write



def merge_temp_logs_to_main(log_file ):
    """
    Merge all temporary log files created by threads into the main log file.

    Parameters:
    - log_file: str, the path to the main log file.
    """
    # Assume temp files are in the same directory as the main log file
    temp_files = [f for f in os.listdir(os.path.dirname(log_file)) if f.startswith('temp_log_') and f.endswith('.csv')]
    print('Num of temp files found ', len(temp_files) ) 

    # Create or append to the main log file
    if len(temp_files) != 0:
        for temp_file in temp_files:
            temp_file_path = os.path.join(os.path.dirname(log_file), temp_file)
            try:
                df_temp = pd.read_csv(temp_file_path )
            except:
                print('Error reading temp file ', temp_file_path )
                continue
            
            if os.path.exists(log_file):
                df_temp.to_csv(log_file, mode='a', header=False, index=False)
            else:
                df_temp.to_csv(log_file, mode='w', header=True, index=False)
    
    cleanup_temp_files( temp_dir = os.path.dirname(log_file), temp_file_prefix="temp_log_", )

            

def cleanup_temp_files(temp_dir, temp_file_prefix="temp_log_", ):
    print('Starting cleanup')
    for filename in os.listdir(temp_dir):
        if filename.startswith(temp_file_prefix) and filename.endswith('.csv'):
            os.remove(os.path.join(temp_dir, filename))
            print(f"Deleted temporary file: {filename}") 
    