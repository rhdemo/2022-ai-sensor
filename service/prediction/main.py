import utils
import os

import config
from ingest import read_data, create_df
from calibrate import calibrate

import pickle


#if data doesn't exist
if not os.path.exists(config.fields_loc):
    data_list = read_data(bucket_name=config.bucket_name,
                          prefix=config.prefix,
                          n_data_max=config.n_data_max)

    df, df_flat, fields = create_df(data_list, config.df_out_loc)
    utils.write_json(fields, config.fields_loc)
else:
    #if data exists
    df, df_flat = utils.read_data_from_csv(config.df_out_loc)

    cals = calibrate(df, df_flat, config.plot_loc)

    utils.write_json(cals, config.cals_loc)

def run():
    pass