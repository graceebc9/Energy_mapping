#!/usr/bin/env python3

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from SALib.sample import morris as morris_sampler
from SALib.analyze import morris

# Add the parent directory to the Python path
# sys.path.append('../')
from src.postcode_utils import load_onsud_data, load_ids_from_file

from src.fuel_calc import find_data_pc_joint, pre_process_building_data, calculate_postcode_attr_with_null_case, check_duplicate_primary_key, gen_nulls
 
# Constants
BATCH_PATH = '/home/gb669/rds/hpc-work/energy_map/data/batches_10k/WM/batch_0.txt'
BATCH_NAME = 'WM_batch_1'
PC_SHP_PATH = os.getenv('PC_SHP_PATH')
BUILDING_PATH = os.getenv('BUILDING_PATH')

BASE_PATH = '/home/gb669/rds/hpc-work/energy_map/data/sensitivty_analysis'
ONSUD_DATA = 'DEC_2022'
PC_COUNT =int(os.getenv('PC_COUNT'))
n_morris=int(os.getenv('N_MORRIS'))
overlap = False 

# Problem definition
PROBLEM = {
    'num_vars': 4,
    'names': ['MAX_THRESHOLD_FLOOR_HEIGHT', 'MIN_THRESH_FL_HEIGHT', 'height_multiplier', 'premise_area_multiplier'],
    'bounds': [[4.8, 5.8], [2.0, 2.4], [0.9, 1.1], [0.9, 1.1]]
}

def setup_paths():
    output_path = os.path.join(BASE_PATH, 'GSA', BATCH_NAME)
    os.makedirs(output_path, exist_ok=True)
    
    label = BATCH_PATH.split('/')[-2]
    batch_id = BATCH_PATH.split('/')[-1].split('.')[0].split('_')[-1]
    onsud_path = os.path.join(os.path.dirname(BATCH_PATH), f'onsud_{batch_id}.csv')
    
    return output_path, onsud_path

