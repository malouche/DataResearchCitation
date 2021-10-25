# Databricks notebook source
# MAGIC %md # init parameters

# COMMAND ----------

from pyspark.sql import functions as func

sort_pub_year='year'
minyear='1960'
mincityear='1996'
maxyear='2020'
minyear_overall=None # this should usually be None, this is used for the lower bound filter for citation stats, otherwise includes citations to papers < minyear.
includepp=False

basePath_coreData='dbfs:/mnt/elsevier-fcads-icsrlab-databricks/default/' # path to where the datasets are stored. This is fixed for the default cluster to this value and shouldnt be changed
location_version="v007.20210818120551" # version of the dataset. You can choose once there are more versions available (currently only one version)
sample_full="full" # can only be "sample" on the default cluster

ani={'stamp':'20210801'}
sm_mapping_labels={'stamp':'20210801'}
ipr={'stamp':'20210801'}
sm_mapping_date="20210801"

tablename_ani="ani_"+ani['stamp'] # which table to load
tablename_ipr="ipr_"+ipr['stamp'] # which table to load
tablename_smc="smc_complete_"+sm_mapping_date+"_ani_"+ani['stamp']

# where to store our intermediate tables and results
basePath_project='s3a://elsevier-fcads-icsr-userdata/top_cited_scholars/20210801/'

export_filename_pattern=('career' if mincityear=='1996' else 'singleyr' if mincityear==maxyear else mincityear )+'_'+maxyear+Y4_name_postfix+('_wpp' if includepp else '_wopp')+'_extracted_'+ani['stamp'][0:6]

# COMMAND ----------

df_ani=(
  spark
  .read
  .format("parquet")
  .load(basePath_coreData+location_version+'/'+sample_full+'/'+tablename_ani+'')
)

df_ipr=(
  spark
  .read
  .format("parquet")
  .load(basePath_coreData+location_version+'/'+sample_full+'/'+tablename_ipr+'')
)


tablename_sm_map="smc_"+sm_mapping_labels['stamp']+"_classification"
df_smc_mapping_labels=spark.read.format("parquet").load(basePath_coreData+location_version+'/'+sample_full+'/'+tablename_sm_map)  

# science-metrix hybrid classification
df_smc=(
  spark
  .read
  .format("parquet")
  .load(basePath_coreData+location_version+'/'+sample_full+'/'+tablename_smc+'')
  .withColumn('subfield_match',func.lower(func.trim(func.col('subfield_hybrid'))))
  .join(df_smc_mapping_labels.withColumn('subfield_match',func.lower(func.trim(func.col('subfield')))),['subfield_match'])
  .select(
    'Eid','Domain','Field','Subfield'
  )
)

# COMMAND ----------

# MAGIC %md ## discontinued sources

# COMMAND ----------

