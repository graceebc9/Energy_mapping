total_builds_new = ['all_types_total_buildings', 'log_all_types_total_buildings',]

res = [ 
'comm_alltypes_count',
'unknown_alltypes',
'all_res_total_buildings',
'all_res_premise_area_total',
'all_res_gross_area_total',
'all_res_heated_vol_fc_total',
'all_res_heated_vol_h_total',
'all_res_base_floor_total',
'all_res_listed_bool_total',
'clean_res_total_buildings',
'clean_res_premise_area_total',
'clean_res_gross_area_total',
'clean_res_heated_vol_fc_total',
'clean_res_heated_vol_h_total',
'clean_res_base_floor_total',
'clean_res_basement_heated_vol_max_total',
'perc_all_res',
'perc_clean_res',
'perc_all_res_basement',
'perc_all_res_listed',

]

uprn_cols = [
'all_types_uprn_count_total',
'all_res_uprn_count_total',]

outb = [
'outb_res_total_buildings',
'outb_res_premise_area_total',
'outb_res_gross_area_total',
'outb_res_heated_vol_fc_total',
'outb_res_heated_vol_h_total',]

type_cols = [
'2 storeys terraces with t rear extension_pct',
'3-4 storey and smaller flats_pct',
'Domestic outbuilding_pct',
'Large detached_pct',
'Large semi detached_pct',
'Linked and step linked premises_pct',
'Medium height flats 5-6 storeys_pct',
'Planned balanced mixed estates_pct',
'Semi type house in multiples_pct',
'Small low terraces_pct',
'Standard size detached_pct',
'Standard size semi detached_pct',
'Tall flats 6-15 storeys_pct',
'Tall terraces 3-4 storeys_pct',
'Very large detached_pct',
'Very tall point block flats_pct',
'all_unknown_pct',
]

age_cols = [
'1919-1944_pct',
'1945-1959_pct',
'1960-1979_pct',
'1980-1989_pct',
'1990-1999_pct',
'None_age_pct',
'Post 1999_pct',
'Pre 1919_pct',
'Unknown_age_pct',] 

temp_cols = ['HDD',
'CDD',
'HDD_summer',
'CDD_summer',
'HDD_winter',
'CDD_winter',
] 

postcode_geoms = [
'postcode_area',
'postcode_density',
'log_pc_area',]

region_cols =[ 
'region',
'oa11cd',
'lsoa11cd',
'msoa11cd',
'ladcd' ] 




rural_urban = [
'RUC11CD',
'RUC11']


economic_census = [ 
'economic_activity_perc_Does not apply',
'economic_activity_perc_Economically active (excluding full-time students): In employment: Employee: Part-time',
'economic_activity_perc_Economically active (excluding full-time students): In employment: Employee: Full-time',
'economic_activity_perc_Economically active (excluding full-time students): In employment: Self-employed with employees: Part-time',
'economic_activity_perc_Economically active (excluding full-time students): In employment: Self-employed with employees: Full-time',
'economic_activity_perc_Economically active (excluding full-time students): In employment: Self-employed without employees: Part-time',
'economic_activity_perc_Economically active (excluding full-time students): In employment: Self-employed without employees: Full-time',
'economic_activity_perc_Economically active (excluding full-time students): Unemployed: Seeking work or waiting to start a job already obtained: Available to start working within 2 weeks',
'economic_activity_perc_Economically active and a full-time student: In employment: Employee: Part-time',
'economic_activity_perc_Economically active and a full-time student: In employment: Employee: Full-time',
'economic_activity_perc_Economically active and a full-time student: In employment: Self-employed with employees: Part-time',
'economic_activity_perc_Economically active and a full-time student: In employment: Self-employed with employees: Full-time',
'economic_activity_perc_Economically active and a full-time student: In employment: Self-employed without employees: Part-time',
'economic_activity_perc_Economically active and a full-time student: In employment: Self-employed without employees: Full-time',
'economic_activity_perc_Economically active and a full-time student: Unemployed: Seeking work or waiting to start a job already obtained: Available to start working within 2 weeks',
'economic_activity_perc_Economically inactive: Retired',
'economic_activity_perc_Economically inactive: Student',
'economic_activity_perc_Economically inactive: Looking after home or family',
'economic_activity_perc_Economically inactive: Long-term sick or disabled',
'economic_activity_perc_Economically inactive: Other',
]

