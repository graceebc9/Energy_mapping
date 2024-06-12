import os
import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import matplotlib.pyplot as plt
from autogluon.tabular.visualizer import PartialDependencePlotter
import scipy.stats as stats
from ml_utils.src.model_col_final import settings_dict, settings_col_dict_census

def find_file_by_pattern(directory, pattern):
    """Find a file in a directory that matches the given pattern."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern in file:
                return os.path.join(root, file)
    return None

def transform(df, label, col_setting, setting_dict):
    cols = setting_dict[col_setting][1]
    working_cols = cols + [label]
    df = df[working_cols]
    df = df[~df[label].isna()]
    return df

# Read environment variables
model_dir = os.getenv('MODEL_DIR')
output_path = os.getenv('OUTPUT_PATH')
fp_path = os.getenv('FP_PATH')

if not model_dir or not output_path or not fp_path:
    raise ValueError("Please set the MODEL_DIR, OUTPUT_PATH, and FP_PATH environment variables.")

# Ensure the output path exists
os.makedirs(output_path, exist_ok=True)

# Find the model and test data paths
model_path = find_file_by_pattern(model_dir, 'model')
test_path = find_file_by_pattern(model_dir, 'test_data.csv')

if not model_path or not test_path:
    raise ValueError("Could not find model or test data files in the specified directory.")

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
# Identify top important features
top_features = feature_importance.index[:5]  # Adjust number of top features as needed

# Generate Partial Dependence Plots for top features
pdp = PartialDependencePlotter(predictor, dataset=test_data.drop(columns=[label]))

for feature in top_features:
    plt.figure(figsize=(10, 6))
    pdp.plot_partial_dependence(feature)
    plt.title(f'Partial Dependence Plot for {feature}')
    plt.savefig(os.path.join(output_path, f'pdp_{feature}.png'))
    plt.close()

# Example environment variable exports:
# export MODEL_DIR='/path/to/your/model/and/test/data/directory'
# export OUTPUT_PATH='/path/to/output/directory'
# export FP_PATH='/path/to/feature_importance.csv'

