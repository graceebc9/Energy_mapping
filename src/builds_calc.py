from src.fuel_calc import gen_nulls

from src.pre_process_buildings import pre_process_building_data 
from src.postcode_utils import check_duplicate_primary_key , find_data_pc_joint, find_data_pc, find_postcode_for_ONSUD_file
import numpy as np
from src.overlap import custom_load_onsud 
import pandas as pd
import sys 
import numpy as np  


def calc_build_attr(df):
    df[df['']]

def process_postcode(pc, onsud_data, INPUT_GPK, overlap = False, batch_dir=None, path_to_pcshp=None  ):
    """Process one postcode, deriving building attributes and electricity and fuel info.
    
    Inputs: 
    
    pc: postcode 
    onsud_data: output of find_postcode_for_ONSUD_file, tuples of data, pc_shp 
    gas_df: gas uk gov data
    elec_df: uk goc elec data 
    INPUT_GPK: building file verisk 
    overlap: bool, is this for the overlapping postcodes? 
    batch_dir = needed for overlap - where are the batche stored?
    path_to_schp: path to postcode shapefiles location , needed for overlap 
    """
    pc = pc.strip() 

    if overlap ==True: 
        print('starting overlap pc')
        onsud_data = custom_load_onsud(pc, batch_dir)
        _, onsud_data = find_postcode_for_ONSUD_file(onsud_data, path_to_pcshp )
        
    
    uprn_match= find_data_pc_joint(pc, onsud_data, input_gpk=INPUT_GPK)
    dc_full = {'postcode': pc  }

    if uprn_match.empty:
        print('Empty uprn match')
        dc =  gen_nulls()
        print(len(dc) ) 
    else:
        df  = pre_process_building_data(uprn_match)    
        if len(df)!=len(uprn_match):
            raise Exception('Error in pre process - some cols dropped? ')
        dc = dummm(df)
        if df is not None:
            if check_duplicate_primary_key(df, 'upn'):
                print('Duplicate primary key found for upn')
                sys.exit()
    dc_full.update(dc)

    return dc_full
