import os 
from src.fuel_proc import load_fuel_data 
from src.postcode_utils import load_ids_from_file, get_onsud_path 
import pandas as pd 


from src.pc_main import main , run_fuel_process




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
    overlap = os.environ.get('OVERLAP_BL')
 
    # path_to_onsud_file = get_onsud_path( onsud_dir, onsud_data, label )
    print(overlap)
    if overlap=='Yes':
        print('overlap starting')
        overlap_outcode = os.environ.get('OVERLAP_OUTCODE')
        ovl_diir =os.environ.get('OVERLAP_ONSUD_BATCH_FOlDER')  
        onsud_path = os.path.join(ovl_diir, f'{overlap_outcode}_omsud.csv')
        label=f'overlap_{overlap_outcode}'
        batch_id = f'overlap_{overlap_outcode}'
    else:
        print('Non overlap starting')
        label = batch_path.split('/')[-2]
        batch_id = batch_path.split('/')[-1].split('.')[0].split('_')[-1]
        onsud_path = os.path.join(os.path.dirname(batch_path), f'onsud_{batch_id}.csv') 
        overlap_outcode= None 

    main(batch_path, data_dir, onsud_path, path_to_pcshp, INPUT_GPK=input_gpk_building, region_label=label,  batch_label=batch_id, attr_lab='fuel', process_function=run_fuel_process, gas_path=gas_path, elec_path=elec_path, overlap_outcode=overlap_outcode, overlap=overlap)




# # export  BATCH_PATH='/Users/gracecolverd/New_dataset/test/batches/WM/batch_0.txt'
# export BATCH_PATH='/Users/gracecolverd/New_dataset/overlapping_pcs.txt'
# export DATA_DIR='/Users/gracecolverd/New_dataset/test'
# export PC_SHP_PATH='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'
# export GAS_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_2022.csv'
# export ELEC_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_2022.csv'
# export BUILDING_PATH='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_22_updated_data/UKBuildings_Edition_15_new_format_upn.gpkg'
# export OVERLAP_ONSUD_BATCH_FOlDER='/Volumes/T9/Data_downloads/new-data-outputs/overlap_batches'
# export OVERLAP_BL='Yes'
# export OVERLAP_OUTCODE='BH'
    
