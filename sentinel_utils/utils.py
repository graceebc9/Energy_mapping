import geopandas as gpd
import pandas as pd
import glob
from pyproj import CRS
import os
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import pandas as pd
import glob 
import re 
from datetime import datetime
from pathlib import Path
from shapely.geometry import box


# Function to get the geographic extent of a shapefile in different target CRS
def get_shapefile_extent(shp_path, target_crs_list):
    results = []
    gdf = gpd.read_file(shp_path)
    postcode = os.path.basename(shp_path).split('.')[0]
    for crs in target_crs_list:
        gdf_crs = gdf.to_crs(crs)
        extent = gdf_crs.total_bounds
        results.append((postcode, shp_path, crs.to_string(), extent))
    
    return results

def get_extent(tif_list, pcs):
    print('starting extent')
    unique_crs = []
    for file in tif_list:
        with rasterio.open(file) as src:
            unique_crs.append(src.crs)


    distinct_vals = list(set(unique_crs))
    print('target vars ' , distinct_vals)

    target_crs = distinct_vals
    # Initialize an empty DataFrame
    columns = ['postcode', 'postcode_shp_path', 'crs', 'bounds']
    final_df = pd.DataFrame(columns=columns)

    # Process each shapefile and collect results
    for i, shp_path in enumerate(pcs):
        extent_results = get_shapefile_extent(shp_path, target_crs)
        final_df = pd.concat([final_df, pd.DataFrame(extent_results, columns=columns)])
        
        # Save every 20 shapefiles
        if (i + 1) % 20 == 0:
            final_df.to_csv(f'shapefile_extents.csv', index=False)
            


def convert_string_to_float_list(string):
    # Strip the square brackets and then split by space
    cleaned_string = string.strip('[]')
    # Convert each split string into a float
    float_list = [float(num) for num in cleaned_string.split()]
    return float_list



def load_new_extent():
    df = pd.read_csv('/Users/gracecolverd/New_dataset/sentinel/shapefile_extents.csv')
    df['extent'] = df['bounds'].apply(convert_string_to_float_list)
    return df 


def extract_date_from_filename(filename):
    """
    Extract date and time from a filename.

    Parameters:
        filename (str): Filename.

    Returns:
        datetime: Date and time.
    """
    match = re.search(r'\d{8}T\d{6}', filename)
    if match:
        date_str = match.group(0)
        return datetime.strptime(date_str, '%Y%m%dT%H%M%S')
    else:
        return None


def get_raster_extent(tif_path):
    """
    Get the geographic extent of a raster.

    Parameters:
        tif_path (str): Path to the raster file.

    Returns:
        tuple: Tuple representing the extent.
    """
    with rasterio.open(tif_path) as src:
        bounds = src.bounds
    return bounds

def extents_overlap(extent1, extent2):
    """
    Check if two extents overlap.

    Parameters:
        extent1 (tuple): Extent coordinates (xmin, ymin, xmax, ymax).
        extent2 (tuple): Extent coordinates (xmin, ymin, xmax, ymax).

    Returns:
        bool: True if the extents overlap, False otherwise.
    """
    return not (extent1[0] >= extent2[2] or extent1[2] <= extent2[0] or
                extent1[1] >= extent2[3] or extent1[3] <= extent2[1])

def convert_string_to_float_list(string):
    """
    Convert a string of space-separated numbers to a list of floats.

    Parameters:
        string (str): String containing space-separated numbers.

    Returns:
        list: List of floats.
    """
    cleaned_string = string.strip('[]')
    float_list = [float(num) for num in cleaned_string.split()]
    return float_list


def get_tif_files(directory):
    """
    Get a list of TIFF files in a directory.

    Parameters:
        directory (str): Directory path.

    Returns:
        list: List of TIFF file paths.
    """
    path = Path(directory)
    tif_files = [p for p in path.rglob('/*/*.tif') if not p.name.startswith('._')]
    return tif_files 


def process_shapefile(tif_path, shp_path, tif_crs, results, date_time):
    gdf = gpd.read_file(shp_path)
    gdf = gdf.to_crs(tif_crs)
    
    with rasterio.open(tif_path) as src:
        bounds = src.bounds
        left, bottom, right, top = bounds
        tif_geom = box(left, bottom, right, top)
        tif_gdf = gpd.GeoDataFrame({"geometry": [tif_geom]}, crs=tif_crs)

        # Clip the shapefile to the bounds of the TIFF file
        clipped_gdf = gpd.clip(gdf, tif_gdf)
        
        if clipped_gdf.empty:
            print(f"No overlap between {tif_path} and {shp_path}")
            return

        for _, geom_row in clipped_gdf.iterrows():
            geom = [geom_row['geometry']]
            postcode = geom_row['POSTCODE']
            
            try:
                out_image, out_transform = mask(src, geom, crop=True)
                masked_data = np.where(out_image >= -1, out_image, np.nan)
                if masked_data.size == 0 or np.all(np.isnan(masked_data)) or np.all(masked_data == 0):
                    mean_value = np.nan
                else:
                    mean_value = np.nanmean(masked_data)
                results.append({
                    'postcode': postcode,
                    'mean_value': mean_value,
                    'date_time': date_time,
                    'tif_path': tif_path,
                    'shp_path': shp_path
                })
            except Exception as e:
                print(f'Error processing geometry: {e}')
                continue
