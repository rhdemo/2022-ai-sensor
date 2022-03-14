import os
import utils

#Data store
bucket_name = 'summit-demo'
prefix = 'ai-sensor-v3/device'
n_data_max = None

#CSV files
df_out_loc = './data'
utils.check_create(df_out_loc)

fields_loc = './fields.json'

#Calibration and plotting
plot_loc = './plots'
utils.check_create(plot_loc)

perc_list = [10, 25, 50, 75, 90]
low_p = 25
high_p = 75

cals_loc = './calibration.json'