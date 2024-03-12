
import geopandas as gpd
import glob 
import pandas as pd
import os
import concurrent.futures
from osgeo import ogr
import tempfile
import shutil
import pandas as pd
import os


# # Function to generate a unique filename based on bbox
# def generate_filename(bbox, prefix="bbox", directory="/Volumes/T9/postcode_data/data/geo_verisk"):
#     # Create a filename from bbox coordinates rounded to 2 decimal places for brevity
#     filename = f"{prefix}_{bbox[0]:.2f}_{bbox[1]:.2f}_{bbox[2]:.2f}_{bbox[3]:.2f}.gpkg"
#     return os.path.join(directory, filename)

# Function to generate a unique filename based on bbox
def generate_new_filename(bbox,directory, prefix="bbox", ):
    filename = f"{prefix}_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}.gpkg"
    return os.path.join(directory, filename)



def calculate_bounding_boxes(extent, chunk_width = 100000, chunk_height = 100000):
    minX, maxX, minY, maxY = extent
    bounding_boxes = []
    current_minX = minX
    while current_minX < maxX:
        current_minY = minY
        while current_minY < maxY:
            current_maxX = min(current_minX + chunk_width, maxX)
            current_maxY = min(current_minY + chunk_height, maxY)
            bounding_boxes.append((current_minX, current_minY, current_maxX, current_maxY))
            current_minY += chunk_height
        current_minX += chunk_width
    return bounding_boxes





def get_bounding_boxes(input_gpk):
    ds = ogr.Open(input_gpk)
    layer = ds.GetLayer()
    extent = layer.GetExtent()
    bounding_boxes = calculate_bounding_boxes(extent)
    # if len(bounding_boxes)!=91:
    #     raise ValueError('Error: incorrect number of bounding boxes')
    return bounding_boxes



def convert_gpk(f, log, name_dict):
    """ Convert gpkg chunks to csv to speped up runs 
    """
    print(f)
    out_f = f.replace('.gpkg', '.csv')
    
    if os.path.exists(out_f):
        print(f"Output file {out_f} already exists. Skipping.")
        return
    
    bbox = name_dict[f]
    if log[log['bbox'] == str(bbox)]['status'].iloc[0] == 'completed':
     
        print('Starting save', f)
        # Use a temporary file
        with tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(out_f), mode='w', suffix='.csv', prefix='temp_') as temp_file:
            gdf = gpd.read_file(f)
            # Convert geometry to WKT if needed
            # gdf['geometry'] = gdf['geometry'].apply(lambda x: x.wkt)
            gdf.to_csv(temp_file.name, index=False)
        
        # Move the temporary file to the final output file path
        shutil.move(temp_file.name, out_f)
        print('Finished save', f)