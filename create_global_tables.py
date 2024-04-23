from src.global_av import compute_global_modal_age, compute_global_fc, compute_global_heights

import geopandas as gpd
import glob 
import pandas as pd
from osgeo import ogr
import pandas as pd
import os


from src.buildings import get_bounding_boxes , calculate_bounding_boxes, generate_new_filename


run_type = 'height'
# input_gpk = '/Volumes/T9/Data_downloads/Versik_building_data/2024_03_22_updated_data/UKBuildings_Edition_15_new_format_upn.gpkg' 
# output_path = '/Users/gracecolverd/New_dataset/proc'


def main():
    input_gpk = os.environ.get('BUILDING_PATH')
    output_path = os.environ.get('OUTPUT_PATH')
    
    ds = ogr.Open(input_gpk)
    layer = ds.GetLayer()
    extent = layer.GetExtent()
    bounding_boxes = calculate_bounding_boxes(extent, chunk_height=10000, chunk_width=10000)
    
    
    print('boxes to process: ', len(bounding_boxes  ))
    if run_type == 'age':
        compute_global_modal_age(bounding_boxes, input_gpk, output_path) 
    elif run_type =='height':
        compute_global_heights(bounding_boxes, input_gpk, output_path)
        compute_global_fc(bounding_boxes, input_gpk, output_path)
    else:
        raise Exception('Incorrect run type for global averages')
    print('Complete')


if __name__ == "__main__":
    main() 