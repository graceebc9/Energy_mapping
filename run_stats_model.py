import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from libpysal.weights import KNN, DistanceBand
import libpysal
from spreg import OLS
import pickle
import json 
import geopandas as gpd



def load_shapefile_with_mapping(shapefile_path, mapping_path):
    # Load the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Load the column name mapping from the JSON file
    with open(mapping_path, 'r') as file:
        mapping = json.load(file)
    
    # Invert the mapping dictionary to map from numeric identifiers back to original names
    inverted_mapping = {v: k for k, v in mapping.items()}
    
    # Rename the columns using the inverted mapping
    gdf.rename(columns=inverted_mapping, inplace=True)
    
    return gdf

def save_weights(w, filename):
    with open(filename, 'wb') as f:
        pickle.dump(w, f)

def load_weights( filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_weights(df, dist_thres, knn, full_filename):
    print('Calculating weights...')
    
    if not os.path.exists(full_filename):
        w_distance = DistanceBand.from_dataframe(df, threshold=dist_thres, binary=True)
        w_distance.transform = 'r'
        w_knn = KNN.from_dataframe(df, k=knn)
        w_combined = libpysal.weights.w_union(w_distance, w_knn)
        w_combined.transform = 'r'
        w_combined.remap_ids(df.index.tolist())
        save_weights(w_combined, full_filename)
    else:
        w_combined = load_weights( full_filename)
    return w_combined



def export_model_results(results, filename):
    with open(filename, 'w') as f:
        f.write(results.summary)
    

def create_model_directory(knn, path, thresh_dist, dataset_name):
    directory = f'{dataset_name}_knn{knn}_dist{thresh_dist}'
    path = os.path.join(path, directory)
    if not os.path.exists(path):
        os.makedirs(path)
    return path



def pre_x_proc(df):
    print('Processing data...')
    X = df.copy()
    X.localfill_modal_age = X.localfill_modal_age.fillna('Unknown Age')
    X = pd.get_dummies(X)
    X['localfill_modal_age_1919-1999'] = X[['localfill_modal_age_1919-1944', 'localfill_modal_age_1945-1959', 'localfill_modal_age_1960-1979', 'localfill_modal_age_1980-1989', 'localfill_modal_age_1990-1999']].sum(axis=1)
    X['standard_detached_and_semi_detached'] = X['Standard size detached_pct'] + X['Standard size semi detached_pct']
    X_filt = X[['clean_res_heated_vol_h_total', 'av_vol_per_uprn', 'outb_res_premise_area_total', '2 storeys terraces with t rear extension_pct', '3-4 storey and smaller flats_pct', 'standard_detached_and_semi_detached', 'Large detached_pct', 'Large semi detached_pct', 'Linked and step linked premises_pct', 'Medium height flats 5-6 storeys_pct', 'None_type_pct', 'Planned balanced mixed estates_pct', 'Semi type house in multiples_pct', 'Small low terraces_pct', 'Tall flats 6-15 storeys_pct', 'Tall terraces 3-4 storeys_pct', 'Very large detached_pct', 'Very tall point block flats_pct', 'density', 'localfill_modal_age_Post 1999', 'localfill_modal_age_Pre 1919', 'localfill_modal_age_1919-1999']]
    return X_filt

def gen_x_y(df):
    y = df['av_gas_per_vol'].values
    y_transformed = np.log(y + 1)
    X_filt = pre_x_proc(df)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_filt)
    return X_scaled, y_transformed, X_filt.columns

def main():
    knn = 1 
    dist_thres = 1000 
    
    path = os.environ.get('OUTPUT_DIR')  # Default path
    shapefile_path = os.environ.get('INPUT_DATA')  # Default path
    mapping_path= os.environ.get('INPUT_COLMAP')  # Default path
    
    dataset_name =shapefile_path.split('/')[-1].split('.')[0]
    
    model_directory = create_model_directory(knn, path, dist_thres, dataset_name)
    weights_file = os.path.join(model_directory, 'weights.pkl')
    results_file = os.path.join(model_directory, 'model_results.txt')
    
    df = load_shapefile_with_mapping(shapefile_path, mapping_path)
    
    w = get_weights(df, dist_thres, knn, weights_file)
    X_scaled, y_transformed , X_cols= gen_x_y(df)

    # Fit the OLS model
    ols = OLS(y_transformed, X_scaled, name_y='log_av_gas_per_vol', name_x=X_cols.tolist(), w=w, spat_diag=True, moran=True)
    export_model_results(ols, results_file)

if __name__ == '__main__':
    main()


# export OUTPUT_DIR='/Users/gracecolverd/New_dataset/stats_models/model_res'
# export INPUT_DATA='/Users/gracecolverd/New_dataset/postcode_attrs/statsmodels_data_v1.shp'
# export INPUT_COLMAP='/Users/gracecolverd/New_dataset/postcode_attrs/statsmodels_data_v1.json'
  