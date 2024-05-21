import os
import pandas as pd
from src.postcode_utils import load_onsud_data, load_ids_from_file, get_onsud_path
from src.fuel_proc import run_fuel_calc_main , run_fuel_calc_main_overlap, load_fuel_data
from src.age_proc import run_age_calc
from src.type_proc import run_type_calc


def main(batch_path, data_dir, path_to_onsud_file, path_to_pcshp, INPUT_GPK, region_label, batch_label, attr_lab, process_function, gas_path=None, elec_path=None, overlap= None, batch_dir = None ):
    
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

    # label = path_to_onsud_file.split('/')[-2]

    print('Starting Label ', region_label)
    proc_dir = os.path.join(data_dir, 'proc_dir', attr_lab, region_label)
    os.makedirs(proc_dir, exist_ok=True)
    print('batch is ', batch_path )
    log_file = os.path.join(proc_dir, f'{batch_label}_log_file.csv')
    print('Log file is ', log_file)

    print('Loading onsud data')
    onsud_data = load_onsud_data(path_to_onsud_file, path_to_pcshp)
    

    batch_ids = load_ids_from_file(batch_path)
    batch_ids = gen_batch_ids(batch_ids, log_file)
    
    print('Len of batch is ', len(batch_ids))
    print('Starting batch process')
    print('Batch ids are ', len(batch_ids))
    print('Onsud data is ', onsud_data)
    print('Input gpk is ', INPUT_GPK)
    print('Batch size is ', 10)
    print('Batch label is ', batch_label)
    print('Log file is ', log_file)
    print('Gas path is ', gas_path)
    print('Elec path is ', elec_path)
    print('Overlap is ', overlap)
    print('Batch dir is ', batch_dir)

    # Call the process function with required arguments
    process_function(batch_ids, onsud_data, INPUT_GPK, batch_size=10, batch_label=batch_label, log_file=log_file , gas_path= gas_path, elec_path= elec_path,  overlap= overlap, batch_dir = batch_dir , path_to_pcshp=path_to_pcshp)
    print('Batch complete')

# Define the differing process functions outside of `main`
def run_fuel_process(batch_ids, onsud_data, INPUT_GPK,  batch_size, batch_label, log_file, gas_path, elec_path, overlap, batch_dir, path_to_pcshp):
    gas_df, elec_df = load_fuel_data(gas_path, elec_path)
    run_fuel_calc_main(batch_ids, onsud_data,  INPUT_GPK= INPUT_GPK, batch_size= batch_size, batch_label = batch_label, log_file= log_file ,gas_df = gas_df, elec_df = elec_df)

def run_fuel_process_overlap(batch_ids, onsud_data, INPUT_GPK,  batch_size, batch_label, log_file, gas_path, elec_path, overlap, batch_dir, path_to_pcshp):
    gas_df, elec_df = load_fuel_data(gas_path, elec_path)
    run_fuel_calc_main_overlap(batch_ids, INPUT_GPK, batch_size, batch_label, log_file, gas_df, elec_df, overlap, batch_dir , path_to_pcshp) 


# def run_fuel_process_overlap(batch_ids, INPUT_GPK,  batch_size, batch_label, log_file, gas_path, elec_path, overlap, batch_dir):
#     gas_df, elec_df = load_fuel_data(gas_path, elec_path)
#     run_fuel_calc_main_overlap(batch_ids, INPUT_GPK= INPUT_GPK, batch_size= batch_size, batch_label = batch_label, log_file= log_file, gas_df = gas_df, elec_df = elec_df, overlap= overlap, batch_dir = batch_dir )



def run_age_process(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, gas_path=None, elec_path=None, overlap=None, batch_dir=None, path_to_pcshp=None):
    run_age_calc(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file )

def run_type_process(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file, gas_path=None, elec_path=None, overlap=None, batch_dir=None, path_to_pcshp=None):
    run_type_calc(batch_ids, onsud_data, INPUT_GPK, batch_size, batch_label, log_file )