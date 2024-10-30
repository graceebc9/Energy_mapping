import os
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from SALib.sample import saltelli

from SALib.analyze import sobol
from autogluon.tabular import TabularPredictor
import seaborn as sns 

from ml_utils.src.problem_definitions import get_problem, group_mapping, check_and_enforce_heating_volume_constraint, enforce_heating_volume_constraint, enforce_pc_area

# Configuration
col_setting = int(os.getenv('COL_SETTING'))
folder = os.getenv('MODEL_FOLDER')
dataset_name = 'clean_v1_round2_secondfilter'
if folder is None:
    if col_setting==47:
        folder='results_47'
    else:
        folder='results_cl_v2'
    
region = os.getenv('REGION')
label = os.getenv('LABEL')
if label is None:
    label = 'total_gas'
model_path= f'/home/gb669/rds/hpc-work/energy_map/data/automl_models/{folder}/{dataset_name}__local_{label}__25000__colset_{col_setting}__best_quality___tsp_1.0__all__{region}'

if region ==False or region is None:
    model_path= f'/home/gb669/rds/hpc-work/energy_map/data/automl_models/{folder}/{dataset_name}__global__{label}__25000__colset_{col_setting}__best_quality___tsp_1.0__all__None'
else:
    model_path= f'/home/gb669/rds/hpc-work/energy_map/data/automl_models/{folder}/{dataset_name}__local__{label}__25000__colset_{col_setting}__best_quality___tsp_1.0__all__{region}'
print(model_path)

# New output path structure
BASE_OUTPUT_PATH = f'/home/gb669/rds/hpc-work/energy_map/data/sobol_results/second_ranges/{label}'
os.makedirs(BASE_OUTPUT_PATH, exist_ok=True)

# Number of samples for Sobol analysis
N = int(os.getenv('N', 1024))
grouped = os.getenv('GROUPED', 'False').lower() == 'true'
print('grouped value is ', grouped )


def remove_groups_from_problem(problem):
    # Create a new dict with all keys except 'groups'
    return {k: v for k, v in problem.items() if k != 'groups'}

# Usage:



problem = get_problem(col_setting, grouped)
if grouped is False:
    problem = remove_groups_from_problem(problem)


print('num vars' , problem['num_vars'])
print('var names' , problem['names'])
print('bounds' , problem['bounds'])
print('keys' , problem.keys())

# Load the predictor
print('Loading predictor')
predictor = TabularPredictor.load(model_path, require_version_match=True)

def model_function(X):
    df = pd.DataFrame(X, columns=problem['names'])
    try:
        predictions = predictor.predict(df).values
        if np.any(np.isnan(predictions)) or np.any(np.isinf(predictions)):
            print(f"Warning: NaN or Inf in predictions for inputs: {df.iloc[np.isnan(predictions) | np.isinf(predictions)]}")
        return predictions
    except Exception as e:
        print(f"Error in model prediction: {e}")
        return np.full(len(X), np.nan)

def run_sobol_analysis(N):
    param_values = saltelli.sample(problem, N)
    print(param_values)
    # Check if constraint is satisfied
    is_satisfied, difference, expected = check_and_enforce_heating_volume_constraint(param_values, problem)
    print(f"Constraint satisfied: {is_satisfied}")
    print(f"Difference: {difference}")
    print(f"Expected clean_res_heated_vol_h_total: {expected}")

    # Enforce the constraint
    param_values = enforce_heating_volume_constraint(param_values, problem)
    param_values = enforce_pc_area(param_values, problem)
    
    
    Y = model_function(param_values)
    if np.any(np.isnan(Y)) or np.any(np.isinf(Y)):
        print(f"Warning: {np.sum(np.isnan(Y))} NaN and {np.sum(np.isinf(Y))} Inf values in model output")
    return sobol.analyze(problem, Y, print_to_console=True)