education_census = [  'highest_qual_perc_Does not apply',
'highest_qual_perc_No qualifications',
'highest_qual_perc_Level 1 and entry level qualifications: 1 to 4 GCSEs grade A* to C, Any GCSEs at other grades, O levels or CSEs (any grades), 1 AS level, NVQ level 1, Foundation GNVQ, Basic or Essential Skills',
'highest_qual_perc_Level 2 qualifications: 5 or more GCSEs (A* to C or 9 to 4), O levels (passes), CSEs (grade 1), School Certification, 1 A level, 2 to 3 AS levels, VCEs, Intermediate or Higher Diploma, Welsh Baccalaureate Intermediate Diploma, NVQ level 2, Intermediate GNVQ, City and Guilds Craft, BTEC First or General Diploma, RSA Diploma',
'highest_qual_perc_Apprenticeship',
'highest_qual_perc_Level 3 qualifications: 2 or more A levels or VCEs, 4 or more AS levels, Higher School Certificate, Progression or Advanced Diploma, Welsh Baccalaureate Advance Diploma, NVQ level 3; Advanced GNVQ, City and Guilds Advanced Craft, ONC, OND, BTEC National, RSA Advanced Diploma',
'highest_qual_perc_Level 4 qualifications or above: degree (BA, BSc), higher degree (MA, PhD, PGCE), NVQ level 4 to 5, HNC, HND, RSA Higher Diploma, BTEC Higher level, professional qualifications (for example, teaching, nursing, accountancy)',
'highest_qual_perc_Other: vocational or work-related qualifications, other qualifications achieved in England or Wales, qualifications achieved outside England or Wales (equivalent not stated or unknown)',
]

occupation_census = [ 'occupation_perc_Does not apply',
'occupation_perc_1. Managers, directors and senior officials',
'occupation_perc_2. Professional occupations',
'occupation_perc_3. Associate professional and technical occupations',
'occupation_perc_4. Administrative and secretarial occupations',
'occupation_perc_5. Skilled trades occupations',
'occupation_perc_6. Caring, leisure and other service occupations',
'occupation_perc_7. Sales and customer service occupations',
'occupation_perc_8. Process, plant and machine operatives',
'occupation_perc_9. Elementary occupations',
]
ethnic_census = [ 
'ethnic_group_perc_Does not apply',
'ethnic_group_perc_Asian, Asian British or Asian Welsh: Bangladeshi',
'ethnic_group_perc_Asian, Asian British or Asian Welsh: Chinese',
'ethnic_group_perc_Asian, Asian British or Asian Welsh: Indian',
'ethnic_group_perc_Asian, Asian British or Asian Welsh: Pakistani',
'ethnic_group_perc_Asian, Asian British or Asian Welsh: Other Asian',
'ethnic_group_perc_Black, Black British, Black Welsh, Caribbean or African: African',
'ethnic_group_perc_Black, Black British, Black Welsh, Caribbean or African: Caribbean',
'ethnic_group_perc_Black, Black British, Black Welsh, Caribbean or African: Other Black',
'ethnic_group_perc_Mixed or Multiple ethnic groups: White and Asian',
'ethnic_group_perc_Mixed or Multiple ethnic groups: White and Black African',
'ethnic_group_perc_Mixed or Multiple ethnic groups: White and Black Caribbean',
'ethnic_group_perc_Mixed or Multiple ethnic groups: Other Mixed or Multiple ethnic groups',
'ethnic_group_perc_White: English, Welsh, Scottish, Northern Irish or British',
'ethnic_group_perc_White: Irish',
'ethnic_group_perc_White: Gypsy or Irish Traveller',
'ethnic_group_perc_White: Roma',
'ethnic_group_perc_White: Other White',
'ethnic_group_perc_Other ethnic group: Arab',
'ethnic_group_perc_Other ethnic group: Any other ethnic group',
]



household_size_census = [ 
'household_siz_perc_perc_0 people in household',
'household_siz_perc_perc_1 person in household',
'household_siz_perc_perc_2 people in household',
'household_siz_perc_perc_3 people in household',
'household_siz_perc_perc_4 people in household',
'household_siz_perc_perc_5 people in household',
'household_siz_perc_perc_6 people in household',
'household_siz_perc_perc_7 people in household',
'household_siz_perc_perc_8 or more people in household',

]
occupancy_census = [  'occupancy_rating_perc_Does not apply',
'occupancy_rating_perc_Occupancy rating of bedrooms: +2 or more',
'occupancy_rating_perc_Occupancy rating of bedrooms: +1',
'occupancy_rating_perc_Occupancy rating of bedrooms: 0',
'occupancy_rating_perc_Occupancy rating of bedrooms: -1',
'occupancy_rating_perc_Occupancy rating of bedrooms: -2 or less',
]

