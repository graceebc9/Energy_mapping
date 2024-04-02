from src.global_av import compute_global_modal_age

import geopandas as gpd
import glob 
import pandas as pd
from osgeo import ogr
import pandas as pd
import os


from src.buildings import get_bounding_boxes , calculate_bounding_boxes, generate_new_filename



# input_gpk = '/Volumes/T9/Data_downloads/Versik_building_data/2024_03_22_updated_data/UKBuildings_Edition_15_new_format_upn.gpkg' 
# output_path = '/Users/gracecolverd/New_dataset/test'


def main():
    input_gpk = os.environ.get('BUILDING_PATH')
    output_path = os.environ.get('OUTPUT_PATH')
    
    ds = ogr.Open(input_gpk)
    layer = ds.GetLayer()
    extent = layer.GetExtent()
    bounding_boxes = calculate_bounding_boxes(extent, chunk_height=10000, chunk_width=10000)
    
    
    print('boxes to process: ', len(bounding_boxes  ))
    compute_global_modal_age(bounding_boxes, input_gpk, output_path) 
    print('Complete')


if __name__ == "__main__":
    main() 