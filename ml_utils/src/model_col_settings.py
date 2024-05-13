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

outb_cols = [ 'outb_res_total_buildings',
 'outb_res_premise_area_total',
 'outb_res_gross_area_total',
 'outb_res_heated_vol_fc_total',
 'outb_res_heated_vol_h_total',
 ] 

uprn_cols = [ 'all_types_uprn_count_total',
            'all_res_uprn_count_total',  
            'clean_res_uprn_count_total', 
            'max_vol_per_uprn',
            'min_vol_per_uprn',] 


settings_col_dict = {0: total_builds + region_cols , 
1 : total_builds + region_cols + temp_cols ,
2 : total_builds + region_cols + temp_cols + clean_res_cols, 
3 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols,
4 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + type_cols, 
5 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols,
6 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols,
7 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols + uprn_cols ,
8 : total_builds + region_cols + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols + uprn_cols + res_cols,
9 : total_builds + temp_cols + clean_res_cols + outb_cols + age_cols + type_cols + uprn_cols + res_cols,
10: temp_cols,
11:age_cols,
12: region_cols,
13: type_cols, 
 }


name_mapping = {0: 'build_region',
1: 'build_region_temp' ,
2: 'build+region+temp+cleanres',
3: 'build+region+temp+cleanres+outb',
4:'build+region+temp+cleanres+outb+type',
5:'build+region+temp+cleanres+outb+age',
6:'build+region+temp+cleanres+outb+age+type',
7:'build+region+temp+cleanres+outb+age+type+uprn',
8:'build+region+temp+cleanres+outb+age+type+uprn+res',
9:'build+temp+cleanres+outb+age+type+uprn+res',
10: 'temp',
11:'age',
12:'region',
13:'type'
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