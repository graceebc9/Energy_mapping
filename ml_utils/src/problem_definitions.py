

    # problem_definitions.py
from .model_col_final import settings_dict
import numpy as np 

# Base dictionary of all possible parameters and their bounds
base_params = {
    'all_res_heated_vol_h_total': [0, 7600],
    'all_types_total_buildings': [0, 150],
    'clean_res_total_buildings': [0, 150],
    'all_res_total_buildings': [0, 150],
    'clean_res_heated_vol_h_total': [0, 7400],
    'Domestic outbuilding_pct': [0, 52],
    'Standard size detached_pct': [0, 100],
    'Standard size semi detached_pct': [0, 100],
    'Small low terraces_pct': [0, 100],
    '2 storeys terraces with t rear extension_pct': [0, 100],
    'Pre 1919_pct': [0, 100],
    'Unknown_age_pct': [0, 20],
    '1960-1979_pct': [0, 100],
    '1919-1944_pct': [0, 100],
    'Post 1999_pct': [0, 100],
    '1945-1959_pct': [0, 100],
    '1980-1989_pct': [0, 100],
    '1990-1999_pct': [0, 100],
    'Post 1999_pct': [0, 100],  
    'None_age_pct': [0, 15],
    'HDD': [30, 80],
    'CDD': [0, 8],
    'HDD_summer': [3, 15],
    'HDD_winter': [30, 60],
    'postcode_area': [1, 26000],
    'postcode_density': [0, 0.5],
    'log_pc_area': [5, 12],
    'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British': [0, 1],
    'central_heating_perc_Mains gas only': [0, 1],
    'household_siz_perc_perc_1 person in household': [0, 1],
    'Average Household Size': [1, 5],
    'clean_res_premise_area_total': [0, 2000],
    'all_res_premise_area_total': [0, 2000],
    'all_res_base_floor_total': [0, 1000]
}

problem_47 = {
    'num_vars': 18,
    'names': [
        'all_res_heated_vol_h_total',
        'clean_res_total_buildings',
        'clean_res_heated_vol_h_total',
        'Domestic outbuilding_pct',
        'Standard size detached_pct',
         'Standard size semi detached_pct',
        'Pre 1919_pct',
        'Unknown_age_pct',
        '1960-1979_pct',
        'HDD',
        'CDD',
        'HDD_winter',
        'postcode_area',
        'postcode_density',
        'log_pc_area',
        'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British',
         'central_heating_perc_Mains gas only',
         'Average Household Size'
    ],
    'bounds': [
        [738.73, 6824.35],
        [2.0, 43.0],
        [720.18, 6634.51],
        [0.0, 100.0],
        [0.0, 100.0],
        [0.0, 100.0],
        [0.0, 100.0],
        [0.0, 100.0],
        [0.0, 100.0],
        [46.26, 65.35],
        [0.0, 5.41],
        [39.67, 52.35],
        [1835.16, 35699.59],
        [0.045, 0.33],
        [7, 11],
        [0.0, 1.0],
        [0.0, 1.0],
        [1, 5]
    ],
    'groups': [
        'G1',     # all_res_heated_vol_h_total (corr: 0.996 with clean_res_heated_vol_h_total)
        'G2',     # clean_res_total_buildings (independent)
        'G1',     # clean_res_heated_vol_h_total
        'G3',     # Domestic_outbuilding_pct (independent)
        'G4',     # Standard_size_detached_pct (independent)
        'G5',     # Standard_size_semi_detached_pct (independent)
        'G6',     # Pre_1919_pct (independent)
        'G7',     # Unknown_age_pct (independent)
        'G8',     # age_1960_1979_pct (independent)
        'G9',     # HDD (corr: 0.979 with HDD_winter)
        'G10',    # CDD (independent)
        'G9',     # HDD_winter
        'G11',    # postcode_area (moderate correlations only)
        'G12',    # postcode_density (moderate correlations only)
        'G11',    # log_pc_area (moderate correlations only)
        'G14',    # ethnic_group_perc_White (independent)
        'G15',    # central_heating_perc_Mains_gas (independent)
        'G16'     # Average_Household_Size (independent)
    ]
}


