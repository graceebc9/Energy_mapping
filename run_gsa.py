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

# Configuration
col_setting = int(os.getenv('COL_SETTING'))
folder = os.getenv('MODEL_FOLDER')
if folder is None:
    folder = 'results_cl_v2'
MODEL_PATH = f'/home/gb669/rds/hpc-work/energy_map/data/automl_models/{folder}/clean_v1_round2_secondfilter__global__total_gas__25000__colset_{col_setting}__best_quality___tsp_1.0__all__None'

# New output path structure
BASE_OUTPUT_PATH = '/home/gb669/rds/hpc-work/energy_map/data/sobol_results'
os.makedirs(BASE_OUTPUT_PATH, exist_ok=True)

# Number of samples for Sobol analysis
N = int(os.getenv('N', 1024))
grouped = os.getenv('GROUPED', 'False').lower() == 'true'


if col_setting == 45:
    problem = {
        'num_vars': 13,
        'names': [
            'all_res_heated_vol_h_total',
            'clean_res_total_buildings',
            'Domestic outbuilding_pct',
            'Standard size detached_pct',
            'Standard size semi detached_pct',
            'Pre 1919_pct',
            'Unknown_age_pct',
            'HDD',
            'CDD',
            'postcode_density',
            'log_pc_area',
            'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British',
            'central_heating_perc_Mains gas only'
        ],
        'bounds': [
            [0, 7600],  # all_res_heated_vol_h_total
            [0, 50],    # clean_res_total_buildings
            [0, 52],    # Domestic outbuilding_pct
            [0, 100],   # Standard size detached_pct
            [0, 100],   # Standard size semi detached_pct
            [0, 100],   # Pre 1919_pct
            [0, 20],    # Unknown_age_pct
            [30, 80],   # HDD
            [0, 8],     # CDD
            [0, 0.5],   # postcode_density
            [5, 12],    # log_pc_area
            [0, 1],     # ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British
            [0, 1]      # central_heating_perc_Mains gas only
        ]
    }
elif col_setting ==44:
    if grouped == False: 
        problem = {
        'num_vars': 26,
        'names': [
            'all_res_heated_vol_h_total',
            'clean_res_total_buildings',
            'clean_res_heated_vol_h_total',
            'Domestic outbuilding_pct',
            'Standard size detached_pct',
            'Standard size semi detached_pct',
            'Small low terraces_pct',
            '2 storeys terraces with t rear extension_pct',
            'Pre 1919_pct',
            'Unknown_age_pct',
            '1960-1979_pct',
            '1919-1944_pct',
            'Post 1999_pct',
            'HDD',
            'CDD',
            'HDD_summer',
            'HDD_winter',
            'postcode_area',
            'postcode_density',
            'log_pc_area',
            'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British',
            'central_heating_perc_Mains gas only',
            'household_siz_perc_perc_1 person in household',
            'Average Household Size',
            'clean_res_premise_area_total',
            'all_res_base_floor_total'
        ],
        'bounds': [
            [0, 7600],  # all_res_heated_vol_h_total (assumed range, adjust as needed)
            [0, 50],  # clean_res_total_buildings (assumed range, adjust as needed)
            [0, 7400],  # clean_res_heated_vol_h_total (assumed range, adjust as needed)
            [0, 52],    # Domestic outbuilding_pct
            [0, 100],    # Standard size detached_pct
            [0, 100],    # Standard size semi detached_pct
            [0, 100],    # Small low terraces_pct
            [0, 100],    # 2 storeys terraces with t rear extension_pct
            [0, 100],    # Pre 1919_pct
            [0, 20],    # Unknown_age_pct
            [0, 100],    # 1960-1979_pct
            [0, 100],    # 1919-1944_pct
            [0, 100],    # Post 1999_pct
            [30, 80], # HDD (Heating Degree Days, assumed range)
            [0, 8], # CDD (Cooling Degree Days, assumed range)
            [3, 15], # HDD_summer (assumed range)
            [30, 60], # HDD_winter (assumed range)
            [1, 26000], # postcode_area (assumed range in km^2)
            [0, 0.5], # postcode_density (assumed range in people/km^2)
            [5, 12],   # log_pc_area (assumed range for log of postcode area)
            [0, 1],    # ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British
            [0, 1],    # central_heating_perc_Mains gas only
            [0, 1],    # household_siz_perc_perc_1 person in household
            [1, 5],     # Average Household Size (assumed range)
            [0,2000],
            [0,1000]
            
        ]
         }
    else:
        problem = {
            'num_vars': 26,
            'groups': ['group_1', 'group_1','group_1', 'group_2', 'group_3', 'group_4', 'group_5',  'group_6', 'group_7', 'group_8', 'group_9', 
            'group_10', 'group_11', 'group_12', 'group_13',  'group_12', 'group_12' , 'group_14', 'group_15', 'group_14', 'group_15' , 
            'group_16', 'group_17', 'group_18', 'group_1', 'group_1'],
            'names': [
                'all_res_heated_vol_h_total',
                'clean_res_total_buildings',
                'clean_res_heated_vol_h_total',
                'Domestic outbuilding_pct',
                'Standard size detached_pct',
                'Standard size semi detached_pct',
                'Small low terraces_pct',
                '2 storeys terraces with t rear extension_pct',
                'Pre 1919_pct',
                'Unknown_age_pct',
                '1960-1979_pct',
                '1919-1944_pct',
                'Post 1999_pct',
                'HDD',
                'CDD',
                'HDD_summer',
                'HDD_winter',
                'postcode_area',
                'postcode_density',
                'log_pc_area',
                'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British',
                'central_heating_perc_Mains gas only',
                'household_siz_perc_perc_1 person in household',
                'Average Household Size',
                'clean_res_premise_area_total',
                'all_res_base_floor_total'
                
            ],
            'bounds': [
                [0, 7600],  # all_res_heated_vol_h_total (assumed range, adjust as needed)
                [0, 50],  # clean_res_total_buildings (assumed range, adjust as needed)
                [0, 7400],  # clean_res_heated_vol_h_total (assumed range, adjust as needed)
                [0, 52],    # Domestic outbuilding_pct
                [0, 100],    # Standard size detached_pct
                [0, 100],    # Standard size semi detached_pct
                [0, 100],    # Small low terraces_pct
                [0, 100],    # 2 storeys terraces with t rear extension_pct
                [0, 100],    # Pre 1919_pct
                [0, 20],    # Unknown_age_pct
                [0, 100],    # 1960-1979_pct
                [0, 100],    # 1919-1944_pct
                [0, 100],    # Post 1999_pct
                [30, 80], # HDD (Heating Degree Days, assumed range)
                [0, 8], # CDD (Cooling Degree Days, assumed range)
                [3, 15], # HDD_summer (assumed range)
                [30, 60], # HDD_winter (assumed range)
                [1, 26000], # postcode_area (assumed range in km^2)
                [0, 0.5], # postcode_density (assumed range in people/km^2)
                [5, 12],   # log_pc_area (assumed range for log of postcode area)
                [0, 1],    # ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British
                [0, 1],    # central_heating_perc_Mains gas only
                [0, 1],    # household_siz_perc_perc_1 person in household
                [1, 5],     # Average Household Size (assumed range)
                [0,2000],
                [0,1000]
                
            ]
        }
