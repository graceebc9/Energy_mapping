import sys
import os
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor


import os
import sys

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



def transform(df, label):
    cols_remove = [
        'ï»¿pcd7', 'pcd8', 'pcds', 'dointr', 'doterm', 'usertype', 'oa21cd',
        'lsoa21cd', 'msoa21cd', 'ladcd', 'lsoa21nm', 'msoa21nm', 'ladnm',
        'ladnmw', 'pcd7', 'diff_min_max_gas_per_vol', 'diff_gas_meters_uprns_res',
        'min_gas_per_vol', 'max_gas_per_vol', 'total_gas', 'avg_gas', 'median_gas',
        'num_meters_gas', 'total_elec', 'avg_elec', 'median_elec', 'num_meters_elec',
        'comm_alltypes_count', 'unknown_alltypes', 'outb_res_uprn_count_total', 'mixed_total_buildings', 'mixed_premise_area_total', 'mixed_gross_area_total', 'mixed_heated_vol_fc_total', 'mixed_heated_vol_h_total', 'mixed_base_floor_total', 'mixed_basement_heated_vol_max_total', 'mixed_listed_bool_total', 'mixed_uprn_count_total', 'percent_residential', 'perc_all_res', 'Unknown_pct', 'ethnic_group_perc_Does not apply', 'household_siz_perc_perc_0 people in household', 'occupancy_rating_perc_Does not apply', 'household_comp_by_bedroom_perc_Does not apply_Does not apply', 'household_comp_by_bedroom_perc_Does not apply_1 bedroom', 'household_comp_by_bedroom_perc_Does not apply_2 bedrooms', 'household_comp_by_bedroom_perc_Does not apply_3 bedrooms', 'household_comp_by_bedroom_perc_Does not apply_4 or more bedrooms', 'household_comp_by_bedroom_perc_One-person household_Does not apply', 'household_comp_by_bedroom_perc_Single family household: All aged 66 years and over_Does not apply', 'household_comp_by_bedroom_perc_Single family household: Couple family household_Does not apply', 'household_comp_by_bedroom_perc_Single family household: Lone parent household_Does not apply', 'household_comp_by_bedroom_perc_Other household types_Does not apply', 'central_heating_perc_Does not apply'
    ]
    working_cols = [col for col in df.columns if col not in cols_remove]
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
    
    label = 'av_gas_per_vol'
    target_var='avgas'    
    model_names ='all'

    print(f'starting model run for {target_var}, time lim {time_limit}, model preset {model_preset} adn train subset {train_subset_prop}' )

      # Proportion of data to use for training
    col_type ='allcols'



    if not data_path or not output_path:
        print("Please set DATA_PATH and OUTPUT_PATH environment variables.")
        sys.exit(1)

    dataset_name = os.path.basename(data_path).split('.')[0]
    output_directory = f"{output_path}/{dataset_name}_{target_var}_{time_limit}_{model_preset}_{col_type}_tsp_{train_subset_prop}_{model_names}"
    
    # Example usage:
    
    required_files = ['model_summary.txt', 'feature_importance.csv', 'leaderboard_results.csv']  # List of files you expect to exist
    excluded_model_types = ['KNeighborsDist_BAG_L1', 'KNeighborsUnif_BAG_L1','LightGBMXT_BAG_L1','LightGBM_BAG_L1']
    
    # Check if output directory exists and has all required files
    if check_directory_and_files(output_directory, required_files):
        print(f"Directory {output_directory} already contains all necessary files. Exiting to prevent data overwrite.")
        sys.exit(0)
    else:
        # Create directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        print(f"Directory {output_directory} is ready for use.")
        # model_dir = os.path.join(output_directory, 'models')
        # existing_models = os.listdir(model_dir)
        # # filter to only dirs within the dir 
        # existing_models = [x for x in existing_models if os.path.isdir(os.path.join(model_dir, x))]
        # excluded_model_types += existing_models
    

    df = pd.read_csv(data_path)
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
    train_data = transform(TabularDataset(train_data), label)
    
    # Reduce the training dataset if needed
    if train_subset_prop != 1:
        train_subset, _ = train_test_split(train_data, test_size=1-train_subset_prop, random_state=42)
    else:
        train_subset = train_data   
    
    predictor = TabularPredictor(label, path=output_directory).fit(train_subset, 
                                                                #    num_gpus=1,
                                                                time_limit=time_limit,
                                                                presets=model_preset,
                                                                excluded_model_types=excluded_model_types)
    
    test_data = transform(TabularDataset(test_data), label)
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



# export DATA_PATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_data_engwales_census_v2.csv'
# export OUTPUT_PATH='/Volumes/T9/Data_downloads/new-data-outputs/ml/results'
# export MODEL_PRESET='medium_quality'
# export TIME_LIM=500
# export TRAIN_SUBSET_PROP=0.1