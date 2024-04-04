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
    if len(files_paths)!=2:
        raise Exception('no matches found for pcs ', pc)
    return files_paths 

def convert_batch_fp_to_onsud(path):
    dirr = os.path.dirname(path)
    label = os.path.basename(path).split('.')[0].split('_')[-1]
    path = os.path.join(dirr, f'onsud_{label}.csv')
    return path


def custom_load_onsud(pc , batch_dir  ):
    f1, f2 = find_batches(pc, batch_dir)    
    f1, f2 = convert_batch_fp_to_onsud(f1), convert_batch_fp_to_onsud(f2)
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)
    df = pd.concat([df1,df2])
    return df 