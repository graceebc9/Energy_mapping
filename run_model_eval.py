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

# Load the test data
test = pd.read_csv(test_path)

# Transform the data
label = 'total_gas'
column_setting = 18
setting_dir = settings_dict
test_data = transform(TabularDataset(test), label, column_setting, setting_dir)

# Predict and evaluate
y_pred = predictor.predict(test_data.drop(columns=[label]))
y_true = test_data[label]

results = predictor.evaluate_predictions(y_true=y_true, y_pred=y_pred, auxiliary_metrics=True)
print(results)

# Generate and save plots
residuals = y_true - y_pred

# Residual Plot
plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals, alpha=0.7, color="g")
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.savefig(os.path.join(output_path, 'residual_plot.png'))
plt.close()

# Predicted vs Actual Plot
plt.figure(figsize=(10, 6))
plt.scatter(y_true, y_pred, edgecolor='k', alpha=0.7, s=70)
plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predicted vs Actual')
plt.savefig(os.path.join(output_path, 'predicted_vs_actual.png'))
plt.close()

# Distribution of Residuals
plt.figure(figsize=(10, 6))
plt.hist(residuals, bins=30, color="b", edgecolor='k', alpha=0.7)
plt.xlabel('Residuals')
plt.title('Distribution of Residuals')
plt.savefig(os.path.join(output_path, 'distribution_of_residuals.png'))
plt.close()

# Error Histogram
plt.figure(figsize=(10, 6))
plt.hist(residuals, bins=30, edgecolor='k', alpha=0.7)
plt.xlabel('Error')
plt.ylabel('Frequency')
plt.title('Error Histogram')
plt.savefig(os.path.join(output_path, 'error_histogram.png'))
plt.close()

# Q-Q Plot
plt.figure(figsize=(10, 6))
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Q-Q Plot')
plt.savefig(os.path.join(output_path, 'qq_plot.png'))
plt.close()

# Load feature importance
feature_importance = pd.read_csv(fp_path, index_col=0)
print(feature_importance)

# Generate Partial Dependence Plots for top features
plt.figure(figsize=(10, 6))
feature_importance.iloc[0:5, :].plot(x='Variable', y='importance', kind='bar')
plt.title('Feature Importance')
plt.ylabel('Importance')
plt.xticks(rotation=45,ha='right' )
plt.savefig(os.path.join(output_path, 'feat_imp.png'))
plt.close()


# Example environment variable exports:
# export MODEL_PATH='/path/to/your/model/directory'
# export OUTPUT_PATH='/path/to/output/directory'
# export FP_PATH='/path/to/feature_importance.csv'

# Example environment variable exports:
# export MODEL_DIR='/path/to/your/model/and/test/data/directory'
# export OUTPUT_PATH='/path/to/output/directory'
# export FP_PATH='/path/to/feature_importance.csv'

