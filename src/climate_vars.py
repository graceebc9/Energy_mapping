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

def calc_HDD_CDD_pc(pc, xds):
    """
    """

    # check crs same
    xds.rio.write_crs(pc.crs, inplace=True) 
    if pc.crs != xds.rio.crs:
        raise ValueError("CRS mismatch between GeoDataFrame and xarray Dataset")
    
    sampled_values =sample(pc, xds)

    # Convert sampled DataArray to DataFrame
    sampled_df = sampled_values.to_dataframe().reset_index() 
    sampled_df = sampled_df[sampled_df['bnds']==1].reset_index() 

    # Apply the function to each row
    sampled_df[['HDD', 'CDD']] = sampled_df.apply(calculate_hdd_cdd, axis=1)


    group = sampled_df.groupby('points')[['HDD', 'CDD']].sum().join(pc)
    return  group  


def save_pc_file(res, output_path):
    res.to_csv(output_path, index=False)
    


def run_all_pc_shps(output_path, pc_base_path,  temp_1km_res_file_year):
    pc_shps1 = glob.glob(os.path.join(pc_base_path , 'one_letter_pc_code/*/*.shp') ) 
    pc_shps2 = glob.glob(os.path.join(pc_base_path , 'two_letter_pc_code/*.shp') )
    if not pc_shps1 and not pc_shps2:
        raise ValueError("No postcode shapefiles found.")

    xds = load_nc_file(temp_1km_res_file_year )   
    for pc in pc_shps1 + pc_shps2:
        pc_name = os.path.basename(pc).split('.')[0]
        output_file = os.path.join(output_path, f'{pc_name}.csv')
        print(f"Processing {pc_name}...")
        pc_df = gpd.read_file(pc)
        res = calc_HDD_CDD_pc(pc_df, xds)
        save_pc_file(res, output_file)



