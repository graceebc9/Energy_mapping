import sys
import os
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor


from ml_utils.src.model_col_final import settings_dict, settings_col_dict_census


def check_directory_and_files(output_directory, required_files):
    """
    Check if the specified directory exists and contains the required files.
    
    Parameters:
        output_directory (str): The path to the directory to check.
        required_files (list): A list of filenames expected in the directory.
    
    Returns:
        bool: True if the directory exists and contains all required files, False otherwise.
    """
    # Check if the directory exists
    if not os.path.exists(output_directory):
        print(f"Directory {output_directory} does not exist. Will be created.")
        return False

    # Check for the presence of all required files in the directory
    missing_files = [file for file in required_files if not os.path.isfile(os.path.join(output_directory, file))]
    if missing_files:
        print(f"Missing files in {output_directory}: {', '.join(missing_files)}")
        return False
    
    return True


def transform(df, label, col_setting, settting_dict ):
    cols = settting_dict[col_setting][1]
    working_cols = cols + [label]
    df = df[working_cols]
    df = df[~df[label].isna()]
    return df

def save_results(results, output_path):
    res_string = str(results)
    # summary = predictor.fit_summary()
    with open(os.path.join(output_path, 'model_summary.txt'), 'w') as f:
        f.write(res_string)


def main():

    data_path = os.environ.get('DATA_PATH')
    output_path = os.environ.get('OUTPUT_PATH')
    model_preset= os.environ.get('MODEL_PRESET')
    time_limit = int(os.environ.get('TIME_LIM'))
    train_subset_prop = float(os.environ.get('TRAIN_SUBSET_PROP') )
    model_types = os.environ.get('MODEL_TYPES')
    target = os.environ.get('TARGET')
    column_setting =int( os.environ.get('COL_SETTING'))
    run_regionally = os.environ.get('RUN_REGIONAL')
    run_census = os.environ.get('run_census')   
    region_id = os.environ.get('REGION_ID')
    run_gas_filter = os.environ.get('RUN_GAS_FILTER')
    gas_threshold = os.environ.get('GAS_THRESHOLD')
    
    if target == 'totalelec':   
        label = 'total_elec'
    elif target == 'totalgas':
        label = 'total_gas'
    else:
        raise Exception('No target')

    
    excl_models = []
    

    
    df = pd.read_csv(data_path)
    dataset_name = os.path.basename(data_path).split('.')[0].split('_tr')[0]
    
    if run_gas_filter == 'Yes':
        gas_threshold = int(gas_threshold)
        df = df[df['diff_gas_meters_uprns_res'] < gas_threshold] 
        dataset_name = dataset_name + '_' + str(gas_threshold)

    if run_census =='Yes':
        print('running with census data')
        setting_dir = settings_col_dict_census
    else: 
        setting_dir = settings_dict 


    if run_regionally == 'Yes':
        loc_type='local'
        if region_id in ['SW', 'EM', 'EE', 'WA', 'SE', 'NW', 'YH', 'WM', 'LN', 'NE']:
            train_data = df[df['region']!=region_id]
            test_data = df[df['region']==region_id]
        else:
            raise Exception('Region not correct')
    else:
        loc_type= 'global'
        region_id= None
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
    train_data = transform(TabularDataset(train_data), label, column_setting, setting_dir)
        
    print(f'starting model run for {loc_type} target {label}, time lim {time_limit}, col setting {column_setting}, model preset {model_preset} and train subset {train_subset_prop}' )


    
    output_directory = f"{output_path}/{dataset_name}__{loc_type}__{label}__{time_limit}__colset_{column_setting}__{model_preset}___tsp_{train_subset_prop}__{model_types}__{region_id}"
    required_files = ['model_summary.txt']  # List of files you expect to exist
    
    
    # Check if output directory exists and has all required files
    if check_directory_and_files(output_directory, required_files):
        print(f"Directory {output_directory} already contains all necessary files. Exiting to prevent data overwrite.")
        sys.exit(0)
    else:
        # Create directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        print(f"Directory {output_directory} is ready for use.")

    
    # Reduce the training dataset if needed
    if train_subset_prop != 1:
        train_subset, _ = train_test_split(train_data, test_size=1-train_subset_prop, random_state=42)
        # train_subset.to_csv(os.path.join(output_directory, 'train_subset.csv'), index=False)
    else:
        
        train_subset = train_data   
    size_train = len(train_subset) 
    predictor = TabularPredictor(label, path=output_directory).fit(train_subset, 
                                                                time_limit=time_limit,
                                                                presets=model_preset,
                                                                excluded_model_types=excl_models)
    
    test_data = transform(TabularDataset(test_data), label, column_setting, setting_dir)
    test_data.to_csv(os.path.join(output_directory, 'test_data.csv'), index=False)
    y_pred = predictor.predict(test_data.drop(columns=[label]))
    results = predictor.evaluate_predictions(y_true=test_data[label], y_pred=y_pred, auxiliary_metrics=True)
    size_test = len(test_data)

    
    print(results)

    sizett = {'len_train' :size_train, 'len_test':size_test  }
    results.update(sizett)

    save_results(results, output_directory)
    res = predictor.leaderboard(test_data)
    res.to_csv(os.path.join(output_directory, 'leaderboard_results.csv'))

    pred = predictor.feature_importance(test_data)
    pred.to_csv(os.path.join(output_directory, 'feature_importance.csv'))



if __name__ == '__main__':
    main()



# export DATA_PATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_input/final_V1_ml_data.csv'
# export OUTPUT_PATH='/Volumes/T9/Data_downloads/new-data-outputs/ml/results'
# export MODEL_PRESET='medium_quality'
# export TIME_LIM=5000
# export TRAIN_SUBSET_PROP=0.4
# export TARGET='totalgas'
# export COL_SETTING=0
# export RUN_REGIONAL='Yes'
# export run_census="No"
# export REGION_ID='NW'
# export RUN_GAS_FILTER='Yes'
# export GAS_THRESHOLD=5