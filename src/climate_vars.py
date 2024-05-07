import os 
import pandas as pd 
import rioxarray as rxr 
import xarray as xr
import netCDF4 as nc
import geopandas as gpd 
import glob

def load_nc_file(path):
    # Convert to xarray Dataset
    nc_dataset = nc.Dataset(path)
    xds = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_dataset))
    xds.rio.set_spatial_dims(x_dim='projection_x_coordinate', y_dim='projection_y_coordinate', inplace=True)
    xds = xds.interpolate_na(dim='projection_x_coordinate')
    return xds 

base_temp_heating = 15.5  # Base temperature for heating
base_temp_cooling = 18.0  # Base temperature for cooling


def calculate_hdd_cdd(row):
    temp = row['tas']
    hdd = max(base_temp_heating - temp, 0)
    cdd = max(temp - base_temp_cooling, 0)
    if hdd is None or cdd is None:
        raise ValueError("Invalid temperature value")
    return pd.Series([hdd, cdd])


def sample(pc, xds):
    if pc.empty:
        raise ValueError("GeoDataFrame is empty")
    centroids = pc.geometry.centroid 
    # Assuming 'xds' is your xarray Dataset and 'centroids' are calculated
    # Convert centroids to suitable format if not already in xarray format
    x_coords = xr.DataArray(centroids.x, dims="points")
    y_coords = xr.DataArray(centroids.y, dims="points")

    # Sample the dataset using nearest neighbor interpolation
    sampled_values = xds.sel(
        projection_x_coordinate=x_coords,
        projection_y_coordinate=y_coords,
        method="nearest"
    )
    return sampled_values 

import pandas as pd
import xarray as xr

def calc_HDD_CDD_pc(pc, xds, tolerance=0.001):
    """
    Calculate Heating Degree Days (HDD) and Cooling Degree Days (CDD) for each point in a GeoDataFrame
    using the nearest temperature data from an xarray Dataset. Checks if the sum of seasonal data is within
    a specified tolerance of the annual totals.

    Parameters:
    - pc: GeoDataFrame with points and their geometries.
    - xds: xarray Dataset containing temperature data.
    - tolerance: float, maximum allowed difference between the sum of seasonal values and the annual total.

    Returns:
    - result: DataFrame with annual, summer, and winter HDD and CDD.
    - sampled_df: DataFrame of sampled values for debugging or further analysis.
    """

    # Check CRS consistency
    xds.rio.write_crs(pc.crs, inplace=True) 
    if pc.crs != xds.rio.crs:
        raise ValueError("CRS mismatch between GeoDataFrame and xarray Dataset")
    
    sampled_values = sample(pc, xds)  # Assuming 'sample' is a predefined function

    # Convert sampled DataArray to DataFrame
    sampled_df = sampled_values.to_dataframe().reset_index() 
    sampled_df = sampled_df[sampled_df['bnds'] == 1].reset_index(drop=True) 

    # Apply the function to calculate HDD and CDD
    sampled_df[['HDD', 'CDD']] = sampled_df.apply(calculate_hdd_cdd, axis=1)

    # Summarize data by points
    annual = sampled_df.groupby('points')[['HDD', 'CDD']].sum()

    # Define month indices for summer (April to September) and winter (October to March)
    summer_months = [4, 5, 6, 7, 8, 9]
    winter_months = [10, 11, 12, 1, 2, 3]

    # Filter data based on month for seasonal calculations
    sampled_df['month'] = sampled_df['time'].dt.month  # assuming 'time' is the time coordinate
    summer_data = sampled_df[sampled_df['month'].isin(summer_months)]
    winter_data = sampled_df[sampled_df['month'].isin(winter_months)]

    # Sum HDD and CDD for summer and winter
    summer = summer_data.groupby('points')[['HDD', 'CDD']].sum()
    winter = winter_data.groupby('points')[['HDD', 'CDD']].sum()

    # Merge results
    result = annual.join([summer.rename(columns=lambda x: x + '_summer'),
                          winter.rename(columns=lambda x: x + '_winter')])

    # Check if the sum of seasonal data is within the specified tolerance
    for season in ['HDD', 'CDD']:
        total_check = abs(result[f'{season}_summer'] + result[f'{season}_winter'] - result[season])
        if any(total_check > tolerance):
            raise ValueError(f"Seasonal totals for {season} exceed the tolerance threshold.")   
    result = result.join(pc.reset_index(), on='points')
    result.drop(columns=['UPP', 'PC_AREA', 'geometry'], inplace=True)
    return result


    # group = sampled_df.groupby('points')[['HDD', 'CDD']].sum().join(pc)
    # return  group  


def save_pc_file(res, output_path):
    res.to_csv(output_path, index=False)
    


def run_all_pc_shps(output_path, pc_base_path,  temp_1km_res_file_year):
    # create folder if not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    pc_shps1 = glob.glob(os.path.join(pc_base_path , 'one_letter_pc_code/*/*.shp') ) 
    pc_shps2 = glob.glob(os.path.join(pc_base_path , 'two_letter_pc_code/*.shp') )
    if not pc_shps1 and not pc_shps2:
        raise ValueError("No postcode shapefiles found.")

    xds = load_nc_file(temp_1km_res_file_year )   
    for pc in pc_shps1 + pc_shps2:
        
        pc_name = os.path.basename(pc).split('.')[0]
        output_file = os.path.join(output_path, f'{pc_name}.csv')
        # check if output already exists
        if os.path.exists(output_file):
            print(f"Output file {output_file} already exists. Skipping...")
            continue
        print(f"Processing {pc_name}...")
        pc_df = gpd.read_file(pc)
        res = calc_HDD_CDD_pc(pc_df, xds)
        save_pc_file(res, output_file)



