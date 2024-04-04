import os 
import glob 
import pandas as pd 


def find_batches(pc, batch_dir ):
    pc= pc.strip()
    files = glob.glob(os.path.join(batch_dir , '*/*.txt') ) 
    print('len of batches to search ', len(files))
    files_paths = [] 
    for f in files:
        with open(f) as file:
            if pc in file.read():
                files_paths.append(f)
    print(files_paths)
    if len(files_paths)< 2:
        return None
    return files_paths 

def convert_batch_fp_to_onsud(path):
    dirr = os.path.dirname(path)
    label = os.path.basename(path).split('.')[0].split('_')[-1]
    path = os.path.join(dirr, f'onsud_{label}.csv')
    return path


def custom_load_onsud(pc , batch_dir  ):
    paths = find_batches(pc, batch_dir)    
    df_list = [] 
    for p in paths:
        p2  = convert_batch_fp_to_onsud(p)
        df1 = pd.read_csv(p2)
        df1 = df1[df1['PCDS'].str.strip() ==pc ]
        df_list.append(df1)
    df = pd.concat(df_list )
    return df 