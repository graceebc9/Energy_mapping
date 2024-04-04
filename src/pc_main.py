import os
import pandas as pd
from src.postcode_utils import load_onsud_data, load_ids_from_file, get_onsud_path
from src.fuel_proc import run_fuel_calc , load_fuel_data
from src.age_proc import run_age_calc

def main(batch_path, data_dir, path_to_onsud_file, path_to_pcshp, INPUT_GPK, batch_label, attr_lab, process_function, gas_path=None, elec_path=None):
    
    def gen_batch_ids(batch_ids, log_file):
        if os.path.exists(log_file):
            print('Removing already proc id')
            print('Old len is ', len(batch_ids))
            log = pd.read_csv(log_file)
            proc_id = log.postcode.unique().tolist()
            batch_ids = [x for x in batch_ids if x not in proc_id]
            print('new len is ', len(batch_ids))
            return batch_ids
        else:
            print('No ids proccessed yet')
            return batch_ids

    label = path_to_onsud_file.split('/')[-2]
    print('Starting Label ', label)
    proc_dir = os.path.join(data_dir, 'proc_dir', attr_lab, label)
    os.makedirs(proc_dir, exist_ok=True)
    log_file = os.path.join(proc_dir, f'{batch_label}_log_file.csv')
    print('Log file is ', log_file)

    onsud_data = load_onsud_data(path_to_onsud_file, path_to_pcshp)

    onsud_data = pd.read_csv(path_to_onsud_file)
    batch_ids = load_ids_from_file(batch_path)
    batch_ids = gen_batch_ids(batch_ids, log_file)
    print('Len of batch is ', len(batch_ids))
    print('Starting batch process')
    
    # Call the process function with required arguments
    process_function(batch_ids, onsud_data, INPUT_GPK, batch_size=10, batch_label=batch_label, log_file=log_file , gas_path= gas_path, elec_path= elec_path )
    print('Batch complete')

# Define the differing process functions outside of `main`
def run_fuel_process(batch_ids, onsud_data, INPUT_GPK,  batch_size, batch_label, log_file, gas_path, elec_path):
    gas_df, elec_df = load_fuel_data(gas_path, elec_path)
    run_fuel_calc(batch_ids, onsud_data,  INPUT_GPK, batch_size, batch_label, log_file ,gas_df, elec_df )

def run_age_process(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, gas_path=None, elec_path=None):
    run_age_calc(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file )


