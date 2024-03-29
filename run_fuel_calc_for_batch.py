import os 
from src.fuel_proc import load_fuel_data , run_fuel_calc, load_onsud_data


def load_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        ids = file.read().splitlines()
    return ids

def get_onsud_path(onsud_dir, label ):

    # DATA_DIR='/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022'
    date = onsud_dir.split('/')[-1].split('ONSUD_')[-1]
    filepath = os.path.join(onsud_dir, f'Data/ONSUD_{date}_{label}.csv' ) 
    return filepath

def main( batch_path, data_dir, gas_path, elec_path, path_to_onsud_file, path_to_pcshp, INPUT_GPK  ):
    label = path_to_onsud_file.split('/')[-1].split('.')[0].split('_')[-1]
    print('Starting Label ', label)
    proc_dir = os.path.join(data_dir, 'proc_dir', label)
    os.makedirs(proc_dir, exist_ok=True )

    gas_df, elec_df = load_fuel_data(gas_path, elec_path )
    onsud_data = load_onsud_data(path_to_onsud_file, path_to_pcshp)
    
    # load txt file 
    batch_ids = load_ids_from_file(batch_path)
    print('Len of batch is ', len(batch_ids))
    print('Starting batch process')
    
    run_fuel_calc(batch_ids, onsud_data, gas_df, elec_df, INPUT_GPK,  proc_dir, batch_size=10)

if __name__ == "__main__":
    print('loading varibles')
    data_dir = os.environ.get('DATA_DIR')
    gas_path = os.environ.get('GAS_PATH')
    elec_path = os.environ.get('ELEC_PATH')
    onsud_dir= os.environ.get('ONSUD_DIR')
    path_to_pcshp= os.environ.get('PC_SHP_PATH')
    input_gpk_building = os.environ.get('BUILDING_PATH')
    batch_path = os.environ.get('BATCH_PATH') 
    label = batch_path.split('/')[-2]
    path_to_onsud_file = get_onsud_path( onsud_dir, label )
    
    print('starting main')
    main( batch_path, data_dir, gas_path, elec_path, path_to_onsud_file, path_to_pcshp, INPUT_GPK = input_gpk_building  ) 


# export  BATCH_PATH='/Users/gracecolverd/New_dataset/test/batches/NE/batch_0.txt'
# export DATA_DIR='/Users/gracecolverd/New_dataset/test'
# export ONSUD_DIR='/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022'
# export PC_SHP_PATH='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'
# export GAS_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_2022.csv'
# export ELEC_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_2022.csv'
# export BUILDING_PATH='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_22_updated_data/UKBuildings_Edition_15_new_format_upn.gpkg'
    
    