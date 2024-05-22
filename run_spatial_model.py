import os
import pandas as pd
import geopandas as gpd
import numpy as np
from libpysal.weights import KNN
from spreg import ML_Error
from splot.esda import plot_moran
import esda
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split

def load_and_prepare_data(input_m3, pclatlong_path, test_size):
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
    gdf = gdf.merge(data, on='postcode')

    target_len = len(gdf) * (1 - float(test_size))

    working_data = gdf[cols + target + ['ladcd', 'geometry', 'postcode', 'latitude', 'longitude']].copy() 
    working_data.dropna(inplace=True)   

    props = pd.DataFrame(working_data['ladcd'].value_counts(normalize=True)).reset_index()
    props.columns = ['ladcd', 'proportion']
    # Randomly sample 80% of the ladcds from props
    train_ladcd = props.sample(frac=1 - float(test_size) , random_state=42)['ladcd'].values

    # Check if the train size is within 5% of the target length
    if abs(100 - len(working_data[working_data['ladcd'].isin(train_ladcd)]) / target_len * 100) < 5:
        print('Train size within 5% of the target length')
    else:
        raise ValueError('Train size not within 5% of the target length')


    # Split the data into training and testing sets based on ladcd
    gdf_train = working_data[working_data['ladcd'].isin(train_ladcd)]
    gdf_test = working_data[~working_data['ladcd'].isin(train_ladcd)]


    # Calculate spatial weights matrix using K-Nearest Neighbors for the training set
    w_train = KNN.from_dataframe(gdf_train, k=5)
    w_train.transform = 'R'

    # Extract the dependent variable and independent variables for training
    y_train = gdf_train['total_gas'].values
    X_train = gdf_train[cols].values

    return X_train, y_train, gdf_train, gdf_test,   w_train, target, cols

def fit_spatial_lag_model(y_train, X_train , w_train , target, cols ):

    # Fit a Spatial Lag Model
    model = ML_Error(y_train, X_train, w_train, name_y=target[0], name_x=cols)
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
    test_size = os.environ.get('TESTSIZE')

    X_train, y_train, gdf_train, gdf_test , w_train, target, cols = load_and_prepare_data(input_m3, pclatlong_path, test_size)
    
    model = fit_spatial_lag_model(y_train, X_train , w_train , target, cols )
    
    # Print the model summary
    print(model.summary)

    # Define the output path
    
    os.makedirs(output_path, exist_ok=True)
    
    # Save the model and results
    save_model_and_results(model, output_path)

if __name__ == "__main__":
    main()


# export MLPATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_input/V3.2_region_geoms.csv'
# export OUTPUTPATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_output'   
# export PCLATLONGPATH='/Volumes/T9/Data_downloads/new-data-outputs/ml_input/postcode_lat_lon.csv' 
# export TESTSIZE=0.2