# discontinued titles 03 June 2021:
discontinued_sources=[18665,19700182619,19700175175,16755,27819,26562,19399,13884,19700167903,19700187642,21100223579,4700151906,19700181106,10600153363,11300153315,19700187801,5100152904,21100913565,28043,28046,21100898760,17606,18500168200,4700152608,71472,100147321,19364,5100155058,20159,8300153132,6400153122,19700188317,21100399172,19700188326,21100437958,5400152617,5700165154,21100855407,10400153308,5400152637,21100334845,5400152620,5700165153,5700170931,21100332454,16300154755,21100255395,70864,10600153357,21100469375,19700175302,21100791821,5700161108,25166,4700151914,22756,21100225606,4600151508,19978,20100195016,16228,16500154705,10600153337,13600154732,21100201062,11300153309,12000154492,17100154710,15600154708,17600155134,19700175036,19700171018,19632,19700174904,21000195625,19700174931,17800156756,16500154706,16500154707,21100198464,17700155011,21100367736,30411,19700174627,11300153722,7900153132,21719,12300154715,21100202936,28594,18412,7200153130,19700176044,5100152606,15300154804,20500195433,25253,17266,28657,16127,21100784750,27490,21100435543,50077,4800152402,17900156733,21100205702,19182,16390,16395,16402,4000148801,29239,62974,65449,21100223146,263710499,29444,28633,21100868092,21100825150,29851,21100265048,4000151703,11300153738,21100316027,5800198357,21100872051,6500153240,21100228084,21100831810,19700190354,19700188428,19700200724,144676,12446,19600164100,5600153105,19700174893,5200152617,13100154702,7200153143,21100239831,21100202909,28720,15458,51117,17895,21100237426,15642,21100235609,15400155900,19700182042,19700182031,16061,21100205743,19872,19700175101,21100856538,21100227410,21100854119,28109,17700156205,145357,21100232418,21100195303,4900153302,21100200821,21100863640,4700152772,4400151716,89410,21100216333,19700176236,14148,21100244835,17900156722,21795,21800,17900156726,27958,145526,18551,23632,28195,37673,19700181240,19700200853,14000156160,19900192601,63434,14243,15687,18082,19700174813,17700156513,25980,25975,21100201055,21100886224,28739,4500151521,17700156703,19700188348,15196,14671,19700188435,21100201522,21100201065,14714,19700166519,19300157107,20600195618,19900191942,19900192205,19900191946,19900191924,19900192202,19900191928,19900192206,21100495829,19900191923,19900192209,19900192207,19900191927,19900191916,19900191925,21100521165,19900191965,20500195412,19900192210,19900191960,19900192208,19900191939,19900191926,19900191919,20500195414,19900192203,21100201982,21100856144,21100944103,21100829147,21100896268,19700188318,7200153152,21100218545,19700173002,21100217234,21100422125,19900193502,19900192586,19700188407,15500154707,19700174967,4700152857,21100322426,4400151502,21100792740,20400195007,19700175055,21100785495,17600155122,17600155123,21100197912,21100231630,19700200860,21100223710,19700201333,19700175758,19700188324,21100408983,17700156220,22749,19700177302,19700181206,21100890303,21100373226,21100913341,21100899502,21100200832,21100805731,78090,21100828027,17700155408,21100890290,19700174900,21100806998,12400154721,21100896634,19600161809,20500195139,21100819610,21100889409,17500155122,21100787766,21100840026,21100945713,17300154704,18100156703,17700156720,21100199803,21100814505,21100808402,19511,19700175829,21100197523,20000195080,19700174617,19800188067,21100790061,20600195619,19900192173,19700174645,19700188319,20400195018,3900148201,19700174810,19700201471,19700175060,19700174979,19700188355,4000151807,17700156008,19700182690,21100889873,21100293201,21100942112,19700175778,21100894501,21100199112,19700182218,21100846309,20200195004,17200154704,21100199850,6100153027,21100429502,19700173022,21100298063,21100205709,19700175161,4700153606,21100201525,4700152479,21100246541,21100901133,17700156323,21100408192,18800156705,19700175066,19700200831,17700155031,21100241786,15314,25299,23806,21100869510,23823,23824,26946,20500195215,21100286923,10900153329,4000151604,21100244802,25312,21100316045,21100244847,12300154727,19700175833,19700174647,19700171306,3900148513,21100264003,19203,18800156718,19700188309,18300156718,19700188484,3900148202,21100782386,21100278103,21100329555,19700175828,19700201139,19700201521,19700201516,19700188420,16400154778,21100313913,16338,19700186829,21100228316,21100920227,16693,4800152306,19300157035,23344,21100230500,21100199344,52429,21100231100,4700152483,19700176302,21100887430,145018,17100154711,17614,15500154702,3200147807,19900193655,144613,19700200708,21100237401,23413,19700201308,21100798510,19300157108,17700156404,21100415050,18300156727,19216,21100229162,21100200601,21100244634,21100223585,7400153105,21100398858,21100247092,19600164600,19700188444,19700186852,18500166400,21100241608,28546,19700186825,21100399105,19700175177,19700174933,19700175858,11200153306,144942,7700153105,25900,21100199307,19600157004,30049,23587,21100435271,13600154725,21100817618,7000153222,18800156704,23650,21100301405,21100870214,21100899004,19700186824,19700173025,20100195054,21100377768,21100332206,31872,21100201076,19700173325,16838,21100244805,21100248002,5200152804,19700177128,19700188206,19700188162,13585,12009,16505,14111,16550,6300153113,24065,13800154702,13600154710,22049,16300154705,24498,82170,21100854867,21100316064,24557,17500155017,21760,21100855844,63518,21100857169,21100283701,18500159400,13770,12100156721,21100197765,21100201971,18584,28513,28515,28531,19900191611,12986,19700186885,21100301603,110124,21100773742,24805,6700153288,20511,5700165212,29782,12930,21100446518,13900154722,19700186827,19700175151,19700186910,19300157028,11900154394,22621,21248,17675,14332,19700175122,21100215707,4400151521,22998,18280,15683,22891,21100197942,19700201509,21083,19200156706,19700174941,19700175143,4700152769,84320,20533,29201,16556,19900193211,4700152475,19400158817,20341,32824,17133,17644,21100821129,23020,20900195115,20900195116,66263,21100889429,15252,13398,15784,19400157128,64325,21100204304,17717,18626,21100890307,17600155110,19700187706,11500153415,18800156725,19700175106,17700155411,19700175045,17200154703,19700174950,17700155030,9500154041,19700174907,17700154923,19700188422,19700175031,18800156745,18800156724,19700174987,21100228751,14500154705,26700,4100151710,22219,18225,21496,25197,17600155009,11200153556,24244,19400158357,17600155138,100147021,11700154724,21100840445,21100389315,19400158329,19700194018,21100850746,130151,14268,21100904912,19900191347,19335,24221,98396,19201,19700187707,80618,21100212600,3900148509,24051,21100814517,21100198713,20000195017,13154,17284,6400153128,19700201140,21100208309,16606,23886,12997,21100265336,17600155047,20145,20180,21100199822,19700175035,19700175137,38536,19500156802,21100898670,21100856014,21100855996,5700164382,20804,21100829275,19700169710,22725,6000195383,5700191222,144842,20500195146,21100411340,19700174801,17600155114,19600157349,144806,1900147401,144885,17700156005,144808,12100154403,144813,87584,76272,19700174730,11300153601,5600152865,21416,65906,22137,18060]