household_comp = [  'household_comp_by_bedroom_perc_Does not apply_Does not apply',
'household_comp_by_bedroom_perc_Does not apply_1 bedroom',
'household_comp_by_bedroom_perc_Does not apply_2 bedrooms',
'household_comp_by_bedroom_perc_Does not apply_3 bedrooms',
'household_comp_by_bedroom_perc_Does not apply_4 or more bedrooms',
'household_comp_by_bedroom_perc_One-person household_Does not apply',
'household_comp_by_bedroom_perc_One-person household_1 bedroom',
'household_comp_by_bedroom_perc_One-person household_2 bedrooms',
'household_comp_by_bedroom_perc_One-person household_3 bedrooms',
'household_comp_by_bedroom_perc_One-person household_4 or more bedrooms',
'household_comp_by_bedroom_perc_Single family household: All aged 66 years and over_Does not apply',
'household_comp_by_bedroom_perc_Single family household: All aged 66 years and over_1 bedroom',
'household_comp_by_bedroom_perc_Single family household: All aged 66 years and over_2 bedrooms',
'household_comp_by_bedroom_perc_Single family household: All aged 66 years and over_3 bedrooms',
'household_comp_by_bedroom_perc_Single family household: All aged 66 years and over_4 or more bedrooms',
'household_comp_by_bedroom_perc_Single family household: Couple family household_Does not apply',
'household_comp_by_bedroom_perc_Single family household: Couple family household_1 bedroom',
'household_comp_by_bedroom_perc_Single family household: Couple family household_2 bedrooms',
'household_comp_by_bedroom_perc_Single family household: Couple family household_3 bedrooms',
'household_comp_by_bedroom_perc_Single family household: Couple family household_4 or more bedrooms',
'household_comp_by_bedroom_perc_Single family household: Lone parent household_Does not apply',
'household_comp_by_bedroom_perc_Single family household: Lone parent household_1 bedroom',
'household_comp_by_bedroom_perc_Single family household: Lone parent household_2 bedrooms',
'household_comp_by_bedroom_perc_Single family household: Lone parent household_3 bedrooms',
'household_comp_by_bedroom_perc_Single family household: Lone parent household_4 or more bedrooms',
'household_comp_by_bedroom_perc_Other household types_Does not apply',
'household_comp_by_bedroom_perc_Other household types_1 bedroom',
'household_comp_by_bedroom_perc_Other household types_2 bedrooms',
'household_comp_by_bedroom_perc_Other household types_3 bedrooms',
'household_comp_by_bedroom_perc_Other household types_4 or more bedrooms',
]

tenure_census = [ 
'tenure_perc_Does not apply',
'tenure_perc_L1, L2 and L3: Higher managerial, administrative and professional occupations',
'tenure_perc_L4, L5 and L6: Lower managerial, administrative and professional occupations',
'tenure_perc_L7: Intermediate occupations',
'tenure_perc_L8 and L9: Small employers and own account workers',
'tenure_perc_L10 and L11: Lower supervisory and technical occupations',
'tenure_perc_L12: Semi-routine occupations',
'tenure_perc_L13: Routine occupations',
'tenure_perc_L14.1 and L14.2: Never worked and long-term unemployed',
'tenure_perc_L15: Full-time students',
]

real_tenure = [] 

sex_census = [ 'sex_perc_Female',
'sex_perc_Male'
]

average_household_size = [ 'Average Household Size']

central_heat_census = [ 
'central_heating_perc_Does not apply',
'central_heating_perc_No central heating',
'central_heating_perc_Mains gas only',
'central_heating_perc_Tank or bottled gas only',
'central_heating_perc_Electric only',
'central_heating_perc_Wood only',
'central_heating_perc_Solid fuel only',
'central_heating_perc_Renewable energy only',
'central_heating_perc_District or communal heat networks only',
'central_heating_perc_Other central heating only',
'central_heating_perc_Two or more types of central heating (not including renewable energy)',
'central_heating_perc_Two or more types of central heating (including renewable energy)'
]


deprivation = [ 'deprivation_perc_Does not apply',
'deprivation_perc_Household is not deprived in any dimension',
'deprivation_perc_Household is deprived in one dimension',
'deprivation_perc_Household is deprived in two dimensions',
'deprivation_perc_Household is deprived in three dimensions',
'deprivation_perc_Household is deprived in four dimensions',
]

