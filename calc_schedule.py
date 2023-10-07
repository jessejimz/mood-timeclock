import time as t
import pandas as pd

# -------------------------------------------------------------------
# mood-timeclock | Calcs shcedule new row with playlists and songs
# -------------------------------------------------------------------
# Assuming you've already loaded your data into a DataFrame, df
df = pd.read_csv('output_elt/mood_timeclock-debug_export-20231006-02.csv')

# Define columns, we'll need this for the new "sub total" row
columns_mapping = [
    'id',
    'PROGRAM_ID',
    'PROGRAM_NAME',
    'BASKET_ID',
    'BASKET_NAME',
    'progbskt_uuid',
    'playlist_uuid',
    'START_DATE',
    'END_DATE',
    'START_TIME',
    'END_TIME',
    'TIME_SPAN',
    'PROG_ITEM_BSKT_PERC',
    'BASKET_PERCENT'
]

df = df[columns_mapping]

# Group by "Playlist/Bucket UUID"
grouped = df.groupby(['PROGRAM_ID'])

# Create an empty DataFrame to store the final result
final_df = pd.DataFrame(columns=df.columns)

# Iterate through each group, apply the aggregation function, and append to final_df
for name, group in grouped:
    # Define a custom aggregation function to concatenate the desired columns
    print('Start final timeclock report creation...')

    sub_group = group.groupby(['playlist_uuid'])
    concatenated_values = []

    print('Setting concat values structure...')
    for sub_name, tmp_sub in sub_group:
        concatenated_values.append(f"{tmp_sub['START_DATE'].iloc[0]} - {tmp_sub['END_DATE'].iloc[0]}, {tmp_sub['TIME_SPAN'].iloc[0]} \n")
        #concatenated_values.append(f"{tmp_sub['TIME_SPAN'].iloc[0]} \n")

        basket_name = tmp_sub['BASKET_NAME'].tolist()
        perc = tmp_sub['BASKET_PERCENT'].tolist()

        for temp_basket_name, temp_bskt_perc in zip(basket_name, perc):
            concatenated_values.append(f"[{temp_basket_name}] - {temp_bskt_perc} \n")

        concatenated_values.append("\n")

    # Copy 1st row of the group & Set empty values for all columns
    # except 'PROG_ITEM_BSKT_PERC'
    print('Copying 1st row of grp...')
    new_row = group.iloc[0].copy()
    new_row.loc[df.columns != 'TIME_SPAN'] = ''

    # Set the new concatenated value
    print('Synthesizing sched subtot...' + new_row['TIME_SPAN'])
    new_row['TIME_SPAN'] = ''.join(concatenated_values)
    # Subtot string
    #new_row['PROGRAM_NAME'] = group['PROGRAM_NAME'].tolist()[0] + ' Sub Total'
    new_row['PROGRAM_NAME'] = str(group['PROGRAM_NAME'].tolist()[0]) + ' Sub Total'


    print('Processing final df...')
    final_df = pd.concat([final_df, group, pd.DataFrame([new_row])], ignore_index=True)  # Concatenate group and new row

# Save the result to a CSV file
print("Generating report....")
now = int(t.time())
output_filename = 'output_report/mood_timeclock-20231005-01_' + str(now) + '.csv'
# final_df.to_csv('output_report/mood_timeclock-debug_sched-subtot_report.csv', index=False)
final_df.to_csv(output_filename, index=False)
print("Report output: " + output_filename)