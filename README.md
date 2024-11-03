**READ FIRST:** brief description of data files and scripts in this repository; 3 & 4 are the actual scipts, while the rest are data used in those scripts.

**1. SatAWS_tair_2023.xlsx** – data used in “4. b_sat_aws_tair.py” 

**2. SatAWS_tair_2023_withNames.xlsx** – data used in “4. b_sat_aws_tair.py” (but also has more details about each column) 

**3. aws_outlier_filtering.py** – import weather station data, filter any unnatural outliers for unique attributes, and generate figures. 1) Import libraries [pandas, scipy(stats), matplotlib.pyplot, numpy, os], 2) read in .csv file, 3) double check time formatting, 4) create initial plot for visual inspection, 5) apply thresholds to data using z-score values, 6) patch any existing gaps, and 7) export final plots. 

**4. b_sat_aws_tair.py** – similar to “3. aws_outlier_filtering.py” but instead of loading weather station data, load, correct, and export temperature data from a satellite station measuring temperature. This script also contains a section in which I merge two temperature datasets with different time intervals into one. 

**5. hayden_jas2023.csv** – data used in “3. aws_outlier_filtering.py” 

**6. hayden_jas2023_withNames.csv** – data used in “3. aws_outlier_filtering.py” (but also has more details about each column)
