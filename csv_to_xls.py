import time as t
import pandas as pd
import glob
from core.mood_timeclock import calc_basket_window_size_secs, \
    calc_programming_duration, calc_prog_as_percent_of_basket
import sys


z = 'output_report/mood_timeclock-20231005-01_1696566285.csv'
colnames_program_def = ['ID_DEFPRG', 'PROGRAM ID', 'PROGRAM']
df_timeclock = pd.read_csv(z)
print('Report SPECS')
print(df_timeclock.info(memory_usage='deep'))

# Save to Excel and add a time stamp
now = int(t.time())
output_filename = 'output_report/mood_timeclock-20231005-01_1696566285.xlsx'
df_timeclock.to_excel(output_filename, index=False)

df_timeclock.drop(df_timeclock.index, inplace=True)
df_report = None
sys.exit()