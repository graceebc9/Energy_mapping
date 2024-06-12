import os
import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from ml_utils.src.model_col_final import settings_dict, settings_col_dict_census

# Ensure paths are provided via environment variables
path = os.getenv('MODEL_PATH')
test_path = os.getenv('TEST_PATH')
output_path = os.getenv('OUTPUT_PATH')

if not path or not test_path or not output_path:
    raise ValueError("Please set the MODEL_PATH, TEST_PATH, and OUTPUT_PATH environment variables.")

# Ensure the output path exists
os.makedirs(output_path, exist_ok=True)

# Load the predictor
predictor = TabularPredictor.load(path)

# Load the test data
test = pd.read_csv(test_path)

def transform(df, label, col_setting, settting_dict ):
    cols = settting_dict[col_setting][1]
    working_cols = cols + [label]
    df = df[working_cols]
    df = df[~df[label].isna()]
    return df





label = 'total_gas'
column_setting = 18
setting_dir = settings_dict
test_data = transform(TabularDataset(test), label, column_setting, setting_dir)

y_pred = predictor.predict(test_data.drop(columns=[label]))
y_true = test_data[label]

results = predictor.evaluate_predictions(y_true=y_true, y_pred=y_pred, auxiliary_metrics=True)
print(results)

# Assuming y_pred and y_true are your predicted and actual values
residuals = y_true - y_pred

# Create and save the residual plot
plt.figure(figsize=(10, 6))
sns.residplot(x=y_pred, y=residuals, lowess=True, color="g")
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.savefig(os.path.join(output_path, 'residual_plot.png'))
plt.close()

# Create and save the Predicted vs Actual plot
plt.figure(figsize=(10, 6))
plt.scatter(y_true, y_pred, edgecolor='k', alpha=0.7, s=70)
plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predicted vs Actual')
plt.savefig(os.path.join(output_path, 'predicted_vs_actual.png'))
plt.close()

# Create and save the distribution plot of residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color="b")
plt.xlabel('Residuals')
plt.title('Distribution of Residuals')
plt.savefig(os.path.join(output_path, 'distribution_of_residuals.png'))
plt.close()

# Create and save the error histogram
plt.figure(figsize=(10, 6))
plt.hist(residuals, bins=30, edgecolor='k')
plt.xlabel('Error')
plt.ylabel('Frequency')
plt.title('Error Histogram')
plt.savefig(os.path.join(output_path, 'error_histogram.png'))
plt.close()

# Create and save the Q-Q plot
plt.figure(figsize=(10, 6))
stats.probplot(residuals, dist="norm", plot=plt)
plt.title('Q-Q Plot')
plt.savefig(os.path.join(output_path, 'qq_plot.png'))
plt.close()


# export MODEL_PATH='/Volumes/T9/Data_downloads/new-data-outputs/ml/results/final_V1_ml_data__global__total_gas__500__colset_0__medium_quality___tsp_0.4__None__None'
# export TEST_PATH='/Users/gracecolverd/Downloads/test_data.csv'
# export output_path='/Volumes/T9/Data_downloads/new-data-outputs/ml/results/vis'