# COMMAND ----------

# MAGIC %md # run base

# COMMAND ----------

# MAGIC %run "./top cited scholars - base v07c"

# COMMAND ----------

print(csvOutFileName_s1+'_top2p_bysubfield_100K_combined.csv')

# COMMAND ----------

# MAGIC %md # output

# COMMAND ----------

# MAGIC %md ## Table 1: all authors

# COMMAND ----------

df_table1_ranked_author_selection=(
  spark.read.csv(csvOutFileName_s1+'_top2p_bysubfield_100K_combined.csv',header = 'true', quote='"', escape='"')
  .orderBy(func.col('rank (ns)').cast('long').asc())
)

# COMMAND ----------

# DBTITLE 0,Table S6
display(
  df_table1_ranked_author_selection
)

# COMMAND ----------

print(csvOutFileName_s3+'_SM_SUBFIELD.csv')
print(csvOutFileName_s3+'_SM_FIELD.csv')

# COMMAND ----------

# MAGIC %md ## Table 2a: subfield aggregates

# COMMAND ----------

# DBTITLE 0,Table S8a and S8b
df_table_2_subfield=(
  spark.read.csv(csvOutFileName_s3+'_SM_SUBFIELD.csv',header = 'true', quote='"', escape='"')
  .withColumnRenamed('subject_column','subfield')
  .join(df_smc_mapping_labels,['subfield'],'LEFT_OUTER')
  .withColumn('subfield',func.coalesce('subfield',func.lit("Unassigned")))
  .orderBy(func.expr("IFNULL(domain,'ZZ')").asc(),func.asc("field"),func.expr("IF(subfield='TOTAL','ZZ',subfield)").asc())
  .select(
    func.col('domain').alias('Domain'),func.col('field').alias('Field'),func.col('subfield').alias('Subfield'),
    func.col('Auth').alias('#Auth'),
    func.col('Auth-top-100k-ns').alias('#Auth top 100k (ns)'),
    func.expr('CONCAT(ROUND((`Auth-top-100k-ns`/`Auth`)*100,2),"%")').alias('% in 100k (ns)'),
    func.col('Auth-top-100k').alias('#Auth top 100k'),
    func.expr('CONCAT(ROUND((`Auth-top-100k`/`Auth`)*100,2),"%")').alias('% in 100k'),
    func.col('Auth-in-top-list').alias('#Auth in top-list'),
    func.expr('CONCAT(ROUND((`Auth-in-top-list`/`Auth`)*100,2),"%")').alias('% in top-list'),
    func.col('Cites-25').alias('Cites@25'),
    func.col('Cites-50').alias('Cites@50'),
    func.col('Cites-75').alias('Cites@75'),
    func.col('Cites-90').alias('Cites@90'),
    func.col('Cites-95').alias('Cites@95'),
    func.col('Cites-99').alias('Cites@99'),
    func.round('c-25',3).alias('c@25'),
    func.round('c-50',3).alias('c@50'),
    func.round('c-75',3).alias('c@75'),
    func.round('c-90',3).alias('c@90'),
    func.round('c-95',3).alias('c@95'),
    func.round('c-99',3).alias('c@99'),

        # the citation stats across the entire population in the higher bands are affected by the long tail of researchers with low publication volumes
    # i.e. the self citation cutoff percentage @95 percentile = 100% self cites, because of a large group with low citation volume (of which the chance
    # of self-cites is higher)
    # therefore omitting the following columns from the results:
#     func.col('selfp-95').alias('self%@95'),
#     func.col('selfp-99').alias('self%@99'),
#     func.col('cprat-95').alias('cprat@95'),
#     func.col('cprat-99').alias('cprat@99'),
#     func.col('cprat-ns-95').alias('cprat@95 (ns)'),
#     func.col('cprat-ns-99').alias('cprat@99 (ns)'),
    
    func.col('top-list-selfp-95').alias('top-list self%@95'),
    func.col('top-list-selfp-99').alias('top-list self%@99'),
    func.col('top-list-cprat-95').alias('top-list cprat@95'),
    func.col('top-list-cprat-99').alias('top-list cprat@99'),
    func.col('top-list-cprat-ns-95').alias('top-list cprat@95 (ns)'),
    func.col('top-list-cprat-ns-99').alias('top-list cprat@99 (ns)'),
    
    # % of authors from the top-list in the top-list based top percentiles is not very meaningful. 
    # it will yield the percentile most of the time, i.e. 95th percentile = 5 percent of the authors, exception of course are ties.
    # omitting this from the result table.
#     func.expr('CONCAT(ROUND((`Auth-in-top-list-selfp-95`/`Auth-in-top-list`)*100,2),"%")').alias('% in top-list in self%@95'), 
  )
)

