# problem_definitions.py

problems = {
    45: {
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
    },
    44: {
        'ungrouped': {
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
                [0, 7600],  # all_res_heated_vol_h_total
                [0, 50],    # clean_res_total_buildings
                [0, 7400],  # clean_res_heated_vol_h_total
                [0, 52],    # Domestic outbuilding_pct
                [0, 100],   # Standard size detached_pct
                [0, 100],   # Standard size semi detached_pct
                [0, 100],   # Small low terraces_pct
                [0, 100],   # 2 storeys terraces with t rear extension_pct
                [0, 100],   # Pre 1919_pct
                [0, 20],    # Unknown_age_pct
                [0, 100],   # 1960-1979_pct
                [0, 100],   # 1919-1944_pct
                [0, 100],   # Post 1999_pct
                [30, 80],   # HDD
                [0, 8],     # CDD
                [3, 15],    # HDD_summer
                [30, 60],   # HDD_winter
                [1, 26000], # postcode_area
                [0, 0.5],   # postcode_density
                [5, 12],    # log_pc_area
                [0, 1],     # ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British
                [0, 1],     # central_heating_perc_Mains gas only
                [0, 1],     # household_siz_perc_perc_1 person in household
                [1, 5],     # Average Household Size
                [0, 2000],  # clean_res_premise_area_total
                [0, 1000]   # all_res_base_floor_total
            ]
        },
        'grouped': {
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
                [0, 7600],  # all_res_heated_vol_h_total
                [0, 50],    # clean_res_total_buildings
                [0, 7400],  # clean_res_heated_vol_h_total
                [0, 52],    # Domestic outbuilding_pct
                [0, 100],   # Standard size detached_pct
                [0, 100],   # Standard size semi detached_pct
                [0, 100],   # Small low terraces_pct
                [0, 100],   # 2 storeys terraces with t rear extension_pct
                [0, 100],   # Pre 1919_pct
                [0, 20],    # Unknown_age_pct
                [0, 100],   # 1960-1979_pct
                [0, 100],   # 1919-1944_pct
                [0, 100],   # Post 1999_pct
                [30, 80],   # HDD
                [0, 8],     # CDD
                [3, 15],    # HDD_summer
                [30, 60],   # HDD_winter
                [1, 26000], # postcode_area
                [0, 0.5],   # postcode_density
                [5, 12],    # log_pc_area
                [0, 1],     # ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British
                [0, 1],     # central_heating_perc_Mains gas only
                [0, 1],     # household_siz_perc_perc_1 person in household
                [1, 5],     # Average Household Size
                [0, 2000],  # clean_res_premise_area_total
                [0, 1000]   # all_res_base_floor_total
            ]
        }
    }
}


