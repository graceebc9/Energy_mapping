# problem_definitions.py
from .model_col_final import settings_dict

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

# Define problem bounds for SALib
problem_47 = {
    'num_vars': 18,
    'names': [
        'all_res_heated_vol_h_total',
        'clean_res_total_buildings',
        'clean_res_heated_vol_h_total',
        'Domestic_outbuilding_pct',
        'Standard_size_detached_pct',
        'Standard_size_semi_detached_pct',
        'Pre_1919_pct',
        'Unknown_age_pct',
        'age_1960_1979_pct',
        'HDD',
        'CDD',
        'HDD_winter',
        'postcode_area',
        'postcode_density',
        'log_pc_area',
        'ethnic_group_perc_White',
        'central_heating_perc_Mains_gas',
        'Average_Household_Size'
    ],
    'bounds': [
        [738.73, 6824.35],      # all_res_heated_vol_h_total
        [2.0, 43.0],            # clean_res_total_buildings
        [720.18, 6634.51],      # clean_res_heated_vol_h_total
        [0.0, 100.0],           # Domestic_outbuilding_pct
        [0.0, 100.0],           # Standard_size_detached_pct
        [0.0, 100.0],           # Standard_size_semi_detached_pct
        [0.0, 100.0],           # Pre_1919_pct
        [0.0, 100.0],           # Unknown_age_pct
        [0.0, 100.0],           # age_1960_1979_pct
        [46.26, 65.35],         # HDD
        [0.0, 5.41],            # CDD
        [39.67, 52.35],         # HDD_winter
        [1835.16, 35699.59],    # postcode_area
        [0.045, 0.33],          # postcode_density
        [7.51, 10.48],          # log_pc_area
        [0.0, 1.0],             # ethnic_group_perc_White
        [0.0, 1.0],             # central_heating_perc_Mains_gas
        [1.84, 3.03]            # Average_Household_Size
    ]
}



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

    problems = {}
    
    problems[col_setting] = generate_problem(col_setting)

    # Special case for problem 44 with grouped version
    if 44 in problems:
        problem_44_ungrouped = problems[44]
        problem_44_grouped = {
            'num_vars': problem_44_ungrouped['num_vars'],
            'groups': ['group_1', 'group_1', 'group_1', 'group_2', 'group_3', 'group_4', 'group_5', 'group_6', 'group_7', 'group_8', 'group_9', 
                    'group_10', 'group_11', 'group_12', 'group_13', 'group_12', 'group_12', 'group_14', 'group_15', 'group_14', 'group_15', 
                    'group_16', 'group_17', 'group_18', 'group_1', 'group_1'],
            'names': problem_44_ungrouped['names'],
            'bounds': problem_44_ungrouped['bounds']
        }
        problems[44] = {
            'ungrouped': problem_44_ungrouped,
            'grouped': problem_44_grouped
        }

    if col_setting == 44 and grouped:
        return problems[44]['grouped']
    return problems[col_setting]