def save_results_to_csv_sobol(results, output_path, problem):
    if 'groups' in problem:
        # For grouped analysis
        unique_groups = list(dict.fromkeys(problem['groups']))
        S1_df = pd.DataFrame({'parameter': unique_groups, 'S1': results['S1'], 'S1_conf': results['S1_conf']})
        ST_df = pd.DataFrame({'parameter': unique_groups, 'ST': results['ST'], 'ST_conf': results['ST_conf']})
        
        # Create S2 data for grouped analysis
        s2_data = []
        for i, group1 in enumerate(unique_groups):
            for j, group2 in enumerate(unique_groups):
                s2_data.append({
                    'group1': group1,
                    'group2': group2,
                    'S2': results['S2'][i][j],
                    'S2_conf': results['S2_conf'][i][j]
                })
        S2_df = pd.DataFrame(s2_data)
        S2_df.to_csv(os.path.join(output_path, 'sobol_S2_results.csv'), index=False)
    else:
        # For non-grouped analysis
        S1_df = pd.DataFrame({'parameter': problem['names'], 'S1': results['S1'], 'S1_conf': results['S1_conf']})
        ST_df = pd.DataFrame({'parameter': problem['names'], 'ST': results['ST'], 'ST_conf': results['ST_conf']})
        
        # Create S2 data for non-grouped analysis
        n_params = len(problem['names'])
        s2_data = []
        for i in range(n_params):
            for j in range(n_params):
                s2_data.append({
                    'param1_name': problem['names'][i],
                    'param2_name': problem['names'][j],
                    'S2': results['S2'][i][j],
                    'S2_conf': results['S2_conf'][i][j]
                })
        S2_df = pd.DataFrame(s2_data)
        S2_df.to_csv(os.path.join(output_path, 'sobol_S2_results.csv'), index=False)

    S1_df.to_csv(os.path.join(output_path, 'sobol_S1_results.csv'), index=False)
    ST_df.to_csv(os.path.join(output_path, 'sobol_ST_results.csv'), index=False)
    
    return S1_df, ST_df

def plot_sobol_results(results, output_path):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))
    
    ax1.bar(range(len(results['S1'])), results['S1'])
    ax1.set_xticks(range(len(results['S1'])))
    ax1.set_xticklabels(problem['names'], rotation=45, ha='right')
    ax1.set_ylabel('First Order Sensitivity Index')
    ax1.set_title('Sobol First Order Indices')
    
    ax2.bar(range(len(results['ST'])), results['ST'])
    ax2.set_xticks(range(len(results['ST'])))
    ax2.set_xticklabels(problem['names'], rotation=45, ha='right')
    ax2.set_ylabel('Total Order Sensitivity Index')
    ax2.set_title('Sobol Total Order Indices')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'sobol_results_plot.png'))
    plt.close()
    print(f"Sobol plot saved in {output_path}")

def plot_sobol_heatmap(results, output_path, problem):
    S2_matrix = results['S2']
    
    if 'groups' in problem:
        # For grouped analysis
        labels = list(dict.fromkeys(problem['groups']))
    else:
        # For non-grouped analysis
        labels = problem['names']
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(S2_matrix, annot=True, cmap='YlOrRd', xticklabels=labels, yticklabels=labels)
    np.savetxt(os.path.join(output_path, 'sobol_S2_results.csv'), S2_matrix, delimiter=',')
    plt.title('Sobol Second-Order Indices')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'sobol_S2_heatmap.png'))
    plt.close()
    print(f"Sobol S2 heatmap saved in {output_path}")


