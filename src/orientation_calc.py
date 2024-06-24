from src.pre_process_buildings import pre_process_building_data 
from src.postcode_utils import check_duplicate_primary_key, find_data_pc_joint
import numpy as np
import pandas as pd
import geopandas as gpd
import sys 

def calculate_orientation(geometry):
    """
    Calculate the orientation of the building footprint.
    """
    centroid = geometry.centroid
    minx, miny, maxx, maxy = geometry.bounds
    angle = np.arctan2(maxy - centroid.y, maxx - centroid.x) * 180 / np.pi
    orientation = (angle + 360) % 360  # Normalize the angle to be between 0 and 360
    return orientation

def categorize_orientation(angle):
    """
    Categorize orientation into cardinal directions.
    """
    if 337.5 <= angle or angle < 22.5:
        return 'North'
    elif 22.5 <= angle < 67.5:
        return 'Northeast'
    elif 67.5 <= angle < 112.5:
        return 'East'
    elif 112.5 <= angle < 157.5:
        return 'Southeast'
    elif 157.5 <= angle < 202.5:
        return 'South'
    elif 202.5 <= angle < 247.5:
        return 'Southwest'
    elif 247.5 <= angle < 292.5:
        return 'West'
    else:
        return 'Northwest'

def calc_orientation_percentage(df):
    """
    Calculate the percentage of different building orientations.
    """
    df['orientation'] = df['geometry'].apply(calculate_orientation)
    df['orientation_category'] = df['orientation'].apply(categorize_orientation)
    
    orientation_counts = df['orientation_category'].value_counts(normalize=True) * 100
    orientation_dict = orientation_counts.to_dict()

    # Ensure all categories are present in the result
    categories = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
    for category in categories:
        if category not in orientation_dict:
            orientation_dict[category] = 0.0

    return orientation_dict

def process_postcode_orientation(pc, onsud_data, INPUT_GPK):
    """
    Process one postcode to calculate orientation attributes.
    """
    pc = pc.strip()

    uprn_match = find_data_pc_joint(pc, onsud_data, input_gpk=INPUT_GPK)
    dc_full = {'postcode': pc}

    if uprn_match is None:
        print('Empty uprn match')
    elif uprn_match.empty:
        print('uprn epty')
    else:
        if not isinstance(uprn_match, gpd.GeoDataFrame):
            uprn_match = gpd.GeoDataFrame(uprn_match, geometry='geometry')
        print(uprn_match)
       
        df = pre_process_building_data(uprn_match)
        if len(df) != len(uprn_match):
            raise Exception('Error in pre-process - some cols dropped?')

        if check_duplicate_primary_key(df, 'upn'):
            print('Duplicate primary key found for upn')
            sys.exit()

        dc_full.update(calc_orientation_percentage(df))

    return dc_full

def run_orientation_calc(batch_ids, onsud_data, INPUT_GPK, batch_label, log_file):
    """
    Process each batch of postcodes to calculate orientation percentages.
    """
    results = []
    for pc in batch_ids:
        result = process_postcode_orientation(pc, onsud_data, INPUT_GPK)
        results.append(result)
    results_df = pd.DataFrame(results)
    results_df.to_csv(log_file, index=False)
    print(f'Batch {batch_label} processed and saved to {log_file}')
