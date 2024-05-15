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


from sentinel_utils.utils import * 

def run_ndvi(outpath, extent_df,  tif_list):
    """
    Process NDVI for each raster file and save results.

    Parameters:
        outpath (str): Output directory path.
        extent_df (pd.DataFrame): DataFrame containing shapefile extents.
        tif_list (list): List of TIFF file paths.
    """
    results = []
    for tif_path in tif_list:
        filename = os.path.basename(tif_path)
        print(filename)
        outname = os.path.join(outpath, filename.split('__ndvi')[0] + '_pcresults.csv' ) 
        if os.path.exists(outname):
            print('Results already exists')
            continue

        date_time = extract_date_from_filename(filename)
        tif_extent = get_raster_extent(tif_path)
        tif_crs = rasterio.open(tif_path).crs.to_string()
        filt_crs = rasterio.open(tif_path).crs

        extent_live = extent_df[extent_df['crs']==filt_crs].copy()
        extent_live.reset_index(inplace=True ) 
        
        for idx, row in extent_df.iterrows():
            shp_path =  row['postcode_shp_path'] 
            shp_extent = row['extent']
            if extents_overlap(tif_extent, shp_extent):
                gdf = gpd.read_file(shp_path)
                gdf = gdf.to_crs(tif_crs)
                for _, geom_row in gdf.iterrows():
                    geom = [geom_row['geometry']]
                    postcode = geom_row['POSTCODE']
                    
                    with rasterio.open(tif_path) as src:
                        try:
                            out_image, out_transform = mask(src, geom, crop=True)
                            masked_data = np.where(out_image >= -1, out_image, np.nan)
                            mean_value = np.nanmean(masked_data)
                            results.append({'postcode': postcode, 'mean_value': mean_value, 'date_time': date_time, 'tif_path': tif_path, 'shp_path': shp_path  })
                        except:
                            continue

        results_df = pd.DataFrame(results)
        results_df.to_csv(outname, index=False)
        print("Results saved successfully.")


def main():
    """
    Main function to process NDVI for Sentinel data.

    Parameters:
        pcs (list): List of shapefile paths.
        outpath (str): Output directory path.
        tif_folder (str): Folder containing TIFF files.
    """
    label =  os.environ.get('LABEL')
    pc_shp_folder = os.environ.get('PC_SHP')
    tif_folder = os.environ.get('TIF_PATH')
    outpath = os.environ.get('OUTPUT_PATH')
    outpath = os.path.join(outpath, label)
    os.makedirs(outpath, exist_ok=True)

    pcs = glob.glob(os.path.join(pc_shp_folder, 'two_letter_pc_code/*.shp')) + glob.glob(os.path.join(pc_shp_folder , 'one_letter_pc_code/*/*.shp'))
    

    tif_list = glob.glob(tif_folder + '/*/*.tif')
    
    # extent_df = get_extent(tif_list, pcs)
    extent_df = load_new_extent() 
    run_ndvi(outpath, extent_df, tif_list)


if __name__ == "__main__":

    
    main()

# Sample environment variables:
# export LABEL='2022_04'
# export TIF_PATH='/Volumes/T9/Data_downloads/NDVI/2022_04'
# export OUTPUT_PATH='/Users/gracecolverd/New_dataset/sentinel/results_new'
# export PC_SHP='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'


# Sample environment variables:
# export LABEL='2022_05'
# export TIF_PATH='/Volumes/T9/Data_downloads/NDVI/2022_04'
# export OUTPUT_PATH='/Users/gracecolverd/New_dataset/sentinel/results_new'
# export PC_SHP='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'

