temp_cols= ['HDD',
 'CDD',
 'HDD_summer',
 'CDD_summer',
 'HDD_winter',
 'CDD_winter']

region_cols = ['oa11cd', 'lsoa11cd', 'msoa11cd', 'ladcd', 'outcode' , 'region',
  'region_EE',
 'region_EM',
 'region_LN',
 'region_NE',
 'region_NW',
 'region_SC',
 'region_SW',
 'region_WA',
 'region_WM',
 'region_YH']

age_cols = [ 'localfill_median_age',
 'localfill_modal_age',
 'localfill_min_age',
 'localfill_max_age',
 'localfill_range_age',
 'localfill_distinct_ages',
 'localfill_iqr_age',
 'globalfill_median_age',
 'globalfill_modal_age',
 'globalfill_min_age',
 'globalfill_max_age',
 'globalfill_range_age',
 'globalfill_distinct_ages',
 'globalfill_iqr_age' 
 ]

type_cols = [ '2 storeys terraces with t rear extension_pct',
 '3-4 storey and smaller flats_pct',
 'Domestic outbuilding_pct',
 'Large detached_pct',
 'Large semi detached_pct',
 'Linked and step linked premises_pct',
 'Medium height flats 5-6 storeys_pct',
 'None_type_pct',
 'Planned balanced mixed estates_pct',
 'Semi type house in multiples_pct',
 'Small low terraces_pct',
 'Standard size detached_pct',
 'Standard size semi detached_pct',
 'Tall flats 6-15 storeys_pct',
 'Tall terraces 3-4 storeys_pct',
 'Unknown_pct',
 'Very large detached_pct',
 'Very tall point block flats_pct']

total_builds_new = ['all_types_total_buildings']

clean_res_cols = [ 'clean_res_total_buildings',
 'clean_res_premise_area_total',
 'clean_res_gross_area_total',
 'clean_res_heated_vol_fc_total',
 'clean_res_heated_vol_h_total',
 'clean_res_base_floor_total',
 'clean_res_basement_heated_vol_max_total',
 'clean_res_listed_bool_total',
'range_heated_vol',
'max_heated_vol',
'min_heated_vol',
 ]

total_builds = ['all_types_total_buildings',  'perc_all_res',
 'perc_clean_res',
 'perc_all_res_basement',
 'perc_all_res_listed']

res_cols = ['all_res_total_buildings',
 'all_res_premise_area_total',
 'all_res_gross_area_total',
 'all_res_heated_vol_fc_total',
 'all_res_heated_vol_h_total',
 'all_res_base_floor_total',
 'all_res_basement_heated_vol_max_total',
 'all_res_listed_bool_total',
]



res = ['all_res_total_buildings',
 'all_res_premise_area_total',
 'all_res_gross_area_total',
 'all_res_heated_vol_fc_total',
 'all_res_heated_vol_h_total',
 'all_res_base_floor_total',
 'all_res_basement_heated_vol_max_total',
 'all_res_listed_bool_total',
 'perc_all_res',
 'perc_clean_res',
 'perc_all_res_basement',
 'perc_all_res_listed',
 'clean_res_total_buildings',
 'clean_res_premise_area_total',
 'clean_res_gross_area_total',
 'clean_res_heated_vol_fc_total',
 'clean_res_heated_vol_h_total',
 'clean_res_base_floor_total',
 'clean_res_basement_heated_vol_max_total',
 'clean_res_listed_bool_total',
'range_heated_vol',
'max_heated_vol',
'min_heated_vol',
 ]

outb_cols = [ 'outb_res_total_buildings',
 'outb_res_premise_area_total',
 'outb_res_gross_area_total',
 'outb_res_heated_vol_fc_total',
 'outb_res_heated_vol_h_total',
 ] 

uprn_cols = [ 'all_types_uprn_count_total',
            'all_res_uprn_count_total',  
            'clean_res_uprn_count_total', ]
            # 'max_vol_per_uprn',
            # 'min_vol_per_uprn',] 


# best_cols = [ 'max_vol_per_uprn',
#             'min_vol_per_uprn',
#             'all_types_total_buildings',
#                'all_res_heated_vol_fc_total',
#  'all_res_heated_vol_h_total']


best_cols = [
    'max_vol_per_uprn',
            'min_vol_per_uprn',]
            # 'all_types_total_buildings',
              #  'all_res_heated_vol_fc_total',
#  'all_res_heated_vol_h_total'
 


pc_geom = ['postcode_area', 'postcode_density']

ndvi = ['max_ndvi']

l_fuel_pov = ['PercentageOfHouseholdsFuelPoor', 'EstimatedNumberOfFuelPoorHouseholds' ]
 
# settings_col_dict = {0: total_builds + region_cols , 
# 1 : total_builds + region_cols + temp_cols ,
# 2 : total_builds + region_cols + temp_cols + clean_res_cols, 
# 3 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols,
# 4 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + type_cols, 
# 5 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols,
# 6 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols,
# 7 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols + uprn_cols ,
# 8 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols + uprn_cols + res_cols,
# 9 : total_builds + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols + uprn_cols + res_cols,
# 10: temp_cols,
# 11:age_cols,
# 12: region_cols,
# 13: type_cols, 
# 14: total_builds,  
#  }