problem_44 = {
    'num_vars': 25,
    'names': [
        'all_res_heated_vol_h_total',          # Same as 47
        'clean_res_total_buildings',           # Same as 47 
        'clean_res_heated_vol_h_total',        # Same as 47
        'clean_res_premise_area_total',        # New
        
        'Domestic outbuilding_pct',            # Same as 47
        'Standard size detached_pct',          # Same as 47
        'Standard size semi detached_pct',     # Same as 47
        'Small low terraces_pct',              # New
        '2 storeys terraces with t rear extension_pct', # New
        'Pre 1919_pct',                        # Same as 47
        'Unknown_age_pct',                     # Same as 47
        '1960-1979_pct',                       # Same as 47
        '1919-1944_pct',                       # New
        'Post 1999_pct',                       # New
        'HDD',                                 # Same as 47
        'CDD',                                 # Same as 47
        'HDD_summer',                          # New
        'HDD_winter',                          # Same as 47
        'postcode_area',                       # Same as 47
        'postcode_density',                    # Same as 47
        'log_pc_area',                         # Same as 47
        'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British', # Same as 47
        'central_heating_perc_Mains gas only', # Same as 47
        'household_siz_perc_perc_1 person in household', # New
        'Average Household Size'               # Same as 47
    ],
    'bounds': [
        [738.73, 6824.35],      # Copied from 47
        [2.0, 43.0],            # Copied from 47
        [720.18, 6634.51],      # Copied from 47
       [337.30, 3161.90],           
          
        [0.0, 100.0],           # Copied from 47
        [0.0, 100.0],           # Copied from 47
        [0.0, 100.0],           # Copied from 47
        [0.0, 100.0],           # New percentage
        [0.0, 100.0],           # New percentage
        [0.0, 100.0],           # Copied from 47
        [0.0, 100.0],           # Copied from 47
        [0.0, 100.0],           # Copied from 47
        [0.0, 100.0],           # New percentage
        [0.0, 100.0],           # New percentage
        [46.26, 65.35],         # Copied from 47
        [0.0, 5.41],            # Copied from 47
       [6.05, 13.24] ,          
        [39.67, 52.35],         # Copied from 47
        [1835.16, 35699.59],    # Copied from 47
        [0.045, 0.33],          # Copied from 47
        [7, 11],                # Copied from 47
        [0.0, 1.0],             # Copied from 47
        [0.0, 1.0],             # Copied from 47
        [0.0, 1.0],             # New percentage as proportion
        [1, 5]                  # Copied from 47
    ],
    'groups': [
        'G1',     # all_res_heated_vol_h_total (corr with clean_res_heated_vol_h_total)
        'G2',     # clean_res_total_buildings
        'G1',     # clean_res_heated_vol_h_total
        'G1',     # clean_res_premise_area_total (likely correlated with heated vol)
        
        'G3',     # Domestic_outbuilding_pct
        'G4',     # Standard_size_detached_pct
        'G5',     # Standard_size_semi_detached_pct
        'G6',     # Small_low_terraces_pct
        'G7',     # 2_storeys_terraces_pct
        'G8',     # Pre_1919_pct
        'G9',     # Unknown_age_pct
        'G10',    # age_1960_1979_pct
        'G11',    # age_1919_1944_pct
        'G12',    # Post_1999_pct
        'G13',    # HDD (corr with HDD_winter)
        'G14',    # CDD
        'G13',    # HDD_summer (likely correlated with other HDD)
        'G13',    # HDD_winter
        'G15',    # postcode_area
        'G16',    # postcode_density
        'G15',    # log_pc_area
        'G17',    # ethnic_group_perc_White
        'G18',    # central_heating_perc_Mains_gas
        'G19',    # household_siz_perc_1_person
        'G20'  
    ]
}

group_mapping_44 = {
    'G1': 'building_volume',          # Combines heated volumes and premise area
    'G2': 'total_buildings',          # Number of buildings
    'G3': 'outbuilding_pct',         # Domestic outbuilding percentage
    'G4': 'detached_pct',            # Standard size detached
    'G5': 'semi_detached_pct',       # Standard size semi detached
    'G6': 'small_terrace_pct',       # Small low terraces
    'G7': 'large_terrace_pct',       # 2 storeys terraces with rear extension
    'G8': 'pre_1919_pct',            # Pre 1919 buildings
    'G9': 'unknown_age_pct',         # Unknown age buildings
    'G10': 'age_1960_1979_pct',      # Buildings from 1960-1979
    'G11': 'age_1919_1944_pct',      # Buildings from 1919-1944
    'G12': 'post_1999_pct',          # Post 1999 buildings
    'G13': 'heating_degree_days',     # Combines HDD, HDD summer and winter
    'G14': 'cooling_degree_days',     # CDD
    'G15': 'postcode_area',        # Combines postcode area and log area
    'G16': 'postcode_density',        # Postcode density
    'G17': 'white_british_pct',       # White British percentage
    'G18': 'mains_gas_heating_pct',   # Mains gas central heating
    'G19': 'single_person_hh_pct',    # Single person households
    'G20': 'avg_household_size'       # Average household size
}




group_mapping_47 = {
   # Grouped variables (corr > 0.9)
   'G1': 'Building Floor Area (G)',
   'G9': 'HDD (G)',  # corr: 0.979
    'G11': 'Postcode Area (G)',
   
   # Individual variables
   'G2': 'Count of Buildings (Domestic)',
   'G3': 'Pct Domestic outbuilding ',
   'G4': 'Pct Standard size detached ',
   'G5': 'Pct Standard size semi detached',
   'G6': 'Pct Pre 1919',
   'G7': 'Pct Unknown age',
   'G8': 'Pct 1960-1979',
   'G10': 'CDD',
   'G12': 'Postcode density',
   'G14': 'Pct White',
   'G15': 'Pct Gas Central Heating',
   'G16': 'Average Household Size'
}


