import os
import pandas as pd
import geopandas as gpd
import numpy as np
from libpysal.weights import KNN
from spreg import ML_Lag
from splot.esda import plot_moran
import esda
import matplotlib.pyplot as plt
import pickle

def load_and_prepare_data(input_m3, pclatlong_path):
    # Load the data
    data = pd.read_csv(input_m3)

    # Define columns
    cols = [
        'all_types_total_buildings', 
        'all_res_heated_vol_h_total',
        'HDD_winter',
        'max_vol_per_uprn',
        'all_types_uprn_count_total',
        'postcode_area',
        'postcode_density'
    ]
    target = ['total_gas']

    # Load the latitude and longitude data
    results_df = pd.read_csv(pclatlong_path)

    # Create a GeoDataFrame from the results
    gdf = gpd.GeoDataFrame(results_df, geometry=gpd.points_from_xy(results_df.longitude, results_df.latitude))

    # Merge with additional data and select relevant columns
    gdf = gdf.merge(data, on='postcode')[cols + target + ['geometry', 'postcode', 'latitude', 'longitude']].copy()
    gdf.dropna(inplace=True)

    return gdf, cols, target

def calculate_spatial_weights(gdf):
    # Calculate spatial weights matrix using K-Nearest Neighbors
    w = KNN.from_dataframe(gdf, k=5)
    w.transform = 'R'
    return w

def fit_spatial_lag_model(gdf, w, cols, target):
    # Extract the dependent variable and independent variables
    y = gdf[target].values
    X = gdf[cols].values

    # Fit a Spatial Lag Model
    model = ML_Lag(y, X, w, name_y=target[0], name_x=cols)
    return model

def save_model_and_results(model, output_path):
    # Save the model
    model_file = os.path.join(output_path, 'spatial_lag_model.pkl')
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)
    
    # Save the model summary to a text file
    summary_file = os.path.join(output_path, 'model_summary.txt')
    with open(summary_file, 'w') as f:
        f.write(str(model.summary))

def main():
    input_m3 = os.environ.get('MLPATH')
    output_path = os.environ.get('OUTPUTPATH')
    pclatlong_path = os.environ.get('PCLATLONGPATH')

    gdf, cols, target = load_and_prepare_data(input_m3, pclatlong_path)
    w = calculate_spatial_weights(gdf)
    model = fit_spatial_lag_model(gdf, w, cols, target)
    
    # Print the model summary
    print(model.summary)

    # Define the output path
    
    os.makedirs(output_path, exist_ok=True)
    
    # Save the model and results
    save_model_and_results(model, output_path)

if __name__ == "__main__":
    main()