# COMMAND ----------

display(df_table_2_subfield)

# COMMAND ----------

# MAGIC %md ## Table 2b: field aggregates

# COMMAND ----------

df_table_2_field=(
  spark.read.csv(csvOutFileName_s3+'_SM_FIELD.csv',header = 'true', quote='"', escape='"')
  .withColumnRenamed('subject_column','field')
  .join(df_smc_mapping_labels.select('domain','field').distinct(),['field'],'LEFT_OUTER')
  .withColumn('field',func.coalesce('field',func.lit("Unassigned")))
  .orderBy(func.expr("IFNULL(domain,'ZZ')").asc(),func.expr("IF(Field='TOTAL','ZZ',Field)").asc())
  
  .select(
    func.col('domain').alias('Domain'),func.col('field').alias('Field'),
    func.col('Auth').alias('#Auth'),
    func.col('Auth-top-100k-ns').alias('#Auth top 100k (ns)'),
    func.expr('CONCAT(ROUND((`Auth-top-100k-ns`/`Auth`)*100,2),"%")').alias('% in 100k (ns)'),
    func.col('Auth-top-100k').alias('#Auth top 100k'),
    func.expr('CONCAT(ROUND((`Auth-top-100k`/`Auth`)*100,2),"%")').alias('% in 100k'),
    func.col('Auth-in-top-list').alias('#Auth in top-list'),
    func.expr('CONCAT(ROUND((`Auth-in-top-list`/`Auth`)*100,2),"%")').alias('% in top-list'),
    func.col('Cites-25').alias('Cites@25'),
    func.col('Cites-50').alias('Cites@50'),
    func.col('Cites-75').alias('Cites@75'),
    func.col('Cites-90').alias('Cites@90'),
    func.col('Cites-95').alias('Cites@95'),
    func.col('Cites-99').alias('Cites@99'),
    func.round('c-25',3).alias('c@25'),
    func.round('c-50',3).alias('c@50'),
    func.round('c-75',3).alias('c@75'),
    func.round('c-90',3).alias('c@90'),
    func.round('c-95',3).alias('c@95'),
    func.round('c-99',3).alias('c@99'),
    
    # the citation stats across the entire population in the higher bands are affected by the long tail of researchers with low publication volumes
    # i.e. the self citation cutoff percentage @95 percentile = 100% self cites, because of a large group with low citation volume (of which the chance
    # of self-cites is higher)
    # therefore omitting the following columns from the results:
#     func.col('selfp-95').alias('self%@95'),
#     func.col('selfp-99').alias('self%@99'),
#     func.col('cprat-95').alias('cprat@95'),
#     func.col('cprat-99').alias('cprat@99'),
#     func.col('cprat-ns-95').alias('cprat@95 (ns)'),
#     func.col('cprat-ns-99').alias('cprat@99 (ns)'),
    
    func.col('top-list-selfp-95').alias('top-list self%@95'),
    func.col('top-list-selfp-99').alias('top-list self%@99'),
    func.col('top-list-cprat-95').alias('top-list cprat@95'),
    func.col('top-list-cprat-99').alias('top-list cprat@99'),
    func.col('top-list-cprat-ns-95').alias('top-list cprat@95 (ns)'),
    func.col('top-list-cprat-ns-99').alias('top-list cprat@99 (ns)'),
    
    # % of authors from the top-list in the top-list based top percentiles is not very meaningful. 
    # it will yield the percentile most of the time, i.e. 95th percentile = 5 percent of the authors, exception of course are ties.
    # omitting this from the result table.
#     func.expr('CONCAT(ROUND((`Auth-in-top-list-selfp-95`/`Auth-in-top-list`)*100,2),"%")').alias('% in top-list in self%@95'),  
  )
  
)