def stratified_postcode_sample(onsud_data, n_samples=1001):
    postcode_counts = onsud_data.groupby('POSTCODE').size().reset_index(name='UPRN_COUNT')
    postcode_counts['stratum'] = pd.qcut(postcode_counts['UPRN_COUNT'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    samples_per_stratum = n_samples // 5
    sampled_postcodes = []
    for stratum in postcode_counts['stratum'].unique():
        stratum_postcodes = postcode_counts[postcode_counts['stratum'] == stratum]['POSTCODE']
        sampled_postcodes.extend(stratum_postcodes.sample(n=samples_per_stratum, replace=True))
    
    if len(sampled_postcodes) < n_samples:
        additional_samples = n_samples - len(sampled_postcodes)
        sampled_postcodes.extend(postcode_counts['POSTCODE'].sample(n=additional_samples, replace=True))
    
    return pd.Series(sampled_postcodes)


def load_uprn_data(pc, onsud_data, INPUT_GPK ):
    """Process one postcode, deriving building attributes and electricity and fuel info.
    
    Inputs: 
    
    pc: postcode 
    onsud_data: output of find_postcode_for_ONSUD_file, tuples of data, pc_shp 
    gas_df: gas uk gov data
    elec_df: uk goc elec data 
    INPUT_GPK: building file verisk 
    overlap: bool, is this for the overlapping postcodes? 
    batch_dir = needed for overlap - where are the batche stored?
    path_to_schp: path to postcode shapefiles location , needed for overlap 
    """
    pc = pc.strip() 
    if overlap ==True: 
        print('starting overlap pc')
        onsud_data = custom_load_onsud(pc, batch_dir)
        print('finding pc')
        onsud_data = find_postcode_for_ONSUD_file(onsud_data, path_to_pcshp )
        print('pc found')
    
    print('finding uprn')
    uprn_match= find_data_pc_joint(pc, onsud_data, input_gpk=INPUT_GPK)
    return uprn_match 


def process_uprn_match_df(uprn_match,  MIN_THRESH_FL_HEIGHT, MAX_THRESHOLD_FLOOR_HEIGHT ):

    if uprn_match is None  or len(uprn_match)==0:
        print('Empty uprn match')
        dc =  gen_nulls()
        print(len(dc) ) 
    else:
        print('starting data pre process')
        df  = pre_process_building_data(uprn_match, MIN_THRESH_FL_HEIGHT, MAX_THRESHOLD_FLOOR_HEIGHT)    
        print('pre process complete')
        if len(df)!=len(uprn_match):
            raise Exception('Error in pre process - some cols dropped? ')
        dc = calculate_postcode_attr_with_null_case(df)
        if df is not None:
            if check_duplicate_primary_key(df, 'upn'):
                print('Duplicate primary key found for upn')
                sys.exit()
    return dc 



def wrapper_function(X, pc, onsud_data, INPUT_GPK, target_col):
    """Wrapper function for the postcode processing model."""
    MAX_THRESHOLD_FLOOR_HEIGHT, MIN_THRESH_FL_HEIGHT, height_multiplier, premise_area_multiplier = X
    # Load original UPRN data
    original_uprn = load_uprn_data(pc, onsud_data, INPUT_GPK)
    if original_uprn is None:
        print('Empty uprn match')
        return None

    # Create a copy of the sampled data to modify
    modified_data = original_uprn.copy()
    
    # Apply multipliers to height and premise_area
    modified_data['height'] *= height_multiplier
    modified_data['premise_area'] *= premise_area_multiplier

    # Process the modified UPRN data
    result = process_uprn_match_df(modified_data, MIN_THRESH_FL_HEIGHT, MAX_THRESHOLD_FLOOR_HEIGHT)
    
    # Calculate and return the output metric
    return result.get(target_col, 0)


def run_morris_analysis(pc, onsud_data, INPUT_GPK, target_col, N):
    param_values = morris_sampler.sample(PROBLEM, N=N, num_levels=4, optimal_trajectories=None)
    Y = np.array([wrapper_function(X, pc, onsud_data, INPUT_GPK, target_col) for X in param_values])
    return morris.analyze(PROBLEM, param_values, Y, conf_level=0.95, print_to_console=False)

def custom_horizontal_bar_plot(ax, data, sortby, unit):
    y_pos = np.arange(len(data['names']))
    sorted_indices = np.argsort(data[sortby])
    ax.barh(y_pos, [data[sortby][i] for i in sorted_indices], align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels([data['names'][i] for i in sorted_indices])
    ax.set_xlabel(f"{sortby} ({unit})")



def plot_and_save_results(df_summary, df_results, output_path, pc_count):
    # Original bar plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    custom_horizontal_bar_plot(ax1, 
                               {'names': PROBLEM['names'], 'mu_star': df_summary['mean_mu_star'].values}, 
                               sortby='mu_star', 
                               unit="Mean Heated Volume")
    custom_horizontal_bar_plot(ax2, 
                               {'names': PROBLEM['names'], 'sigma': df_summary['mean_sigma'].values}, 
                               sortby='sigma', 
                               unit="Mean Heated Volume")
    
    ax1.set_title("Overall Parameter Importance")
    ax2.set_title("Overall Parameter Interactions")
    plt.tight_layout()
    
    fig.savefig(os.path.join(output_path, f'morris_sensitivity_plot_pc_{pc_count}.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)

    # New scatter plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['r', 'g', 'b', 'c']
    for i, name in enumerate(PROBLEM['names']):
        mu_star_values = df_results[[col for col in df_results.columns if col.endswith('_mu_star')]].loc[name]
        sigma_values = df_results[[col for col in df_results.columns if col.endswith('_sigma')]].loc[name]
        
        ax.scatter(mu_star_values, sigma_values, c=colors[i], label=name, alpha=0.6)
        
        # Plot mean point
        mean_mu_star = df_summary.loc[name, 'mean_mu_star']
        mean_sigma = df_summary.loc[name, 'mean_sigma']
        ax.scatter(mean_mu_star, mean_sigma, c=colors[i], s=100, marker='*', edgecolors='black')
        
        # Plot error bars
        std_mu_star = df_summary.loc[name, 'std_mu_star']
        std_sigma = df_summary.loc[name, 'std_sigma']
        ax.errorbar(mean_mu_star, mean_sigma, xerr=std_mu_star, yerr=std_sigma, c=colors[i], capsize=5)

    ax.set_xlabel(r'$\mu^*$')
    ax.set_ylabel(r'$\sigma$')
    ax.set_title(r'Morris Sensitivity Analysis: $\mu^*$ vs $\sigma$')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    fig.savefig(os.path.join(output_path, f'morris_sensitivity_scatter_pc_{pc_count}__nmorris_{n_morris}.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)


def main():
    output_path, onsud_path = setup_paths()
    
    print('Non overlap starting')
    onsud_data_tuple = load_onsud_data(onsud_path, PC_SHP_PATH)
    batch_ids = load_ids_from_file(BATCH_PATH)
    
    onsud_data = onsud_data_tuple[0]
    sampled_postcodes = stratified_postcode_sample(onsud_data, n_samples=1000)
    sampled_data = onsud_data[onsud_data['POSTCODE'].isin(sampled_postcodes)]
    
    print(f"Number of sampled postcodes: {len(sampled_postcodes)}")
    print(f"Number of UPRNs in sampled data: {len(sampled_data)}")
    
    sampled_postcode_counts = sampled_data.groupby('POSTCODE').size().reset_index(name='UPRN_COUNT')
    print(sampled_postcode_counts['UPRN_COUNT'].describe())
    
    results = {}
    target_col = 'clean_res_heated_vol_h_total'
    
    for pc in sampled_postcodes[0:PC_COUNT]:
        results[pc] = run_morris_analysis(pc, onsud_data_tuple, BUILDING_PATH, target_col , N= n_morris)
    
    df_results = pd.DataFrame(index=PROBLEM['names'])
    for pc, result in results.items():
        df_results[f'{pc}_mu'] = result['mu']
        df_results[f'{pc}_mu_star'] = result['mu_star']
        df_results[f'{pc}_sigma'] = result['sigma']
    
    df_summary = pd.DataFrame({
        'mean_mu': df_results[[col for col in df_results.columns if col.endswith('_mu')]].mean(axis=1),
        'mean_mu_star': df_results[[col for col in df_results.columns if col.endswith('_mu_star')]].mean(axis=1),
        'mean_sigma': df_results[[col for col in df_results.columns if col.endswith('_sigma')]].mean(axis=1),
        'std_mu': df_results[[col for col in df_results.columns if col.endswith('_mu')]].std(axis=1),
        'std_mu_star': df_results[[col for col in df_results.columns if col.endswith('_mu_star')]].std(axis=1),
        'std_sigma': df_results[[col for col in df_results.columns if col.endswith('_sigma')]].std(axis=1),
    })
    
    print("Summary Statistics:")
    print(df_summary)
    
    plot_and_save_results(df_summary, df_results, output_path, PC_COUNT)
    
    df_results.to_csv(os.path.join(output_path, f'morris_sensitivity_results_pc_{PC_COUNT}__nmorris_{n_morris}.csv'))
    df_summary.to_csv(os.path.join(output_path, f'morris_sensitivity_summary_pc_{PC_COUNT}__nmorris_{n_morris}.csv'))
    
    print(f"Results and plot saved in {output_path}")

if __name__ == "__main__":
    main()