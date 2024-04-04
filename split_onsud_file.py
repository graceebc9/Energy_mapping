import pandas as pd 
import os 
from src.postcode_utils import  load_onsud_data


def split_onsud_file(path_to_onsud_file, path_to_pcshp, output_directory, logfile, label  ):

    onsud_data = load_onsud_data(path_to_onsud_file, path_to_pcshp)
    raw_data = pd.read_csv(path_to_onsud_file)
    
    print('Starting split for ', label )
    pcs_list = onsud_data.PCDS.unique().tolist()

    if os.path.exists(logfile):
        log = pd.read_csv(logfile)
        done_ids = log['postcode'].unique().tolist()
        pcs_list = [pc for pc in pcs_list if pc not in done_ids]


    batch_size = 10000
    batch_list = []
    for i in range(0, len(pcs_list), batch_size):
        batchs = pcs_list[i:i+batch_size]  

        batch_dir = f'{output_directory}/batches/{label}/'
        os.makedirs(batch_dir, exist_ok=True)   

        batch_filename = os.path.join(batch_dir, f"batch_{i//batch_size}.txt" ) 
        
        with open('batch_paths.txt', 'w') as f:
                f.write(f"{batch_filename}\n")

        with open(batch_filename, 'a') as f:
            for pc in batchs:
                f.write(f"{pc}\n")
        
        
        # export subst of onsud file 
       
        subsetdata = raw_data[raw_data['PCDS'].str.strip().isin(batchs)].copy()
        subsetdata.to_csv(f'{batch_dir}/onsud_{i//batch_size}.csv', index=False)

    print('Batches saved')
   

if __name__ == "__main__":
    print('Loading files')
    path_to_onsud_file= os.environ.get('ONSUD_PATH')
    path_to_pcshp= os.environ.get('PC_SHP_PATH')
    output_directory = os.environ.get('OUTPUT_DIR')
    
    label = path_to_onsud_file.split('/')[-1].split('.')[0].split('_')[-1]
    log = os.path.join(output_directory, label,  'log_file.csv')
    
    split_onsud_file(path_to_onsud_file,  path_to_pcshp, output_directory, logfile =  log , label =  label)
    
    print('Batches saved to ')





# export OUTPUT_DIR='/Users/gracecolverd/New_dataset/test'
# export ONSUD_PATH='/Volumes/T9/Data_downloads/ONS_UPRN_database/ONSUD_DEC_2022/Data/ONSUD_DEC_2022_EM.csv'
# export PC_SHP_PATH='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'

