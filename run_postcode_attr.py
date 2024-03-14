


import os 
from src import find_postcode_for_ONSUD_file, find_data_pc, calc_med_attr
from src import run_batching, merge_temp_logs_to_main , generate_batch_list 
from src import calc_med_attr , process_postcode  , gen_postcode_areas
from src import  postcode_area_vars_batch_fn, postcode_median_age_batch_fn , postcode_modal_batch_fn

# ######## Median age band varaibles  ########
# col_name = 'postcode'
# attribute = 'median_ageband'
# result_cols = ['postcode', 'status', str(attribute) ]
# batch_fn = postcode_median_age_batch_fn
# postcode_area_bool=True 


# ######## Modal age band varaibles  ########
# col_name = 'postcode'
# attribute = 'modal_age_band'
# result_cols = ['postcode', 'status', str(attribute) ]
# batch_fn = postcode_modal_batch_fn 
# postcode_area_bool= False 


######## Area variables  ########
col_name = 'postcode'
attribute = 'area'
result_cols = ['postcode', 'status', str(attribute) ]
batch_fn = postcode_area_vars_batch_fn 
postcode_area_bool=True 

######## Settings variables ########
batch_size = 50 
max_workers = 10   




def main():
    base_dir = '/Users/gracecolverd/New_dataset'
    print('Finding data for ONSUD file')
    pc_df , data = find_postcode_for_ONSUD_file('/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022/Data/ONSUD_DEC_2022_EE.csv' )
    lab = 'EE'

    full_list = data['PCDS'].unique()   
    print(len(full_list))
    output_dir = os.path.join(base_dir, f'data/postcode_attributes/{attribute}' )
    os.makedirs(output_dir, exist_ok=True)
    log_file =  os.path.join(output_dir, f'{lab}_{attribute}_log.csv' )    
    


    print('starting merge')
    merge_temp_logs_to_main(log_file) 

    whole_batch_list = generate_batch_list(full_list, log_file, col_name  )
    
    print(len(whole_batch_list  ))
    if postcode_area_bool ==True: 
        print('Getting postcode areas')
        postcodes_geom = gen_postcode_areas(data, lab )
        # Set PCDS as index if it's not already
        postcodes_geom.set_index('PCDS', inplace=True)
        postcodes_area = [postcodes_geom.loc[x, 'pc_area'] for x in full_list if x in postcodes_geom.index]
        whole_batch_list = zip(full_list, postcodes_area)
    
    
    print('Starting attribute calculation')
    run_batching(whole_batch_list= whole_batch_list, batch_fn =  batch_fn , result_cols = result_cols, data = data,   log_file = log_file,  pc_area=postcode_area_bool, batch_size = batch_size, max_workers=max_workers) 
    merge_temp_logs_to_main(log_file) 
    print('Attribute calculation complete')

if __name__ == '__main__':  
    main() 
