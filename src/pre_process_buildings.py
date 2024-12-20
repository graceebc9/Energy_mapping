import pandas as pd
import numpy as np
import os 



# ============================================================
# Constants
# ============================================================
BUILD_PERC_VAL = 0.85
BASEMENT_HEIGHT = 2.4
BASEMENT_PERCENTAGE_OF_PREMISE_AREA = 1
DEFAULT_FLOOR_HEIGHT = 2.3
# MAX_THRESHOLD_FLOOR_HEIGHT = 5.3
# MIN_THRESH_FL_HEIGHT = 2.2

# ============================================================
# Data Loading Functions
# ============================================================

# current using not age split floor count 
def load_avg_floor_count():
    """Load the average floor count data from a CSV file."""
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'global_avs' , 'updated_pp_global_average_fl_count_bucket_25.csv')
    
    return pd.read_csv(csv_path)


def create_age_buckets(df):
    df['premise_age_bucketed'] = np.where(df['premise_age'].isin(['Pre 1837', '1837-1869', '1870-1918']), 'Pre 1919', df['premise_age'])
    return df 

def get_height_bins():
    height_bins = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 200]
    height_labels = [f"{b}-{height_bins[i+1]}m" for i, b in enumerate(height_bins[:-1])]
    return height_bins, height_labels

def create_height_bucket_col(df):
    """Bucket height into predefined categories."""
    df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce').fillna(0) 
    height_bins, height_labels = get_height_bins() 
    df['height_bucket'] = pd.cut(df['height_numeric'], bins=height_bins, labels=height_labels, right=False)
    return df

def create_height_bucket_cols(df, col):
    """Bucket height into predefined categories."""
    height_bins, height_labels = get_height_bins() 
    df[f'{col}_bucket'] = pd.cut(df[col], bins=height_bins, labels=height_labels, right=False)
    return df


def update_listed_type(df):
    df.loc[:, 'listed_bool'] = df['listed_grade'].apply(lambda x: 1 if x is not None else 0)
    return df 

# ============================================================
# Geometry Fns
# ============================================================


def min_side(polygon):

    # Minimum rotated rectangle
    min_rect = polygon.minimum_rotated_rectangle

    # Extract the points of the rectangle to calculate side lengths
    x, y = min_rect.exterior.coords.xy

    # Calculate distances between consecutive points (sides of the rectangle)
    distances = [np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2) for i in range(1, len(x))]

    # The least width is the minimum side length of the rectangle
    least_width = min(distances)
    return least_width 


# ============================================================
# Pre process fns 
# ============================================================


def update_outbuildings(test):
    test.loc[(test['height']==3) & (test['premise_floor_count'] == '2') & (test['uprn_count'] == 0), 'premise_type'] = 'Domestic outbuilding'
    # test = create_height_bucket_col(test)
    return test



def update_avgfloor_count_outliers(df, MIN_THRESH_FL_HEIGHT = 2.3, MAX_THRESHOLD_FLOOR_HEIGHT=5.3):
    df['min_side'] = df['geometry'].apply(min_side)
    df['threex_minside'] = [x * 3 for x in df['min_side']]
    df['validated_height'] = np.where(df['height_numeric'] >= df['threex_minside'],   np.nan,  df['height_numeric'])
    df['validated_fc'] = np.where(((df['av_fl_height']>= MAX_THRESHOLD_FLOOR_HEIGHT )| (df['av_fl_height'] <= MIN_THRESH_FL_HEIGHT )) & (df['height']< df['threex_minside']) , np.nan, df['floor_count_numeric'])
    return df 



def fill_local_averages(df):
    num_builds = len(df )

    num_fc_invalid = df.validated_fc.isna().sum() 
    num_h_invalid = df.validated_height.isna().sum() 

    if num_builds - num_fc_invalid ==0 | len(df)==1 | num_builds - num_h_invalid == 0 : 
        print('Cannot do local fill for FC')
        # height_fla = df[~df['validated_height'].isna()]['validated_height'].mean()
        raise Exception('no local fill ')

    fc_fla= df[~df['validated_fc'].isna()]['validated_fc'].mean()
    height_fla = df[~df['validated_height'].isna()]['validated_height'].mean()
    df['fc_filled'] = np.where(df['validated_fc'].isna(), fc_fla, df['validated_fc'])
    df['height_filled'] = np.where(df['validated_height'].isna(), height_fla, df['validated_height'] )
    df = create_height_bucket_cols(df, 'height_filled')
    return df 

def fill_glob_avs(df, fc = None  ):
    if fc is None:
        fc = load_avg_floor_count() 
 
    df = df.merge(fc, left_on=['map_simple_use', 'premise_age_bucketed',  'height_filled_bucket'], right_on = [ 'map_simple_use', 'premise_age_bucketed', 'height_bucket'], how='left')
    if df.empty:
        raise Exception ('Error merging with global averages')
    df.drop(columns=[ 'height_bucket','total_count'], inplace=True )
    return df 


def create_heated_vol(df):
    """
    calc heated premise are
    """
    df['heated_vol_fc'] = df['premise_area'] * df['fc_filled']
    df['heated_vol_h'] = df['premise_area'] * df['global_average_floorcount']
    
    return df 

