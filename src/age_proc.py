import pandas as pd 
import os 
from src.age_calc import process_postcode_age_residential

def process_age_batch(pc_batch, data, INPUT_GPK, temp_dir, process_batch_name):
    print('Starting batch processing...')
    log_file = os.path.join(temp_dir, f'{process_batch_name}_log_file.csv')
    
    # Initialize an empty list to collect results
    results = []
    for pc in pc_batch:
        print('Processing postcode:', pc)
        pc_result = process_postcode_age_residential(pc, data, INPUT_GPK)  # Assuming this function is defined elsewhere
        if pc_result is not None:
            results.append(pc_result)
    
    print(f'Number of processed results: {len(results)}')
    
    # Only proceed if we have results
    if results:
        df = pd.DataFrame(results)
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


def run_age_calc(pcs_list, data, INPUT_GPK, temp_dir, batch_size, batch_label):
    # Ensure temporary directory exists
    os.makedirs(temp_dir, exist_ok=True)
    print('proc dir is ', temp_dir)
    
    for i in range(0, len(pcs_list) , batch_size):
        batch = pcs_list[i:i+batch_size]
        process_age_batch(batch, data, INPUT_GPK,  temp_dir, batch_label)