all_census = economic_census + education_census  + occupation_census + ethnic_census  + household_size_census + occupancy_census + household_comp + tenure_census + deprivation + sex_census + average_household_size + central_heat_census
all_vars = total_builds_new + res + outb + type_cols + age_cols + temp_cols + postcode_geoms + region_cols + uprn_cols + all_census + rural_urban
# minimal_all_vars =  total_builds_new + ['all_res_heated_vol_h_total' ] 

ndvi_cols = ['max_ndvi']

settings_col_dict_census = {
    0: ['Economic', economic_census],
    1: ['Education', education_census],
    2: ['Ethnicity', ethnic_census],
    3: ['Rural Urban', rural_urban],
    4: ['Household Size', household_size_census],
    5: ['Occupancy', occupancy_census],
    6: ['Household Comp', household_comp],
    7: ['SocioEcon Classification', tenure_census],
    8: ['Central Heat', central_heat_census],
    9: ['Deprivation', deprivation],
    10: ['Occupation', occupation_census],
    11: ['Sex', sex_census],
    12: ['Avg Household Size', average_household_size],
    # 13: ['All Census', all_census],
} 






settings_dict = {
0: ['COB' , total_builds_new ] , 
1: ['Residential BS', res],
2: ['Outbuildings BS', outb],
3: ['Typology', type_cols],
4: ['Age', age_cols],
5: ['Temperature', temp_cols],
6: ['Local Morph.', postcode_geoms],
7: ['Region', region_cols],
8: ['Count of UPRNs', uprn_cols],
9: ['Socio-Demogs', all_census ] ,
10: ['Urban/Rural',  rural_urban],
11 : ['COB, Res BS', res  + total_builds_new],
12: ['COB, Type', total_builds_new + type_cols ],
13: ['COB, Region', total_builds_new + region_cols ], 
14: ['COB, Age', total_builds_new + age_cols ],
15: ['COB, Temp', total_builds_new + temp_cols ],
16: ['COB, Local Morph.', total_builds_new + postcode_geoms ],
17: ['COB, Urban/Rural', total_builds_new  + rural_urban],
18: ['All vars', all_vars], 
19: ['COB, Region, PC Geom, Temp', total_builds_new + region_cols  +postcode_geoms +temp_cols ],
20: ['NDVI', ndvi_cols], 
21: ['COB, NDVI' , total_builds_new + ndvi_cols],
22: ['COB, NDVI, Temp, Urban/Rural' , total_builds_new + ndvi_cols + temp_cols + rural_urban], 
23: ['COB, NDVI, Temp, Urban/Rural, Local Morph.' , total_builds_new + ndvi_cols + temp_cols + rural_urban + postcode_geoms ], 
24: ['COB, NDVI, Temp, Urban/Rural, Local Morph., Type' ,  total_builds_new + ndvi_cols + temp_cols + rural_urban + postcode_geoms + type_cols ], 
25: ['COB, NDVI, Temp, Urban/Rural, Local Morph., Socio-Demogs' , total_builds_new + ndvi_cols + temp_cols + rural_urban + postcode_geoms + all_census ], 
26: ['COB, NDVI, Temp, Urban/Rural, Socio-Demogs' , total_builds_new + ndvi_cols + temp_cols + rural_urban  + all_census ], 
27: ['COB, NDVI, Temp,\n Socio-Demogs' , total_builds_new + ndvi_cols + temp_cols  + all_census ], 
28: ['COB, NDVI, Local Morph.\n Temp, Socio-Demogs' , total_builds_new + ndvi_cols + temp_cols  + all_census + postcode_geoms ], 
29: ['COB, Temp,\n Socio-Demogs', total_builds_new + temp_cols + all_census ],
30: ['COB, Temp, \n Socio-Demogs, Local Morph.' , total_builds_new + temp_cols  + all_census + postcode_geoms ], 
31: ['COB, Temp,\n NDVI', total_builds_new + temp_cols + ndvi_cols ],
32: ['COB, Temp, \n NDVI, Local Morph.' , total_builds_new + temp_cols  + ndvi_cols + postcode_geoms ], 
33: ['Temp, \n NDVI, Local Morph.' ,   temp_cols  + ndvi_cols + postcode_geoms ], 
34: ['Temp, Socio-Demogs \n NDVI, Local Morph.' ,  all_census +  temp_cols  + ndvi_cols + postcode_geoms ], 
35: ['Temp', 'Local Morph', temp_cols + postcode_geoms ] , 
36: ['Temp, Socio-Demogs, \n  Local Morph.' ,  all_census +  temp_cols + postcode_geoms ], 
}