def plot_sobol_indices(s1_data, st_data, output_path, problem):
    # Function to shorten parameter names
    def shorten_param_name(name):
        replacements = {
            'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British': 'Pct White',
            'central_heating_perc_Mains gas only': 'Pct Gas Heating',
            'household_siz_perc_perc_1 person in household': 'Pct 1 Person Household',
            '2 storeys terraces with t rear extension_pct': 'Pct 2storey terraces'
        }
        return replacements.get(name, name)

    # Shorten parameter names
    if 'groups' in problem:
        s1_data['real_name'] = [group_mapping[x] for x in s1_data['parameter']]
        st_data['real_name'] = [group_mapping[x] for x in st_data['parameter']]
        print('cont')
    else:
        s1_data['parameter'] = s1_data['parameter'].apply(shorten_param_name)
        st_data['parameter'] = st_data['parameter'].apply(shorten_param_name)

    # Get unique parameters correctly
    all_parameters = sorted(set(s1_data['parameter'].tolist()).union(set(st_data['parameter'].tolist())))
    color_palette = sns.color_palette("husl", len(all_parameters))
    color_dict = dict(zip(all_parameters, color_palette))

    # Sort data by effect size
    s1_data = s1_data.sort_values('S1', ascending=True)
    st_data = st_data.sort_values('ST', ascending=True)

    # Create figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12))
    
    if 'groups' in problem:
        plot_col = 'real_name'
    else:
        plot_col = 'parameter'
        
    # Plot S1 indices
    for _, row in s1_data.iterrows():
        ax1.barh(row[plot_col], row['S1'], xerr=row['S1_conf'], 
                 alpha=0.7, capsize=5, color=color_dict[row['parameter']], ecolor='black')
    ax1.set_title('First-order (S1) Sobol Indices')
    ax1.set_xlabel('S1 Index')

    # Plot ST indices
    for _, row in st_data.iterrows():
        ax2.barh(row[plot_col], row['ST'], xerr=row['ST_conf'], 
                 alpha=0.7, capsize=5, color=color_dict[row['parameter']], ecolor='black')
    ax2.set_title('Total-order (ST) Sobol Indices')
    ax2.set_xlabel('ST Index')

    # Set consistent x-axis limits
    max_value = max(s1_data['S1'].max(), st_data['ST'].max())
    ax1.set_xlim(0, max_value * 1.1)
    ax2.set_xlim(0, max_value * 1.1)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'sobol_indices_plot.png'))
    plt.close()
    print(f"Sobol indices plot saved in {output_path}")

    # Print top 5 S1 and ST indices
    print("Top 5 S1 indices:")
    top_s1 = s1_data.nlargest(5, 'S1')
    for _, row in top_s1.iterrows():
        print(f"{row['parameter']}: {row['S1']:.6f} (conf: ±{row['S1_conf']:.6f})")

    print("\nTop 5 ST indices:")
    top_st = st_data.nlargest(5, 'ST')
    for _, row in top_st.iterrows():
        print(f"{row['parameter']}: {row['ST']:.6f} (conf: ±{row['ST_conf']:.6f})")
        
        
        
if __name__ == "__main__":
    # Start timing
    start_time = time.time()

    # Create subfolder for results
    result_folder = os.path.join(BASE_OUTPUT_PATH, folder, f'colset_{col_setting}', 'grouped' if grouped else 'ungrouped', f'N{N}')
    if region is not False and region is not None:
        result_folder = os.path.join(result_folder, region)
    
    os.makedirs(result_folder, exist_ok=True)

    print(f'Starting Sobol analysis with N={N}')
    sobol_results = run_sobol_analysis(N)
    print('Sobol results are in this form: ', sobol_results)
    print('sobol keys', sobol_results.keys() ) 
    print('Saving Sobol results')
    s1_data, st_data = save_results_to_csv_sobol(sobol_results, result_folder, problem)
    
    print('Plotting Sobol results')
     #plot_sobol_results(sobol_results, result_folder)
    plot_sobol_heatmap(sobol_results, result_folder, problem)
    plot_sobol_indices(s1_data, st_data, result_folder, problem)
    
    # Save problem configuration
    with open(os.path.join(result_folder, 'problem_config.json'), 'w') as f:
        json.dump(problem, f, indent=4)
    print("Problem configuration saved as problem_config.json")

    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")

    # Save execution time to a file
    with open(os.path.join(result_folder, 'execution_time.txt'), 'w') as f:
        f.write(f"Execution time: {execution_time:.2f} seconds")

    print(f"All results have been saved in the '{result_folder}' directory.")