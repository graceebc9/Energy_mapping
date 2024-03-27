
#!/bin/bash

# Base directory where the files are located
BASE_DIR='/rds/user/gb669/hpc-work/energy_map/data/onsud_files/Data'

# List of filenames
FILENAMES=(
'ONSUD_DEC_2022_EE.csv'
'ONSUD_DEC_2022_EM.csv'
'ONSUD_DEC_2022_LN.csv'
'ONSUD_DEC_2022_NE.csv'
'ONSUD_DEC_2022_NW.csv'
'ONSUD_DEC_2022_SC.csv'
'ONSUD_DEC_2022_SE.csv'
'ONSUD_DEC_2022_SW.csv'
'ONSUD_DEC_2022_WA.csv'
'ONSUD_DEC_2022_WM.csv'
'ONSUD_DEC_2022_YH.csv'
)

# Loop through each filename and submit a job
for FILENAME in "${FILENAMES[@]}"; do
  FULL_PATH="${BASE_DIR}/${FILENAME}"
  export ONSUD_PATH="$FULL_PATH"
  sbatch --export=ONSUD_PATH submit_script.sh
done

