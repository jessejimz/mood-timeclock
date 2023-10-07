import time as t
import glob
import pandas as pd
from core.mood_timeclock import calc_basket_window_size_secs, \
    calc_programming_duration, alc_prog_as_percent_of_basket
import sys

# ---------
# Usage: p
# ---------


def extract_program_data(src_data_filepath, destination_filepath):
    """ Extracts only Program data from source and saves/appends to CSV file"""
    print('Extracting Program data and reducing...')

    colnames_program = ['ID_DEFPRG', 'PROGRAM ID', 'PROGRAM']
    chunk_num = 0
    for df_prog_trans in pd.read_csv(src_data_filepath,
                                     usecols=colnames_program,
                                     chunksize=100000, 
                                     encoding='unicode_escape', 
                                     engine='python'):
        print('Droping duppes')
        df_prog_trans.drop_duplicates(subset=['ID_DEFPRG'], keep='first')
        print(f'Processing Program data chunk: {chunk_num}')

        if (chunk_num > 0):
            df_prog_trans.to_csv(destination_filepath, index=False, mode='a', 
                                 header=None)
        else:
            # df_prog_trans = df_prog_trans.ID_DEFPRG != 'ID_DEFPRG'
            # df_prog_trans = df_prog_trans.iloc[1:]
            df_prog_trans.to_csv(destination_filepath, index=False, mode='a')

        chunk_num += 1

        # Release mem
        df_prog_trans.drop(df_prog_trans.index, inplace=True)
        # print(df_prog_trans.info(memory_usage='deep'))


def extract_basket_data(src_data_filepath, destination_filepath):
    """ Extracts only Basket data from src data and saves/appends 
    to CSV file """
    print('Extracting Basket data and reducing...')

    colnames_bskt = ['ID_DEFBSK', 'BASKET ID', 'BASKET']
    chunk_num = 0
    for df_bskt_trans in pd.read_csv(src_data_filepath, usecols=colnames_bskt, 
                                     chunksize=10000, 
                                     encoding='unicode_escape', 
                                     engine='python'):
        print('Droping duppes')
        df_bskt_trans.drop_duplicates(subset=['ID_DEFBSK'], keep='first')
        print(f'Processing Basket data chunk: {chunk_num}')
        
        if (chunk_num > 0):
            df_bskt_trans.to_csv(destination_filepath, index=False, mode='a', 
                                 header=None)
        else:
            df_bskt_trans.to_csv(destination_filepath, index=False, mode='a')
        
        chunk_num += 1

        df_bskt_trans.drop(df_bskt_trans.index, inplace=True)
        #print(df_bskt_trans.info(memory_usage='deep'))


def clean_unique_by_column(src_data_filepath, the_colnames_list, 
                           destination_filepath):
    """ Cleans src data by specified column name, and outputs to CSV file """
    df_cleanse = pd.read_csv(src_data_filepath)
    #drop on specific column
    tmp = df_cleanse.drop_duplicates(subset=the_colnames_list, keep=False)
    tmp.to_csv(destination_filepath, index=False, mode='a')

###############################################################################
# ------ PIPELINE STEP 1: DATA PREPARATION --------
# 1.1: Take Program & Basket detailed definitions and reduce to req'd fields & save to file
#extract_program_data(
#    'data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING.csv', 
#    'data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-programs.csv')
#extract_basket_data('data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING.csv', 'data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-baskets.csv')

# 1.2: Extract unique Programs
#cleanse_prog_cols = ['ID_DEFPRG', 'PROGRAM']
#clean_unique_by_column('data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-programs.csv', cleanse_prog_cols, 'data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-programs-cleansed.csv')

# 1.3: Extract unique Baskets
#cleanse_prog_cols = ['BASKET ID', 'BASKET']
#clean_unique_by_column('data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-baskets.csv', cleanse_prog_cols, 'data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-baskets-cleansed.csv')

#sys.exit()
#------ PIPELINE STEP 2: Load Reduced Program Defs and merge with Data ---------------------------

# 2.1: Load Program object/data for Merging later
program_defs_file = 'data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-programs.csv'
colnames_program_def = ['ID_DEFPRG', 'PROGRAM ID', 'PROGRAM']
df_program_defs = pd.read_csv(program_defs_file, usecols=colnames_program_def)
print('PROGRAM DEFS DF SPECS')
print(df_program_defs.info(memory_usage='deep'))
#drop first row, which is column names causing us headaches
df_program_defs = df_program_defs.iloc[1:] 

""" Contains list of Dataframes loaded from CSV files """
df_list = []

# 2.2: Load actual program data files
#csv_file = 'data/TBL_LN_BLEH_PARTIAL_202305311803.csv'
data_types = {'ID_DEFPRG': 'int', 'ID_DEFBSK': 'int', 'PROG_LINE': 'int', 
              'START_DATE': 'string', 'END_DATE': 'string', 
              'START_TIME': 'int', 'END_TIME': 'int'}
colnames = ['ID_DEFPRG', 'ID_DEFBSK', 'PROG_LINE', 'START_DATE', 'END_DATE', 
            'START_TIME', 'END_TIME']

