import subprocess
import os 

################################ Update the following variables ################################

gas_elec = 'gas'
fuel_year = 2022
root_dir = '/Users/gracecolverd/New_dataset/'

################################ Update paths to downloaded data ################################ 

onsud = '/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022/Data' #ONS ONSUD DATA
raw_elec = f'/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_{fuel_year}.csv' #electricity by postcode 
raw_gas = f'/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_{fuel_year}.csv' #gas by postcode 

pc_map ='/Volumes/T9/Data_downloads/lookups/pcs_to_oa_mapping_census2021/PCD_OA21_LSOA21_MSOA21_LAD_AUG23_UK_LU.csv'
link = '/Volumes/T9/Data_downloads/Versik_building_data/2024_03_full_building_data/6101/Data/edition_15_abc_link_file.csv' #link file
postcode_base  = '/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291/two_letter_pc_code/'
lk = '/Volumes/T9/Data_downloads/Eng_wales_boundary_shapefiles/LSOA_(2021)_to_Built_Up_Area_to_Local_Authority_District_to_Region_(December_2022)_Lookup_in_England_and_Wales_v2.csv'
building_file_directory = '/Volumes/T9/postcode_data/data/verisk_y2022_2' 

################################################################################################ 

postcode_shapefile_path = os.path.join(postcode_base,'*lookup.txt' )

def run_script(script_name, **kwargs):
    # Construct the command with script name and kwargs
    command = ['python', script_name]
    for key, value in kwargs.items():
        command.append(f'--{key}={value}')
    
    # Run the command and check if it succeeded
    completed_process = subprocess.run(command)
    if completed_process.returncode != 0:
        raise Exception(f"Script {script_name} failed with return code {completed_process.returncode}")


def main():
    # Call match_postcode_to_uprns.py with kwargs
    run_script('match_postcode_to_uprns.py', gas_elec= gas_elec, raw_elec=raw_elec, raw_gas=raw_gas, pc_map=pc_map, link=link, lk=lk, onsud=onsud, fuel_year=fuel_year  )

    # Call gen_nrom_fuel.py with kwargs
    run_script('gen_norm_fuel.py', gas_elec= gas_elec , filtered= True, fuel_year=fuel_year , building_file_directory=building_file_directory)
    run_script('gen_norm_fuel.py', gas_elec= gas_elec , filtered= False , fuel_year=fuel_year , building_file_directory=building_file_directory  )

    # Call post_process_fuel.py with kwargs
    run_script('post_process_fuel.py', gas_elec= gas_elec, fuel_year=fuel_year , postcode_shapefile_path=postcode_shapefile_path, root_dir=root_dir )

if __name__ == '__main__':
    main()
