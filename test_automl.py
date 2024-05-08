import sys
import os
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor


import os
import sys

# from src.automl import transform, save_results 

def save_results(results, output_path):
    res_string = str(results)
    # summary = predictor.fit_summary()
    with open(os.path.join(output_path, 'model_summary.txt'), 'w') as f:
        f.write(res_string)


def transform(df, label):
    cols_remove = [
        'ï»¿pcd7', 'pcd8', 'pcds', 'dointr', 'doterm', 'usertype', 'oa21cd',
        'lsoa21cd', 'msoa21cd', 'ladcd', 'lsoa21nm', 'msoa21nm', 'ladnm',
        'ladnmw', 'pcd7', 'diff_min_max_gas_per_vol', 'diff_gas_meters_uprns_res',
        'min_gas_per_vol', 'max_gas_per_vol', 'total_gas', 'avg_gas', 'median_gas',
        'num_meters_gas', 'total_elec', 'avg_elec', 'median_elec', 'num_meters_elec',
        'comm_alltypes_count', 'unknown_alltypes', 'outb_res_uprn_count_total', 'mixed_total_buildings', 'mixed_premise_area_total', 'mixed_gross_area_total', 'mixed_heated_vol_fc_total', 'mixed_heated_vol_h_total', 'mixed_base_floor_total', 'mixed_basement_heated_vol_max_total', 'mixed_listed_bool_total', 'mixed_uprn_count_total', 'percent_residential', 'perc_all_res', 'Unknown_pct', 'ethnic_group_perc_Does not apply', 'household_siz_perc_perc_0 people in household', 'occupancy_rating_perc_Does not apply', 'household_comp_by_bedroom_perc_Does not apply_Does not apply', 'household_comp_by_bedroom_perc_Does not apply_1 bedroom', 'household_comp_by_bedroom_perc_Does not apply_2 bedrooms', 'household_comp_by_bedroom_perc_Does not apply_3 bedrooms', 'household_comp_by_bedroom_perc_Does not apply_4 or more bedrooms', 'household_comp_by_bedroom_perc_One-person household_Does not apply', 'household_comp_by_bedroom_perc_Single family household: All aged 66 years and over_Does not apply', 'household_comp_by_bedroom_perc_Single family household: Couple family household_Does not apply', 'household_comp_by_bedroom_perc_Single family household: Lone parent household_Does not apply', 'household_comp_by_bedroom_perc_Other household types_Does not apply', 'central_heating_perc_Does not apply'
    ]
    working_cols = [col for col in df.columns if col not in cols_remove]
    df = df[working_cols]
    df = df[~df[label].isna()]
    return df

def main():
    label = 'av_gas_per_vol'
    data_path = os.environ.get('DATA_PATH')
    train_subset_prop = float(os.environ.get('TRAIN_SUBSET_PROP') )
    predictor_input= "/home/gb669/rds/hpc-work/energy_map/data/automl_models/results/ml_data_engwales_census_v2_avgas_12000_None_allcols_tsp_0.2_all"
    


    df = pd.read_csv(data_path)
    _, test_data = train_test_split(df, test_size=0.2, random_state=42)
    test_data = test_data.sample(n=20000, random_state=42) 
    test_data = transform(TabularDataset(test_data), label)

    predictor = TabularPredictor.load("/home/gb669/rds/hpc-work/energy_map/data/automl_models/results/ml_data_engwales_census_v2_avgas_12000_None_allcols_tsp_0.2_all")
    y_pred = predictor.predict(test_data.drop(columns=[label]))
    results = predictor.evaluate_predictions(y_true=test_data[label], y_pred=y_pred, auxiliary_metrics=True)


    
    print(results)

    save_results(results, predictor_input)
    res = predictor.leaderboard(test_data)
    res.to_csv(os.path.join(predictor_input, 'leaderboard_results.csv'))

    pred = predictor.feature_importance(test_data)
    pred.to_csv(os.path.join(predictor_input, 'feature_importance.csv'))


if __name__ == '__main__':
    main()


