# run_whole_process.py 

# call a python script 
# call match_postcode_to_uprns.py with kwargs gas+elec ='gas' 


# call script gen_nrom_fuel.py with kwargs gas+elec ='gas' and filtered =True 

# call script post_process_fuel.py with kwargs gas+elec ='gas' 

import subprocess

gas_elec = 'gas'
filt=True 

fuel_year = 2022
onsud = '/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022/Data'
raw_elec = f'/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_{fuel_year}.csv'
raw_gas = f'/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_{fuel_year}.csv'

pc_map ='/Volumes/T9/Data_downloads/Postcode_to_LSOA_mapping/PCD_OA21_LSOA21_MSOA21_LAD_AUG23_UK_LU 2.csv'

link = '/Volumes/T9/Data_downloads/Versik_building_data/UKBuildings_Edition_14_ABC_link_file.csv'
lk = '/Volumes/T9/Data_downloads/Eng_wales_boundary_shapefiles/LSOA_(2021)_to_Built_Up_Area_to_Local_Authority_District_to_Region_(December_2022)_Lookup_in_England_and_Wales_v2.csv'


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
    run_script('gen_norm_fuel.py', gas_elec= gas_elec , filtered= True, fuel_year=fuel_year )
    run_script('gen_norm_fuel.py', gas_elec= gas_elec , filtered= False , fuel_year=fuel_year   )

    # Call post_process_fuel.py with kwargs
    run_script('post_process_fuel.py', gas_elec= gas_elec, fuel_year=fuel_year  )

if __name__ == '__main__':
    main()
