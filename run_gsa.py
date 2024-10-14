
import numpy as np
from SALib.sample import morris as morris_sample
from SALib.analyze import morris
from SALib.sample import saltelli
from SALib.analyze import sobol
import matplotlib.pyplot as plt
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import matplotlib.pyplot as plt

import scipy.stats as stats
from ml_utils.src.model_col_final import settings_dict, settings_col_dict_census



# Read environment variables
# model_path = os.getenv('MODEL_PATH')
col_setting = os.getenv('COL_SETTING')
model_path= f'/home/gb669/rds/hpc-work/energy_map/data/automl_models/results_final/final_V1_ml_data__global__total_gas__25000__colset_{col_setting}__best_quality___tsp_1.0__all__None'

output_path = os.path.join(model_path, 'GSA')
# Ensure the output path exists
os.makedirs(output_path, exist_ok=True)


# Load the predictor
predictor = TabularPredictor.load(model_path)

# Transform the data
label = 'total_gas'
column_setting = 44
setting_dir = settings_dict

y_pred = predictor.predict(test_data.drop(columns=[label]))

# Model function that uses AutoGluon predictor
def model_function(X):
    # Convert the parameter array to a DataFrame
    df = pd.DataFrame(X, columns=problem['names'])
    
    # Make predictions using the AutoGluon model
    y_pred = predictor.predict(df)
    
    return y_pred.values

# Step 1: Morris Method (screening)
def run_morris_analysis():
    # Generate samples
    param_values = morris_sample.sample(problem, N=1000, num_levels=4)
    
    # Run model
    Y = model_function(param_values)
    
    # Perform analysis
    morris_results = morris.analyze(problem, param_values, Y, conf_level=0.95, print_to_console=True)
    
    return morris_results

# Step 2: Sobol Analysis (for top influential parameters)
def run_sobol_analysis(top_params=10):
    # Update problem with top parameters
    reduced_problem = {
        'num_vars': top_params,
        'names': problem['names'][:top_params],
        'bounds': problem['bounds'][:top_params]
    }
    
    # Generate samples
    param_values = saltelli.sample(reduced_problem, 1024)
    
    # Run model
    Y = model_function(param_values)
    
    # Perform analysis
    sobol_results = sobol.analyze(reduced_problem, Y, print_to_console=True)
    
    return sobol_results

# Run Morris Method
morris_results = run_morris_analysis()

 


# Save results to CSV
def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(os.path.join(output_path, filename), index=False)
    print(f"Results saved to {filename}")

# Plot and save Morris results
def plot_morris_results(results):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(results['mu_star'], results['sigma'])
    for i, txt in enumerate(problem['names']):
        ax.annotate(txt, (results['mu_star'][i], results['sigma'][i]))
    ax.set_xlabel('mu_star')
    ax.set_ylabel('sigma')
    ax.set_title('Morris Method Results')
    plt.savefig(os.path.join(output_path, 'morris_results_plot.png'))
    plt.close()
    print("Morris plot saved as morris_results_plot.png")

# Plot and save Sobol results
def plot_sobol_results(results, reduced_problem):
    fig, ax = plt.subplots(figsize=(10, 6))
    indices = results['S1']
    indices_names = reduced_problem['names']
    
    ax.bar(range(len(indices)), indices)
    ax.set_xticks(range(len(indices)))
    ax.set_xticklabels(indices_names, rotation=45)
    ax.set_ylabel('First Order Sensitivity Index')
    ax.set_title('Sobol First Order Indices')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'sobol_results_plot.png'))
    plt.close()
    print("Sobol plot saved as sobol_results_plot.png")


save_results_to_csv(morris_results, 'morris_results.csv')
plot_morris_results(morris_results)



# Select top influential parameters based on mu_star
top_params = 10
top_indices = np.argsort(morris_results['mu_star'])[-top_params:]

# Update problem for Sobol analysis
reduced_problem = {
    'num_vars': top_params,
    'names': [problem['names'][i] for i in top_indices],
    'bounds': [problem['bounds'][i] for i in top_indices]
}

# Run Sobol analysis on reduced problem
sobol_results = run_sobol_analysis(top_params)
save_results_to_csv(sobol_results, 'sobol_results.csv')
plot_sobol_results(sobol_results)

# Save problem configuration
with open(os.path.join(output_path, 'problem_config.json'), 'w') as f:
    json.dump(problem, f, indent=4)
print("Problem configuration saved as problem_config.json")

print(f"All results have been saved in the '{output_path}' directory.")