def create_basement_metrics(df):
    basement_conditions = [
        df['basement'].isin(['Basement confirmed', 'Basement likely']),
        ~df['basement'].isin(['Basement confirmed', 'Basement likely'])
    ]
    basement_choices = [1, 0]
    df['base_floor'] = np.select(basement_conditions, basement_choices, default=0)
    df['basement_heated_vol_max'] = df['base_floor'] *  df['premise_area'] * BASEMENT_HEIGHT * BASEMENT_PERCENTAGE_OF_PREMISE_AREA 
    return df 

def pre_process_buildings(df, fc,  MIN_THRESH_FL_HEIGHT = 2.3, MAX_THRESH_FL_HEIGHT= 5.3):
    """ can only be applied   to a group where you want the local average within the group
    - bcuekts age (turns all pre into pre 1919
    - updat listed into numeric / encoded
    - update outbuilds: for those with heht 3 storey 2 uprn 0 -> outbuildings 
    - update fc outliers: use height / min width ratio and average floor height to nul out invalid heights or fc
    - fill local avs:fill the nulled with local averages 
    - fill glob averages: any local heights, convert to fc with global averages 
    - create heated vol from two diff fcs 
    - create basement metrics using whole premise area for basemenet, whole area heated (can vary this later)

    Ends up with two diff ways of getting floor count, for heated volume :
         either directly (correct fc or local av fc) 
         or through height (either correct height, or local av hegith, converted to global fc for that height)
         
    """ 
    
    df = create_age_buckets(df)
    df['height_numeric'] = pd.to_numeric(df['height'], errors='coerce')
    df['floor_count_numeric'] = pd.to_numeric(df['premise_floor_count'], errors='coerce')
    df['av_fl_height'] = df['height_numeric'] / df['floor_count_numeric']
    df=update_listed_type(df)
    df=update_outbuildings(df)
    df=update_avgfloor_count_outliers(df, MIN_THRESH_FL_HEIGHT, MAX_THRESH_FL_HEIGHT)
    # check before doing local average filles 
    
    df=fill_local_averages(df)
    df=fill_glob_avs(df, fc)
    df = create_heated_vol(df)
    df = create_basement_metrics(df)
    if df.empty:
        raise Exception('Error empty df ')
    return df 

# ============================================================
# Filter fns
# ============================================================


def produce_clean_building_data(df):
    """Filter and test building data."""
    # print("Filtering non-commercial derelict premises...")
 
    if len(df)==0:
        print('No data to process')
        return None 
    # filtered_df = df[df['premise_use'] != 'Commercial - derelict'].copy()
    fdf =df[df['premise_type']=='Residential'].copy() 
    test_building_metrics(fdf)

    return df

# ============================================================
# Validation and Testing Functions
# ============================================================
def assert_larger(df, col1, col2):
    """Ensure values in col1 are larger than those in col2 where columns are not null."""
    df = df[~df[col1].isna() & ~df[col2].isna()].copy()
    assert (df[col1] >= df[col2]).all(), f"Found rows where {col1} is not larger than {col2}."

def assert_perc(df, col):
    """Ensure values in col are between 0 and 1."""
    assert ((df[col] >= 0) & (df[col] <= 1)).all(), f"Found rows where {col} is not between 0 and 1."

def assert_equal(df, col1, col2):
    """Ensure values in col1 are equal to those in col2."""
    assert (df[col1] == df[col2]).all(), f"For df, found rows where {col1} does not equal {col2}."

def check_nulls_percent(df, col, threshold=0.5):
    """Check if the percentage of nulls in col exceeds a threshold."""
    if df[col].isna().mean() > threshold:
        raise Exception(f'Nulls in {col} are greater than {threshold*100}%.')

  

def test_building_metrics(df):
    """Run various assertions on building metrics."""


    for c in ['heated_vol_h', 'heated_vol_fc']:
        check_nulls_percent(df, c, 0)

    test = df[df['validated_height'].isna()].copy() 
    assert_larger(test, 'height', 'height_filled')

# ['premise_age', 'premise_year', 'premise_use', 'premise_type', 'premise_floor_count', 'height', 'premise_area', 'building_area',
#  'address_area', 'gross_area', 'basement', 'listed_grade', 'element_count', 'bathroom_count', 'bedroom_count', 'reception_room_count',
#   'roof_type', 'wall_type', 'substructure_type', 'glazing_type', 'wall_construction_type', 'extension_count', 'habitable_rooms',
#    'open_fireplaces', 'floor_type', 'distance_building', 'site_id', 'site_area', 'site_non_built_area', 'site_building_count',
#     'distance_water', 'verisk_building_id', 'uprn', 'uprn_count', 'uprn_distance', 'toid', 'map_age', 'map_floors', 'map_use', 
#     'map_simple_use', 'upn', 'geometry', 'premise_age_bucketed', 'height_numeric', 'floor_count_numeric', 'av_fl_height',
#      'listed_bool', 'min_side', 'threex_minside', 'validated_height', 'validated_fc', 'fc_filled', 'height_filled',
#       'height_filled_bucket', 'global_average_floorcount', 'updated', 'heated_prem_area_fc', 'heated_prem_area_h', 'base_floor', 'basement_heated_vol_max']

def pre_process_building_data(build,  MIN_THRESH_FL_HEIGHT = 2.3, MAX_THRESH_FL_HEIGHT= 5.3):
    fc = load_avg_floor_count() 
    """Calculate and validate building metrics from verisk data."""
   
    processed_df = pre_process_buildings(build, fc , MIN_THRESH_FL_HEIGHT, MAX_THRESH_FL_HEIGHT)
    
    clean_df = produce_clean_building_data(processed_df)
    
    return clean_df