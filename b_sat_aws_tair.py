# b_sat_aws_tair 

# Purpose: import and visualize air temperature data from the Satellite AWS (2023).
# It also merges the tair and rh datasets of Main and Sat AWSs and compares them visually.
# Created on Nov 24, 2023


#%% 1) Clear and import

print("\014") # clear console
# clear variable explorer w/o user confirmation
%reset -f

# 1.1) import libraries
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import os



#%% 2) Load data
# 2.1) Satellite AWS * * * * * * * * * * * * 
# a) establish "Max's Path"
mp = '/Users/maxims/Library/CloudStorage/OneDrive-UniversityOfOregon/Lab/python/aws/'
# b) create path to csv file
csv_path = mp + 'input/a_jas2023/SatAWS_tair_2023.xlsx'
# c) read the csv file using pandas
sataws = pd.read_excel(csv_path)
# d) clean up
del csv_path
# e) Make sure date is DateTime
# conditional statement that checks if date is/isn't in datetime format
if sataws['date'].dtype == 'datetime64[ns]':
    print("The 'date' is already in datetime format.")
else:
    print("Converting 'date' to datetime format.")
    sataws['date'] = pd.to_datetime(sataws['date'], format='%m/%d/%y %H:%M')
# Verify the changes
print("Currently, the data type of 'date' is: ", sataws['date'].dtype)

# 2.2) Main AWS * * * * * * * * * * * * 
# a) establish "Max's Path"
# create path to csv file
csv_path = mp + 'input/a_jas2023/hayden_jas2023.csv'
# c) read the csv file using pandas
jas23 = pd.read_csv(csv_path)
# d) clean up
del csv_path
# e) conditional statement that checks if date is/isn't in datetime format
if jas23['date'].dtype == 'datetime64[ns]':
    print("The 'date' is already in datetime format.")
else:
    print("Converting 'date' to datetime format.")
    jas23['date'] = pd.to_datetime(jas23['date'], format='%m/%d/%y %H:%M')
# Verify the changes
print("Data type of the 'date' after conversion:", jas23['date'].dtype)

# rename both for future easier manipulation
df_main = jas23; df_sat = sataws; del jas23, sataws

# dt_sat ends with :35 seconds, so this line will turn it to zeros
df_sat['date'] = df_sat['date'].dt.floor('min')




#%% 3) Merge the 2 AWS data (for tair and rh specifically)

# a) Extract the start and end times from df_main
start_time = df_main['date'].min()
end_time = df_main['date'].max()

# b): Create a new DataFrame with 30-minute intervals
date_range = pd.date_range(start=start_time, end=end_time, freq='30T')
df_result = pd.DataFrame({'date': date_range})

# c) Merge with the larger DataFrame ('main') on the 'date' column
df_result = pd.merge(df_result, df_main[['date', 'tair']], on='date', how='left')
df_result.rename(columns={'tair': 'main'}, inplace=True)

# d): Merge with the smaller DataFrame ('sat') on the 'date' column
df_result = pd.merge(df_result, df_sat[['date', 'tair']], on='date', how='left')
df_result.rename(columns={'tair': 'sat'}, inplace=True)

both_tair = df_result; del df_result

# - - - - - - - -
# same but for rh

# aa): Create a new DataFrame with 30-minute intervals
df_result = pd.DataFrame({'date': date_range})
del date_range, start_time, end_time

# bb) Merge with the larger DataFrame ('main') on the 'date' column
df_result = pd.merge(df_result, df_main[['date', 'rh']], on='date', how='left')
df_result.rename(columns={'rh': 'main'}, inplace=True)

# cc): Merge with the smaller DataFrame ('sat') on the 'date' column
df_result = pd.merge(df_result, df_sat[['date', 'rh']], on='date', how='left')
df_result.rename(columns={'rh': 'sat'}, inplace=True)

both_rh = df_result; del df_result




#%% 3) plot

#%%% 3.1) tair

# Plot both time series on the same axes
plt.figure(figsize=(15, 9)) # controls figures size, duh
plt.plot(both_tair['date'], both_tair['main'], color='darkgreen', linewidth=2, label='Main AWS')
plt.plot(both_tair['date'], both_tair['sat'], color='brown', linewidth=1, label='Satellite AWS')

# Add labels and legend
plt.xlabel('Date',fontsize = 14,weight='bold')
plt.ylabel('Air Temperature (°C)',fontsize = 14,weight='bold')  # You can adjust the y-axis label accordingly
plt.legend(fontsize = 14)

# specify output folder into which the figs will be saved
output_folder = mp + 'figures/2. SatAWS_2023/'

# Save the plot in high resolution with specified filename and path
output_filename = os.path.join(output_folder, 'both_tair.png')
plt.savefig(output_filename, dpi=300)

#%%% 3.2) rh
# Plot both time series on the same axes
plt.figure(figsize=(15, 9)) # controls figures size, duh
plt.plot(both_rh['date'], both_rh['main'], color='darkblue', linewidth=2, label='Main AWS')
plt.plot(both_rh['date'], both_rh['sat'], color='pink', linewidth=1, label='Satellite AWS')

# Add labels and legend
plt.xlabel('Date',fontsize = 14,weight='bold')
plt.ylabel('Relative Humidity (%)',fontsize = 14,weight='bold')  # You can adjust the y-axis label accordingly
plt.legend(fontsize = 14)

# Save the plot in high resolution with specified filename and path
output_filename = os.path.join(output_folder, 'both_rh.png')
plt.savefig(output_filename, dpi=300)








