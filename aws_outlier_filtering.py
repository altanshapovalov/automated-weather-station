# a_jas2023 (jas means july, aug, sept)

# Purpose: import AWS data for the the 2023 summer, filter outliers, and make plots
# Created on Nov 15, 2023 by Maxim Altan-Lu Shapovalov


#%% 1) Import

print("\014") # clear console
# clear variable explorer w/o user confirmation
%reset -f


#%%% 1.1) import libraries
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import os


#%%% 1.2) Load csv data
# a) establish "Max's Path"
mp = '/Users/maxims/Library/CloudStorage/OneDrive-UniversityOfOregon/Lab/python/aws/'
# b) create path to csv file
csv_path = mp + 'input/a_jas2023/hayden_jas2023.csv'
# c) read the csv file using pandas
jas23 = pd.read_csv(csv_path)
# d) clean up
del csv_path



#%% 2) Data Manipulation/Organization

#%%% 2.1) Make sure date is DateTime
# conditional statement that checks if date is/isn't in datetime format
if jas23['date'].dtype == 'datetime64[ns]':
    print("The 'date' is already in datetime format.")
else:
    print("Converting 'date' to datetime format.")
    jas23['date'] = pd.to_datetime(jas23['date'], format='%m/%d/%y %H:%M')
# Verify the changes
print("Data type of the 'date' after conversion:", jas23['date'].dtype)


#%%% 2.2) test plot
# get column names
cols = jas23.columns
# establish what you want to plot
x = jas23['date'] # nuestro tiempo
y = jas23['swd']

plt.figure(figsize=(10, 6)) # controls figures size, duh
plt.plot(x, y) # plot

#%%% 2.3) apply outlier filter to Gust Speed

# Calculate Z-scores for the 'gspd' column
z_scores = stats.zscore(jas23['gspd'])

# Define a threshold for outlier detection (adjust as needed)
z_threshold = 4

# Create a new DataFrame with the 'date_column' and 'z_scores' columns
z_scores_df = pd.DataFrame({'date': jas23['date'], 'z_scores': z_scores})
# Identify rows where the absolute Z-score is greater than the threshold
outlier_rows = z_scores_df[abs(z_scores_df['z_scores']) >= z_threshold]

# extract just gspd to not ruin the original dataset
gspd = jas23[['gspd']]

# Loop through each row in outlier_rows
for idx in outlier_rows.index:
    gspd.at[idx, 'gspd'] = np.nan
    
# can ensure that the nans were correctly placed; now, patch via linear interp
gspd['gspd'] = gspd['gspd'].interpolate(method='linear')

# plot to test one more time if it looks good (w/o outliers)
yy = gspd['gspd']; plt.plot(x,yy)


#%%% 2.4) apply outlier filter to Solar Radiation

# Calculate Z-scores for the 'swd' column
z_scores = stats.zscore(jas23['swd'])

# Define a threshold for outlier detection (adjust as needed)
z_threshold = 2.4

# Create a new DataFrame with the 'date_column' and 'z_scores' columns
z_scores_df = pd.DataFrame({'date': jas23['date'], 'z_scores': z_scores})
# Identify rows where the absolute Z-score is greater than the threshold
outlier_rows = z_scores_df[abs(z_scores_df['z_scores']) >= z_threshold]

# extract just gspd to not ruin the original dataset
swd = jas23[['swd']]

# Loop through each row in outlier_rows
for idx in outlier_rows.index:
    swd.at[idx, 'swd'] = np.nan
    
# can ensure that the nans were correctly placed; now, patch via linear interp
swd['swd'] = swd['swd'].interpolate(method='linear')

# plot to test one more time if it looks good (w/o outliers)
yy = swd['swd']; plt.figure(figsize=(10, 6)); plt.plot(x,yy)

#%%% 2.5) update jas23 vars that were filtered
jas23['gspd'] = gspd['gspd']; jas23['swd'] = swd['swd']
# run 2.2 to check if it got replaced properly





#%% 3) Plot and export!

# specify output folder into which the figs will be saved
output_folder = mp + 'figures/1. jas23_vars4permit/'

# Variables to plot
variables_to_plot = ['pressure', 'swd', 'tair', 'rh', 'wspd', 'gspd', 'precip']
x = jas23['date'] # tiempo

# Corresponding y-axis labels and colors
ylabel_mapping = {
    'pressure': 'Pressure (mbar)',
    'swd': 'Incoming Shortwave Radiation (W/m^2)',
    'tair': 'Temperature (°C)',
    'rh': 'Relative Humidity (%)',
    'wspd': 'Wind Speed (m/s)',
    'gspd': 'Gust Speed (m/s)',
    'precip': 'Precipitation (mm)'
}

# specify the colors as you please
color_mapping = {
    'pressure': 'purple',
    'swd': 'darkred',
    'tair': 'darkgreen',
    'rh': 'lightblue',
    'wspd': 'black',
    'gspd': 'gray',
    'precip': 'darkblue'
}

# Create individual plots
for variable in variables_to_plot:
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(x, jas23[variable], color=color_mapping[variable])
    plt.xlabel('Date', weight = 'bold')
    plt.ylabel(ylabel_mapping[variable], weight = 'bold')
    # plt.title(f'Plot for {variable}')
    # plt.grid(True)
    # plt.show()
    
    # Save the plot in high resolution with specified filename and path
    output_filename = os.path.join(output_folder, f'{variable}_Hayden.png')
    plt.savefig(output_filename, dpi=300)








