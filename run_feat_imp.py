import os
import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import matplotlib.pyplot as plt

import scipy.stats as stats
from ml_utils.src.model_col_final import settings_dict, settings_col_dict_census

def transform(df, label, col_setting, setting_dict):
    cols = setting_dict[col_setting][1]
    working_cols = cols + [label]
    df = df[working_cols]
    df = df[~df[label].isna()]
    return df

# Read environment variables
# model_path = os.getenv('MODEL_PATH')
col_setting = os.getenv('COL_SETTING')
label = 'total_gas'
model_path= f'/home/gb669/rds/hpc-work/energy_map/data/automl_models/results_final/final_V1_ml_data__global__total_gas__25000__colset_{col_setting}__best_quality___tsp_1.0__all__None'

fp_path = os.path.join(model_path, 'feature_importance.csv')
output_path = os.path.join(model_path, 'model_evals')

# Ensure the output path exists
os.makedirs(output_path, exist_ok=True)

# Construct the paths for test data and model evaluations
test_path = os.path.join(model_path, 'test_data.csv')


if not os.path.exists(test_path):
    raise ValueError(f"Test data file not found at {test_path}")

# Load the predictor
predictor = TabularPredictor.load(model_path)

if os.path.exists(fp_path):
    raise ValueError('Feature importance already exists')
# # Load the test data
test = pd.read_csv(test_path)

# Transform the data

setting_dir = settings_dict
test_data = transform(TabularDataset(test), label, col_setting, setting_dir)

        
pred = predictor.feature_importance(test_data)
pred.to_csv(fp_path) 
