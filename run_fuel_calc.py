import os 
from src.fuel_proc import load_fuel_data , load_onsud_data, get_pcs_to_process, run_fuel_calc
from src.multi_thread import merge_temp_logs_to_main 


def main(data_dir, gas_path, elec_path, path_to_onsud_file, path_to_pcshp, INPUT_GPK, max_workers=8, batch_size = 50):
    proc_dir = os.path.join(data_dir, 'proc_dir')
    os.makedirs(proc_dir, exist_ok=True )

    log = os.path.join(proc_dir, 'log_file.csv')

    gas_df, elec_df = load_fuel_data(gas_path, elec_path )

    onsud_data = load_onsud_data(path_to_onsud_file, path_to_pcshp)

    pc_list = get_pcs_to_process(onsud_data, log)

    run_fuel_calc(pc_list, onsud_data, gas_df, elec_df, INPUT_GPK,  proc_dir,  max_workers=max_workers, batch_size=batch_size)

    merge_temp_logs_to_main(log)    
    print('Run complete for ONSUD file')



if __name__ == "__main__":
    print('loading varibles')
    data_dir = os.environ.get('DATA_DIR')
    gas_path = os.environ.get('GAS_PATH')
    elec_path = os.environ.get('ELEC_PATH')
    path_to_onsud_file= os.environ.get('ONSUD_PATH')
    path_to_pcshp= os.environ.get('PC_SHP_PATH')
    input_gpk_building = os.environ.get('BUILDING_PATH')
    max_workers=os.environ.get('MAX_WORKERS')
    batch_size =os.environ.get('BATCH_SIZE')
    print(data_dir)
    print('starting main')
    main(data_dir, gas_path, elec_path, path_to_onsud_file, path_to_pcshp, input_gpk_building,  int(max_workers), batch_size ) 