# COMMAND ----------

display(df_table_2_field)

# COMMAND ----------

# MAGIC %md ## dataset stats

# COMMAND ----------

# [x1] % of the scientists who are in the top-2% of their subdiscipline for career-long impact when self-citations are included are no longer be in the top-2% of their subdiscipline when self-citations are excluded
# [x2] % of them fall below the top 10%
# Of the [toplist_count_w_subfield] top-cited scientists of table 1 classified by a subdiscipline, [x3] have a ratio of citations over citing papers exceeding the 99th percentile for their subdiscipline
display(
  df_agg_result_parquet
  .withColumn('top_listed',func.expr(top_list_expression))
  .join(windowedTableS3(df_agg_result_parquet,func.col('sm_subfield_1'),'SM_SUBFIELD').withColumnRenamed('subject_column','sm_subfield_1'),['sm_subfield_1'],'LEFT_OUTER')
  .agg(
    func.count('*').alias('totalcount'),
    func.count(func.expr('IF(top_listed,TRUE,NULL)')).alias('toplist_count'),
    func.count(func.expr('IF(top_listed,sm_subfield_1,NULL)')).alias('toplist_count_w_subfield'),
    func.count(func.expr('IF((rank_sm_subfield_1_ws/count_sm_subfield_1 <=.02),TRUE,NULL)')).alias('auths_top2p_ws'),
    func.count(func.expr('IF((rank_sm_subfield_1_ws/count_sm_subfield_1 <=.02) AND (rank_sm_subfield_1_ns/count_sm_subfield_1 >.02),count_sm_subfield_1,NULL)')).alias('auths_top2p_ws_not_ns'),
    func.count(func.expr('IF((rank_sm_subfield_1_ws/count_sm_subfield_1 <=.02) AND (rank_sm_subfield_1_ns/count_sm_subfield_1 >.1),count_sm_subfield_1,NULL)')).alias('auths_top2p_ws_not_top_10p_ns'),
    func.count(func.expr('IF(ws_cprat>=`top-list-cprat-99`,IF(top_listed,ws_cprat,NULL),NULL)')).alias('x3_cprat_above_p99_top-list'),
    func.count(func.expr('IF(top_listed,IF(sm_subfield_1 IS NULL, NULL, ws_cprat),NULL)')).alias('toplist_count_w_subfield_w_ws_cprat'),
  )
  .withColumn('x1_fraction_2p_ws_2p_ns_dropout',func.expr('auths_top2p_ws_not_ns/auths_top2p_ws'))
  .withColumn('x2_fraction_2p_ws_10p_ns_dropout',func.expr('auths_top2p_ws_not_top_10p_ns/auths_top2p_ws'))
)

