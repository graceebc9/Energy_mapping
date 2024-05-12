import sys
import os
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor


from ml_utils.src.model_col_settings import settings_col_dict 


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


def transform(df, label, col_setting):
    cols = settings_col_dict[col_setting]
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
    tr_lab = 'v2'
    if target == 'avgas1':   
        label = 'av_gas_per_vol_v1'
    elif target == 'totalgas':
        label = 'total_gas'
    else:
        raise Exception('No target')


    excl_models = [] 

    if model_types == 'all':
        excl_models = []
    elif model_types=='set1':
        excl_models = ['KNN']

    print(f'starting model run for target {label}, time lim {time_limit}, col setting {column_setting}, model preset {model_preset} and train subset {train_subset_prop}' )

      # Proportion of data to use for training
    col_type ='allcols'



    if not data_path or not output_path or not data_path:
        print("Please set DATA_PATH and OUTPUT_PATH environment variables.")
        sys.exit(1)

    dataset_name = os.path.basename(data_path).split('.')[0].split('_tr')[0]
    output_directory = f"{output_path}/{dataset_name}__{label}__{time_limit}__colset_{column_setting}__{model_preset}__{col_type}_tsp_{train_subset_prop}_{model_types}_{tr_lab}"
    
    # Example usage:
    
    required_files = ['model_summary.txt', 'feature_importance.csv', 'leaderboard_results.csv']  # List of files you expect to exist
    
    
    # Check if output directory exists and has all required files
    if check_directory_and_files(output_directory, required_files):
        print(f"Directory {output_directory} already contains all necessary files. Exiting to prevent data overwrite.")
        sys.exit(0)
    else:
        # Create directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        print(f"Directory {output_directory} is ready for use.")


    df = pd.read_csv(data_path)
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
    train_data = transform(TabularDataset(train_data), label, column_setting )
    
    
    # Reduce the training dataset if needed
    if train_subset_prop != 1:
        train_subset, _ = train_test_split(train_data, test_size=1-train_subset_prop, random_state=42)
        # train_subset.to_csv(os.path.join(output_directory, 'train_subset.csv'), index=False)
    else:
        train_subset = train_data   
    
    predictor = TabularPredictor(label, path=output_directory).fit(train_subset, 
                                                                #    num_gpus=1,
                                                                time_limit=time_limit,
                                                                presets=model_preset,
                                                                excluded_model_types=excl_models)
    
    test_data = transform(TabularDataset(test_data), label, column_setting)
    test_data.to_csv(os.path.join(output_directory, 'test_data.csv'), index=False)
    y_pred = predictor.predict(test_data.drop(columns=[label]))
    results = predictor.evaluate_predictions(y_true=test_data[label], y_pred=y_pred, auxiliary_metrics=True)

    
    print(results)

    save_results(results, output_directory)
    res = predictor.leaderboard(test_data)
    res.to_csv(os.path.join(output_directory, 'leaderboard_results.csv'))

    pred = predictor.feature_importance(test_data)
    pred.to_csv(os.path.join(output_directory, 'feature_importance.csv'))



if __name__ == '__main__':
    main()



# export DATA_PATH='/Users/gracecolverd/New_dataset/ml_scripts/V2_ml_input_data.csv'
# export OUTPUT_PATH='/Volumes/T9/Data_downloads/new-data-outputs/ml/results'
# export MODEL_PRESET='medium_quality'
# export TIME_LIM=500
# export TRAIN_SUBSET_PROP=0.1
# export TARGET='avgas1'
# export COL_SETTING=1