import json
import os
import glob
import boto3

import numpy as np
import matplotlib.pylab as plt
import pandas as pd

def read_data_from_csv(out_loc):
    '''read formatted data - should be in persistent store/DB
    '''
    df = pd.read_csv(f'{out_loc}/data.csv')
    df_flat = pd.read_csv(f'{out_loc}/data_flat.csv')

    return df, df_flat
    
def write_json(cals, loc):
    json.dump(cals, open(loc, 'w'))

def read_json(loc):
    return json.load(open(loc, 'r'))

def check_create(out_loc):
    if not os.path.exists(out_loc):
        os.makedirs(out_loc)