else:
    print('error no problem defined for col setting')

# Load the predictor
print('Loading predictor')
predictor = TabularPredictor.load(MODEL_PATH, require_version_match=True)

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
        S2_data = [{'parameter1': group1, 'parameter2': group2, 'S2': results['S2'][i][j-i-1], 'S2_conf': results['S2_conf'][i][j-i-1]}
                   for i, group1 in enumerate(unique_groups) for j, group2 in enumerate(unique_groups[i+1:], start=i+1)]
    else:
        # For non-grouped analysis
        S1_df = pd.DataFrame({'parameter': problem['names'], 'S1': results['S1'], 'S1_conf': results['S1_conf']})
        ST_df = pd.DataFrame({'parameter': problem['names'], 'ST': results['ST'], 'ST_conf': results['ST_conf']})
        S2_data = [{'parameter1': param1, 'parameter2': param2, 'S2': results['S2'][i][j-i-1], 'S2_conf': results['S2_conf'][i][j-i-1]}
                   for i, param1 in enumerate(problem['names']) for j, param2 in enumerate(problem['names'][i+1:], start=i+1)]
    
    S2_df = pd.DataFrame(S2_data)
    
    S1_df.to_csv(os.path.join(output_path, 'sobol_S1_results.csv'), index=False)
    ST_df.to_csv(os.path.join(output_path, 'sobol_ST_results.csv'), index=False)
    S2_df.to_csv(os.path.join(output_path, 'sobol_S2_results.csv'), index=False)
    print(f"Sobol results saved in {output_path}")
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
        s1_data['parameter'] = s1_data['parameter']
        st_data['parameter'] = st_data['parameter']
    else:
        s1_data['parameter'] = s1_data['parameter'].apply(shorten_param_name)
        st_data['parameter'] = st_data['parameter'].apply(shorten_param_name)

    # Get unique parameters and create a color mapping
    all_parameters = sorted(set(s1_data['parameter'].tolist() + st_data['parameter'].tolist()))
    color_palette = sns.color_palette("husl", len(all_parameters))
    color_dict = dict(zip(all_parameters, color_palette))

    # Sort data by effect size
    s1_data = s1_data.sort_values('S1', ascending=True)
    st_data = st_data.sort_values('ST', ascending=True)

    # Create figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12))

    # Plot S1 indices
    for _, row in s1_data.iterrows():
        ax1.barh(row['parameter'], row['S1'], xerr=row['S1_conf'], 
                 alpha=0.7, capsize=5, color=color_dict[row['parameter']], ecolor='black')
    ax1.set_title('First-order (S1) Sobol Indices')
    ax1.set_xlabel('S1 Index')

    # Plot ST indices
    for _, row in st_data.iterrows():
        ax2.barh(row['parameter'], row['ST'], xerr=row['ST_conf'], 
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
    os.makedirs(result_folder, exist_ok=True)

    print(f'Starting Sobol analysis with N={N}')
    sobol_results = run_sobol_analysis(N)

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