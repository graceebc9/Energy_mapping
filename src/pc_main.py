import os
import pandas as pd
from src.postcode_utils import load_onsud_data, load_ids_from_file
from src.fuel_proc import run_fuel_calc_main, load_fuel_data
from src.age_perc_proc import run_age_calc
from src.type_proc import run_type_calc
from src.orientation_proc import run_orient_calc
from src.overlap import get_overlap_batch_ids



def main(batch_path, data_dir, path_to_onsud_file, path_to_pcshp, INPUT_GPK, region_label, batch_label, attr_lab, process_function, gas_path=None, elec_path=None, overlap=None, batch_dir=None, overlap_outcode=None):
    
    def gen_batch_ids(batch_ids, log_file):
        if os.path.exists(log_file):
            print('Removing already processed IDs')
            print('Old len is ', len(batch_ids))
            log = pd.read_csv(log_file)
            proc_id = log.postcode.unique().tolist()
            batch_ids = [x for x in batch_ids if x not in proc_id]
            print('New len is ', len(batch_ids))
            return batch_ids
        else:
            print('No IDs processed yet')
            return batch_ids

    print('Starting Label ', region_label)
    proc_dir = os.path.join(data_dir, 'proc_dir', attr_lab, region_label)
    os.makedirs(proc_dir, exist_ok=True)
    print('Batch is ', batch_path)
    log_file = os.path.join(proc_dir, f'{batch_label}_log_file.csv')
    print('Log file is ', log_file)

    print('Loading ONSUD data')
    onsud_data = load_onsud_data(path_to_onsud_file, path_to_pcshp)
    
    print(batch_path)
    if overlap == 'Yes':
        print('Overlap starting')
        batch_ids = get_overlap_batch_ids(overlap_outcode, batch_path)  
    else:
        batch_ids = load_ids_from_file(batch_path)
        batch_ids = gen_batch_ids(batch_ids, log_file)
    
    print('Len of batch is ', len(batch_ids))
    print('Starting batch process')
    print('Batch ids are ', len(batch_ids))
    print('ONSUD data is ', onsud_data)
    print('Input GPK is ', INPUT_GPK)
    print('Batch size is ', 10)
    print('Batch label is ', batch_label)
    print('Log file is ', log_file)
    print('Gas path is ', gas_path)
    print('Elec path is ', elec_path)
    print('Overlap is ', overlap)
    print('Batch dir is ', batch_dir)

    # Call the process function with required arguments
    process_function(batch_ids, onsud_data, INPUT_GPK, batch_size=10, batch_label=batch_label, log_file=log_file, gas_path=gas_path, elec_path=elec_path, overlap=overlap, batch_dir=batch_dir, path_to_pcshp=path_to_pcshp)
    print('Batch complete')

# Define the differing process functions outside of `main`
def run_fuel_process(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, gas_path, elec_path, overlap, batch_dir, path_to_pcshp):
    gas_df, elec_df = load_fuel_data(gas_path, elec_path)
    run_fuel_calc_main(batch_ids, onsud_data, INPUT_GPK=INPUT_GPK, batch_size=batch_size, batch_label=batch_label, log_file=log_file, gas_df=gas_df, elec_df=elec_df)

def run_age_process(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, gas_path=None, elec_path=None, overlap=None, batch_dir=None, path_to_pcshp=None):
    run_age_calc(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, overlap)

def run_type_process(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, gas_path=None, elec_path=None, overlap=None, batch_dir=None, path_to_pcshp=None):
    run_type_calc(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file)

def run_orient_process(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, gas_path=None, elec_path=None, overlap=None, batch_dir=None, path_to_pcshp=None):
    run_orient_calc( pcs_list= batch_ids, data= onsud_data, INPUT_GPK= INPUT_GPK,  batch_size= batch_size, batch_label= batch_label, log_file= log_file, overlap=overlap)