settings_col_dict_new = {0: temp_cols,
1:age_cols,
2: region_cols,
3: type_cols, 
4: total_builds_new,  
5: res,
6: uprn_cols, 
7: outb_cols, 
8: total_builds_new + region_cols , 
9 : total_builds_new + region_cols + temp_cols ,
10 : total_builds_new + region_cols + type_cols ,
11 : total_builds_new + region_cols + age_cols ,
12 : total_builds_new + region_cols + res, 
13 : total_builds_new + region_cols + res + outb_cols,
14 : total_builds_new + region_cols + temp_cols + res + outb_cols , 
15 : total_builds_new + region_cols + temp_cols + res + outb_cols + age_cols,
16 : total_builds_new + region_cols + temp_cols + res + outb_cols + age_cols + type_cols,
17 : total_builds_new + region_cols + temp_cols + res + outb_cols + age_cols + type_cols + uprn_cols ,
18: total_builds_new + type_cols , 

19: best_cols ,
20: best_cols + ndvi,
21: ndvi,
22: total_builds_new + region_cols +  type_cols + temp_cols + ndvi ,
23:  total_builds_new + region_cols +  type_cols + temp_cols , 

24: total_builds_new  + temp_cols + res + outb_cols + age_cols + type_cols + uprn_cols ,
25 : total_builds_new  + temp_cols + res + outb_cols + age_cols + type_cols + uprn_cols +l_fuel_pov  ,
26: l_fuel_pov, 
27:   total_builds_new  + temp_cols + l_fuel_pov + type_cols,
28:   total_builds_new  + temp_cols  + type_cols,

29: total_builds_new  +  ndvi, 
30 : total_builds_new + region_cols + temp_cols + res + outb_cols + age_cols + type_cols + uprn_cols + ndvi   , 
31 :  total_builds_new  + temp_cols  + type_cols + ndvi  ,


32: pc_geom,
33: total_builds_new + pc_geom, 
34: total_builds_new + region_cols + pc_geom, 
35: total_builds_new + region_cols + pc_geom + temp_cols, 
36 : total_builds_new + region_cols + temp_cols + res + outb_cols + age_cols + type_cols + uprn_cols  + pc_geom +  best_cols,
37 : total_builds_new + region_cols + temp_cols  + age_cols + type_cols   + pc_geom ,

38 :  total_builds_new  + temp_cols  + ndvi  + pc_geom ,
39 :  total_builds_new  + temp_cols  + ndvi   ,

40:  ['all_res_heated_vol_fc_total'] , 
41: ['all_res_heated_vol_h_total'],
42: ['all_res_gross_area_total'], 
43: ['range_heated_vol' +  'all_res_heated_vol_h_total'],
}




name_mapping = {0: 'build_region',
1: 'build_region_tmp' ,
2: 'build_region_tmp_clres',
3: 'build+region_tmp_clres_ob',
4:'build_region_tmp_clres_ob_type',
5:'build_region_tmp_clres_ob_age',
6:'build_region_tmp_clres_ob_age_type',
7:'build_region_tmp_clres_ob_age_type_uprn',
8:'build_region_tmp_clres_ob_age_type_uprn_res',
9:'build_temp_clres_ob_age_type_uprn_res',
10: 'temp',
11:'age',
12:'region',
13:'type',
14: 'build',
15: 'clres',
16: 'uprn'
}



region_mapping = {0: 'SW',
 1: 'EM',
 2: 'EE',
 3: 'WA',
 4: 'NW',
 5: 'YH',
 6: 'WM',
 7: 'SC',
 8: 'LN',
 9: 'NE'}



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
# age_census = [ 
#  'age_perc_Aged 15 years',
#  'age_perc_Aged 16 to 17 years',
#  'age_perc_Aged 25 to 29 years',
#  'age_perc_Aged 40 to 44 years',
#  'age_perc_Aged 45 to 49 years',
#  'age_perc_Aged 50 to 54 years',
#  'age_perc_Aged 55 to 59 years',
#  'age_perc_Aged 60 to 64 years',
#  'age_perc_Aged 65 years'] 

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

sex_census = [ 'sex_perc_Female',
 'sex_perc_Male']

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


settings_col_dict_census = {0: economic_census,
                            1: education_census,
                            2: ethnic_census, 
                            # 3: age_census,
                            4: household_size_census,
                            5: occupancy_census,
                            6: household_comp,
                            7: tenure_census,
                            8: central_heat_census,
                            9: deprivation,
                            10: occupation_census,
                            11: sex_census, 
                            12: average_household_size, 
                            13: all_census,
                            14: total_builds_new + all_census,  
                            15: total_builds_new + region_cols + all_census,
                            16: total_builds_new + type_cols + temp_cols +  all_census + pc_geom,
                            17:  total_builds_new + region_cols + temp_cols + res + outb_cols + age_cols + type_cols + uprn_cols  + pc_geom  + all_census + best_cols ,
                            18: total_builds_new  + temp_cols +  all_census + pc_geom,
                            19:  total_builds_new + all_census,  
                            20: total_builds_new ,
                            21:  total_builds_new  + temp_cols + res + outb_cols + age_cols + type_cols + uprn_cols  + pc_geom  + all_census + best_cols,
                                }






