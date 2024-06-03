#!/bin/bash

# Set environment variables
export BATCH_PATH='/Users/gracecolverd/New_dataset/overlapping_pcs.txt'
export DATA_DIR='/Users/gracecolverd/New_dataset/test'
export PC_SHP_PATH='/Volumes/T9/Data_downloads/codepoint_polygons_edina/Download_all_postcodes_2378998/codepoint-poly_5267291'
export GAS_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_gas_2022.csv'
export ELEC_PATH='/Volumes/T9/Data_downloads/UKGOV_Gas_elec/Postcode_level_all_meters_electricity_2022.csv'
export BUILDING_PATH='/Volumes/T9/Data_downloads/Versik_building_data/2024_03_22_updated_data/UKBuildings_Edition_15_new_format_upn.gpkg'
export OVERLAP_ONSUD_BATCH_FOLDER='/Volumes/T9/Data_downloads/new-data-outputs/overlap_batches'
export OVERLAP_BL='Yes'

# Load the IDs from the text file
IDS_FILE='/Users/gracecolverd/New_dataset/overlap_pcs_outcodes.txt'

# Check if the file exists
if [ ! -f "$IDS_FILE" ]; then
    echo "ID file not found!"
    exit 1
fi

# Function to run the Python script
run_python_script() {
    local outcode=$1
    export OVERLAP_OUTCODE="$outcode"
    python run_fuel_calc_for_batch.py
}

export -f run_python_script

# Use GNU Parallel to run the Python script concurrently for each outcode
# Limit the number of concurrent jobs to 10
parallel -j 5 run_python_script ::: $(cat "$IDS_FILE")
