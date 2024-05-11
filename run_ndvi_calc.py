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

def load_extents(example_tif, pcs):
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'src', 'sentinel' , 'shapefile_extents_ndvicrs.csv')
    
    if os.path.exists(csv_path):
        extents_df = pd.read_csv(csv_path)
    else:
        target_crs  = rasterio.open(example_tif).crs
        print('Generating extent')
        shapefile_extents = []
        # Process each shapefile
        for shp in pcs: 
            shp_path = os.path.join(pc_shp_folder, shp)
            if shp_path.endswith('.shp'):
                extent = get_shapefile_extent(shp_path, target_crs)
                shapefile_extents.append({'shapefile': shp, 'extent': extent, 'crs': target_crs})

        # Convert list to DataFrame
        extents_df = pd.DataFrame(shapefile_extents)
        
        extents_df.to_csv(csv_path, index=False)
        print("Shapefile extents saved to CSV.")
    return extents_df 


# Function to get the geographic extent of a shapefile in its original CRS
def get_shapefile_extent(shp_path, target_crs):
    gdf = gpd.read_file(shp_path)
    # original_crs = gdf.crs
    gdf = gdf.to_crs(target_crs)
    
    return gdf.total_bounds

def extract_date_from_filename(filename):
    # Regular expression to match the date and time part of the filename
    match = re.search(r'\d{8}T\d{6}', filename)
    if match:
        date_str = match.group(0)
        # Convert the string to a datetime object
        date_time = datetime.strptime(date_str, '%Y%m%dT%H%M%S')
        return date_time
    else:
        return None

# Function to get the geographic extent of a raster
def get_raster_extent(tif_path):
    with rasterio.open(tif_path) as src:
        bounds = src.bounds
    return bounds

# Function to check if two extents overlap
def extents_overlap(extent1, extent2):
    return not (extent1[0] > extent2[2] or extent1[2] < extent2[0] or
                extent1[1] > extent2[3] or extent1[3] < extent2[1])

def convert_string_to_float_list(string):
    # Strip the square brackets and then split by space
    cleaned_string = string.strip('[]')
    # Convert each split string into a float
    float_list = [float(num) for num in cleaned_string.split()]
    return float_list


def get_tif_files(directory):
    # Create a Path object
    path = Path(directory)

    # Use rglob to find all .tif files
    tif_files = [p for p in path.rglob('*.tif') if not p.name.startswith('._')]

    return tif_files 

def run_ndvi(outpath, extent_df, tif_list):
    extent_df['extent2'] = extent_df['extent'].apply(convert_string_to_float_list)
    # Store results
    results = []
    # Process each tif file
    for tif_path in tif_list:
        if tif_path.endswith('.tif'):
            filename = os.path.basename(tif_path)
            
            outname = os.path.join(outpath, filename.split('__ndvi')[0] + '_pcresults.csv' ) 
            # check if file already exists 
            if os.path.exists(outname):
                print('results already exists')
                continue
            

            date_time = extract_date_from_filename(filename)
            tif_extent = get_raster_extent(tif_path)
            tif_crs = rasterio.open(tif_path).crs.to_string()

            # Process each pre-loaded shapefile extent
            for idx, row in extent_df.iterrows():
            
                shp_path =  row['shapefile'] 
                shp_extent = row['extent2']
                if extents_overlap(tif_extent, shp_extent):
                    gdf = gpd.read_file(shp_path)
                    gdf = gdf.to_crs(tif_crs)  # Convert to the TIF's CRS

                    # Process each geometry in the shapefile
                    for _, geom_row in gdf.iterrows():
                        geom = [geom_row['geometry']]
                        postcode = geom_row['POSTCODE']
                        
                        # Clip and process raster
                        with rasterio.open(tif_path) as src:
                            try:
                                out_image, out_transform = mask(src, geom, crop=True)
                                masked_data = np.where(out_image >= -1, out_image, np.nan)
                                mean_value = np.nanmean(masked_data)

                                # Store the result
                                results.append({'postcode': postcode, 'mean_value': mean_value, 'date_time': date_time, 'tif_path': tif_path, 'shp_path': shp_path  })
                                # print(f"Processed {postcode} for {tif}.")
                            # except if WindowError 
                            except:
                                # print(f"Error processing {postcode} for {tif}.")
                                continue

            # Save results to a CSV file
            results_df = pd.DataFrame(results)
            results_df['month'] = pd.to_datetime(results_df['date_time']).dt.month
            results_df['day'] = pd.to_datetime(results_df['date_time']).dt.day
            results_df.to_csv(outname, index=False)
            print("Results saved successfully.")

def main(pcs, outpath, tif_folder):
    """
    pcs: list of path to shps for polygons split by postcode
    outpath: where results table saved 
    tif_folder: folder where tifs of NDVI for sentinel live
    """
    tif_list =get_tif_files(tif_folder)


    extent_df = load_extents(tif_list[0], pcs)
     
    run_ndvi(outpath, extent_df, tif_list)


if __name__ == "__main__":

    pc_shp_folder = os.environ.get('PC_SHP')
    tif_folder = os.environ.get('TIF_PATH')
    outpath = os.environ.get('OUTPUT_PATH')

    pcs = glob.glob(os.path.join(pc_shp_folder, 'two_letter_pc_code/*.shp') )+ glob.glob(os.path.join(pc_shp_folder + 'one_letter_pc_code/*/*.shp'))

    
    main(pcs, outpath, tif_folder)


# export TIF_PATH='/Volumes/T9/Data_downloads/NDVI/2022_04'
# export OUTPUT_PATH='/Users/gracecolverd/New_dataset/test'
# export PC_SHP='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'


