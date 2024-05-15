import geopandas as gpd
import pandas as pd
import glob
import os
import rasterio
from rasterio.mask import mask
import numpy as np
import re
from datetime import datetime
from pathlib import Path
from pyproj import CRS
from concurrent.futures import ProcessPoolExecutor, as_completed
from sentinel_utils.utils import extract_date_from_filename, get_raster_extent, extents_overlap, load_new_extent, process_shapefile

def process_tif_file(tif_path, extent_df, outpath):
    print('Starting ', tif_path)
    results = []
    filename = os.path.basename(tif_path)
    outname = os.path.join(outpath, filename.split('__ndvi')[0] + '_pcresults.csv')
    
    if os.path.exists(outname):
        print(f'Results already exist for {filename}')
        return

    date_time = extract_date_from_filename(filename)
    tif_extent = get_raster_extent(tif_path)
    tif_crs = rasterio.open(tif_path).crs.to_string()
    filt_crs = rasterio.open(tif_path).crs

    extent_live = extent_df[extent_df['crs'] == filt_crs].copy()
    extent_live.reset_index(inplace=True)
    
    for idx, row in extent_live.iterrows():
        shp_path = row['postcode_shp_path']
        shp_extent = row['extent']
        if extents_overlap(tif_extent, shp_extent):
            process_shapefile(tif_path, shp_path, tif_crs, results, date_time)
    
    save_results(results, outname)


def save_results(results, outname):
    results_df = pd.DataFrame(results)
    results_df.to_csv(outname, index=False)
    print(f'Results saved successfully to {outname}')

def run_ndvi(outpath, extent_df, tif_list):
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_tif_file, tif_path, extent_df, outpath) for tif_path in tif_list]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Error processing file: {e}')

def get_shapefile_paths(pc_shp_folder):
    return glob.glob(os.path.join(pc_shp_folder, 'two_letter_pc_code/*.shp')) + glob.glob(os.path.join(pc_shp_folder, 'one_letter_pc_code/*/*.shp'))

def main():
    label = os.environ.get('LABEL')
    pc_shp_folder = os.environ.get('PC_SHP')
    tif_folder = os.environ.get('TIF_PATH')
    outpath = os.environ.get('OUTPUT_PATH')
    outpath = os.path.join(outpath, label)
    os.makedirs(outpath, exist_ok=True)

    pcs = get_shapefile_paths(pc_shp_folder)
    tif_list = glob.glob(tif_folder + '/*/*.tif')

    extent_df = load_new_extent() 
    run_ndvi(outpath, extent_df, tif_list)



if __name__ == "__main__":
    main()


# export LABEL='2022_05'
# export TIF_PATH='/Volumes/T9/Data_downloads/NDVI/2022_05'
# export OUTPUT_PATH='/Users/gracecolverd/New_dataset/sentinel/results_new/2022_05'
# export PC_SHP='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'
