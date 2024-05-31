import os 
import pandas as pd 
from src.pc_main import main , run_fuel_process_overlap


if __name__ == "__main__":
    onsud_data = 'DEC_2022'
    print('Loading variables')
    data_dir = os.environ.get('DATA_DIR')
    gas_path = os.environ.get('GAS_PATH')
    elec_path = os.environ.get('ELEC_PATH')
    # onsud_dir= os.environ.get('ONSUD_DIR')
    path_to_pcshp= os.environ.get('PC_SHP_PATH')
    input_gpk_building = os.environ.get('BUILDING_PATH')
    batch_path = os.environ.get('BATCH_PATH') 
    batch_dir = os.environ.get('BATCH_DIR')
    
    
    label ='overlap'
    
    # path_to_onsud_file = get_onsud_path( onsud_dir, onsud_data, label )
    onsud_path = None 
    batch_id = 'overlap'
    
    main(batch_path = batch_path, data_dir = data_dir, path_to_onsud_file = onsud_path, path_to_pcshp =path_to_pcshp,
          INPUT_GPK=input_gpk_building, region_label=label, batch_label=batch_id, attr_lab='fuel', process_function=run_fuel_process_overlap, gas_path=gas_path, elec_path=elec_path, overlap=True, batch_dir = batch_dir)



# export BATCH_DIR='/Volumes/T9/Data_downloads/new-data-outputs/batches (1)'
# export  BATCH_PATH='/Users/gracecolverd/New_dataset/overlapping_pcs.txt'
# export DATA_DIR='/Users/gracecolverd/New_dataset/test'
# export ONSUD_DIR='/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022'
# export PC_SHP_PATH='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'
# export GAS_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_2022.csv'
# export ELEC_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_2022.csv'
# export BUILDING_PATH='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_22_updated_data/UKBuildings_Edition_15_new_format_upn.gpkg'
    
    