# TODO: Iterate through files & combine---
for one_file_name in glob.glob('data/TBL_LN_PRGDEF_BSKDEF_202305311803*.csv'):
    print(f'Loading {one_file_name}')

    # Optimize for min memory usage
    new_df = pd.read_csv(one_file_name,  delimiter=',', header=0,
                         usecols=colnames)
    new_df['ID_DEFPRG'] = new_df['ID_DEFPRG'].astype('int64')
    new_df['ID_DEFPRG'] = new_df['ID_DEFPRG'].astype('int64')
    new_df['ID_DEFBSK'] = new_df['ID_DEFBSK'].astype('int64')
    new_df['PROG_LINE'] = new_df['PROG_LINE'].astype('int64')
    new_df['START_DATE'] = pd.to_datetime(new_df['START_DATE'])
    new_df['END_DATE'] = pd.to_datetime(new_df['END_DATE'])
    new_df['START_TIME'] = new_df['START_TIME'].astype('int64')
    new_df['END_TIME'] = new_df['END_TIME'].astype('int64')

    df_list.append(new_df)

tot_files_loaded = len(df_list)
print(f'Total files loaded: {tot_files_loaded}')

df_merged = None
if tot_files_loaded > 0:
    df_combined = pd.concat(df_list)
    print('SRC DATA CLEANSED REDUCED SPECS')
    print(df_combined.info(memory_usage='deep'))

    print('Merging Program defs...')
    # BUG
    df_merged = df_combined.join(df_program_defs, on='ID_DEFPRG', rsuffix='_r', 
                                 how='left')
    df_program_defs.drop(df_program_defs.index, inplace=True)
    df_program_defs = None
    df_combined.drop(df_combined.index, inplace=True)
    df_combined = None
    print(df_merged)
    print('SRC DATA + PROGRAM DEFS MERGED DF SPECS')
    print(df_merged.info(memory_usage='deep'))

# Cleanup
df_list.clear()
df_list = None

# TODO - Fix issue where > 100 GB swap file used!!!!!
#Load Basket object/data & Merge
# basket_defs_file = 'data/TBL_LN_PRGDEF_BSKDEF_202304182317-WORKING_reduced-baskets.csv'
# colnames_basket_defs = ['ID_DEFBSK', 'BASKET ID', 'BASKET']
# df_basket_defs = pd.read_csv(basket_defs_file, usecols=colnames_basket_defs)
# print(df_basket_defs.info(memory_usage='deep'))
# df_basket_defs = df_basket_defs.iloc[1:]

# if tot_files_loaded > 0:
#     print('Merging Basket defs...')
#     df_merged = pd.merge(df_merged, df_basket_defs[['ID_DEFBSK', 'BASKET ID', 'BASKET']], on='ID_DEFBSK', how='left')
#     df_basket_defs.drop(df_basket_defs.index, inplace=True)
#     df_basket_defs = None
#     print(df_merged)
#     print(df_merged.info(memory_usage='deep'))

#df_merged.drop(df_merged.index, inplace=True)
#df_merged = None

#sys.exit()

#------ Calculate Report --------------------------
# WHERE I LEFT OFF: Output Report w/o Basket data until fix issue of Mem over-consumption!!!
# Issue seems to be upon merge of Program defs, rows BLOW UP from 794,572 to 69,517,474

#df_merged = pd.read_csv(csv_file, delimiter=',', header=0, usecols=colnames)
#df_merged = df_merged.iloc[1:]
df_merged['START_DATE'] = pd.to_datetime(df_merged['START_DATE'])
df_merged['END_DATE'] = pd.to_datetime(df_merged['END_DATE'])
print(df_merged)

# Step 1 = Calculate Basket window size, in seconds
df_merged['BSKT_SIZE'] = calc_basket_window_size_secs(df_merged['START_DATE'], 
                                                      df_merged['END_DATE'])
df_merged['BSKT_SIZE'] = df_merged['BSKT_SIZE'].astype(int)

# Step 2: Calculate Programming duration (seconds?)
df_merged['PROG_DURATION'] = calc_programming_duration(
    df_merged['START_TIME'].astype(int), df_merged['END_TIME'].astype(int))

# Step 3: Calculate Programming as percent of Basket
df_merged['Time'] = 'ToDo'
df_merged['Item Percentage'] = calc_prog_as_percent_of_basket(
    df_merged['PROG_DURATION'], df_merged['BSKT_SIZE']) * 100
df_merged['BASKET ID'] = 'ToDo'
df_merged['BASKET'] = 'ToDo'
# Step 4: Create report file
df_merged = df_merged.rename(
    columns={'ID_DEFPRG': 'ID_DEFPRG', 
             'PROGRAM ID_r': 'Program ID', 
             'PROGRAM_r': 'Program', 
             'ID_DEFBSK': 'ID_DEFBSK', 
             'BASKET ID': 'Basket ID', 
             'BASKET': 'Basket', 
             'PROG_LINE': 'Prog Item ID', 
             'BSKT_SIZE': 'Basket Size Secs',
             'PROG_DURATION': 'Prog Item Duration Secs'})
print(df_merged)
print('REPORT DF SPECS')
print(df_merged.info(memory_usage='deep'))

sys.exit()

# Save to Excel and add a time stamp
now = int(t.time())
output_filename = 'output_report/timeclock_report_' + str(now) + '.xlsx'
df_merged.to_excel(output_filename, index=False)

df_merged.drop(df_merged.index, inplace=True)
df_report = None
sys.exit()