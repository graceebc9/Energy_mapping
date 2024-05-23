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

best_cols = [ 'max_vol_per_uprn',
            'min_vol_per_uprn',
            'all_types_total_buildings',
               'all_res_heated_vol_fc_total',
 'all_res_heated_vol_h_total']


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