def check_and_enforce_heating_volume_constraint(x, problem_def):
    """
    Check and enforce the constraint that clean_res_heated_vol_h_total should equal
    all_res_heated_vol_h_total * (1 - Domestic_outbuilding_pct/100)
    
    Args:
        x: List of values corresponding to the variables in problem_def
        problem_def: Dictionary containing problem definition
        
    Returns:
        bool: Whether the constraint is satisfied
        float: The difference between actual and expected values
        float: The expected value of clean_res_heated_vol_h_total
    """
    # Get indices of relevant variables
    names = problem_def['names']
    all_res_idx = names.index('all_res_heated_vol_h_total')
    clean_res_idx = names.index('clean_res_heated_vol_h_total')
    outbuilding_idx = names.index('Domestic outbuilding_pct')
    
    # Calculate expected clean_res_heated_vol_h_total
    all_res_vol = x[all_res_idx]
    outbuilding_pct = x[outbuilding_idx]
    expected_clean_res = all_res_vol * (1 - outbuilding_pct/100)
    
    # Get actual value
    actual_clean_res = x[clean_res_idx]
    
    # Calculate difference
    difference = abs(actual_clean_res - expected_clean_res)
    
    # Check if constraint is satisfied (using small tolerance due to floating point arithmetic)
    is_satisfied = difference < 1e-10
    
    return is_satisfied, difference, expected_clean_res

def enforce_pc_area(x, problem_def):
    """
    Enforce the constraint by updating clean_res_heated_vol_h_total
  
    """
    # Create a copy of the input list
    x_new = x.copy()
    
    # Get indices of relevant variables
    names = problem_def['names']
    all_res_idx = names.index('postcode_area')
    clean_res_idx = names.index('log_pc_area')
    
    
    # Calculate and set the correct value
    all_res_vol = x[all_res_idx]
    
    x_new[clean_res_idx] = [np.log(x) for x in all_res_vol]
    print('new log pc',x_new[clean_res_idx] )
    return x_new

def enforce_heating_volume_constraint(x, problem_def):
    """
    Enforce the constraint by updating clean_res_heated_vol_h_total
    
    Args:
        x: List of values corresponding to the variables in problem_def
        problem_def: Dictionary containing problem definition
        
    Returns:
        List: Updated values with constraint enforced
    """
    # Create a copy of the input list
    x_new = x.copy()
    
    # Get indices of relevant variables
    names = problem_def['names']
    all_res_idx = names.index('all_res_heated_vol_h_total')
    clean_res_idx = names.index('clean_res_heated_vol_h_total')
    outbuilding_idx = names.index('Domestic outbuilding_pct')
    
    # Calculate and set the correct value
    all_res_vol = x[all_res_idx]
    outbuilding_pct = x[outbuilding_idx]
    x_new[clean_res_idx] = all_res_vol * (100 - outbuilding_pct/100)
    
    return x_new

def generate_problem(col_setting):
    name, cols = settings_dict[col_setting]
    
    new_problem = {
        'num_vars': len(cols),
        'names': cols,
        'bounds': [base_params[col] for col in cols]
    }
    
    return new_problem

# # Generate problems dynamically
# problems = {}
# for col_setting in settings_dict.keys():
#     problems[col_setting] = generate_problem(col_setting)

# # Special case for problem 44 with grouped version
# if 44 in problems:
#     problem_44_ungrouped = problems[44]
#     problem_44_grouped = {
#         'num_vars': problem_44_ungrouped['num_vars'],
#         'groups': ['group_1', 'group_1', 'group_1', 'group_2', 'group_3', 'group_4', 'group_5', 'group_6', 'group_7', 'group_8', 'group_9', 
#                    'group_10', 'group_11', 'group_12', 'group_13', 'group_12', 'group_12', 'group_14', 'group_15', 'group_14', 'group_15', 
#                    'group_16', 'group_17', 'group_18', 'group_1', 'group_1'],
#         'names': problem_44_ungrouped['names'],
#         'bounds': problem_44_ungrouped['bounds']
#     }
#     problems[44] = {
#         'ungrouped': problem_44_ungrouped,
#         'grouped': problem_44_grouped
#     }

# Function to get problem definition
def get_problem(col_setting, grouped=False):

    # problems = {}
    
    # problems[col_setting] = generate_problem(col_setting)

    # # Special case for problem 44 with grouped version
    # if 44 in problems:
    #     problem_44_ungrouped = problems[44]
    #     problem_44_grouped = {
    #         'num_vars': problem_44_ungrouped['num_vars'],
    #         'groups': ['group_1', 'group_1', 'group_1', 'group_2', 'group_3', 'group_4', 'group_5', 'group_6', 'group_7', 'group_8', 'group_9', 
    #                 'group_10', 'group_11', 'group_12', 'group_13', 'group_12', 'group_12', 'group_14', 'group_15', 'group_14', 'group_15', 
    #                 'group_16', 'group_17', 'group_18', 'group_1', 'group_1'],
    #         'names': problem_44_ungrouped['names'],
    #         'bounds': problem_44_ungrouped['bounds']
    #     }
    #     problems[44] = {
    #         'ungrouped': problem_44_ungrouped,
    #         'grouped': problem_44_grouped
    #     }

    if col_setting == 44 and grouped:
        return problem_44
    
    if col_setting ==47:
        return problem_47
    return problems[col_setting]