# COMMAND ----------

# MAGIC %md ## self-rate dist

# COMMAND ----------

# cprat = the average number of citations per unique citing document.
display(
  df_agg_result_parquet
  .withColumn('subfield_rec_count',func.when(func.col('sm_subfield_1').isNull(),func.lit(None)).otherwise(func.count('*').over(Window.partitionBy('sm_subfield_1'))))
  .withColumn('cprat_perc',func.when(func.col('sm_subfield_1').isNull()|func.col('ws_cprat').isNull(),func.lit(None)).otherwise(func.rank().over(Window.partitionBy('sm_subfield_1').orderBy(func.asc('ws_cprat')))/func.col('subfield_rec_count')))
  .withColumn('top_listed',func.expr(top_list_expression))
  .filter('sm_subfield_1="Nanoscience & Nanotechnology"')
  #.filter('top_listed')
  .filter('ws_cprat<4')
  .select('author_id','ws_cprat','cprat_perc','ws_ncY2Y3','ws_ncY2Y3_cp','top_listed')
)

# COMMAND ----------

# MAGIC %md ## Table 3: Max values
# MAGIC To assist self-calculating a c-score.

# COMMAND ----------

df_table_3_maxvalues=(
  spark.read.format('csv').option('header',True).load(csvOutFileName_s1+'_lnmaxvalues.csv')
  .select(
    *[
      func.col('ws_maxl'+i[0]).alias(i[1]) for i in [['nc',f'nc{Y2}{Y3}'],['h',f'h{Y3}'],['hm',f'hm{Y3}'],['ns','ncs'],['nsf','ncsf'],['nsfl','ncsfl']]
    ]+[
      func.col('ns_maxl'+i[0]).alias(i[1]+" (ns)") for i in [['nc',f'nc{Y2}{Y3}'],['h',f'h{Y3}'],['hm',f'hm{Y3}'],['ns','ncs'],['nsf','ncsf'],['nsfl','ncsfl']]
    ]
  )
)
display(df_table_3_maxvalues)

# COMMAND ----------

# MAGIC %md # Excel export

# COMMAND ----------

# MAGIC %md ## Table 1: ranked author list

# COMMAND ----------

# download link:
url=gen_workbook_table1(f'Table_1_Authors_{export_filename_pattern}',df_table1_ranked_author_selection,key_data)
print('download result:')
print(url)

# COMMAND ----------

# MAGIC %md ## Tables 2: field/subfield

# COMMAND ----------

# download link:
url=gen_workbook_table2_field_subfield(f'Table_2_field_subfield_thresholds_{export_filename_pattern}',df_table_2_field,df_table_2_subfield,data_cols_width_styles_table2_field,data_cols_width_styles_table2_subfield)
print('download result:')
print(url)

# COMMAND ----------

# MAGIC %md ## Table 3

# COMMAND ----------

# download link:
url=gen_workbook_table3_maxvals(f'Table_3_maxlog_{export_filename_pattern}',data_cols_width_styles_table3)
print('download result:')
print(url)

# COMMAND ----------


