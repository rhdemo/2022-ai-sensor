import json
import os
import glob
import boto3

import numpy as np
import matplotlib.pylab as plt
import pandas as pd

def read_data(bucket_name='summit-demo', prefix='ai-sensor-v3/device', n_data_max=None):
    '''use s3 client to download data from bucket
    '''
    client = boto3.client('s3',
                     aws_access_key_id = os.getenv('aws_access_key'),
                     aws_secret_access_key = os.getenv('aws_secret_key'),
                     )

    bucket_list = client.list_buckets()

    object_list = client.list_objects_v2(Bucket = bucket_name)['Contents']

    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    key_list = []
    for p in pages:
        for o in p['Contents']:
            key_list.append(o['Key'])

    print(f'Example keys:')
    for k in key_list[0:10]: print('\t', k)

    n_keys = len(key_list)
    data_list = []
    for idx, k in enumerate(key_list):
        if n_data_max is not None and idx >= n_data_max: break
            
        if idx % 100 == 0:
            print(f'Fetching key number {idx+1} of {n_keys}')
            
        data = client.get_object(Bucket = bucket_name, Key = k)['Body'].readlines()
        data_list.append(data)
    
    return data_list

def create_df(data_list, out_loc, save_data=False):
    '''create dataframes from raw data
    '''

    data = [json.loads(d[0].decode('utf-8')) for d in data_list] #decode dictionaries
    if save_data:
        json.dump(data, open(f'{out_loc}/data.json', 'w'))

    uniq_dids = np.unique([d['deviceuid'] for d in data]) #unique device uids
    uniq_features = np.unique(np.concatenate([list(d['data']['features'].keys()) for d in data])) #unique feature names

    fields = {} #get mapping from field name -> dict key e.g. accelerometer -> ['x', 'y', 'z']
    for d in data:
        for f in d['data']['features']:
            if f not in fields:
                fields[f] = []
            for k in d['data']['features'][f].keys():
                if k not in fields[f]:
                    fields[f].append(k)

    #one row per device, timestamp, and metric
    data_df = {'deviceuid': [], 'timestamp': [], 'metric': [], 'key': [], 'val': []}
    for d in data: #(ts, uid)
        for m in d['data']['features']: #light, temp, accelerometer etc.
            if m=='accelerometer':
                data_df['deviceuid'].append(d['deviceuid'])
                data_df['timestamp'].append(d['time'])

                data_df['metric'].append(m)
                data_df['key'].append('mag')

                mag = np.sqrt(d['data']['features'][m]['x']**2 + d['data']['features'][m]['y']**2 + d['data']['features'][m]['z']**2)
                data_df['val'].append(mag)

            for v in d['data']['features'][m]: #1 val or 3 vals (acc) 

                data_df['deviceuid'].append(d['deviceuid'])
                data_df['timestamp'].append(d['time'])

                data_df['metric'].append(m)
                data_df['key'].append(v)
                data_df['val'].append(d['data']['features'][m][v])

    #one row per device, timestamp (metrics flattened into row)
    data_df_flat = {'deviceuid': [], 'timestamp': []}
    for f in fields:
        for k in fields[f]:
            data_df_flat[f'{f}_{k}'] = []

    for d in data:
        data_df_flat['deviceuid'].append(d['deviceuid'])
        data_df_flat['timestamp'].append(d['time'])

        for f in uniq_features:
            for k in fields[f]:
                colname = f'{f}_{k}'            
                try:
                    data_df_flat[colname].append(d['data']['features'][f][k])
                except:
                    data_df_flat[colname].append(np.nan)

    #create and save dataframes
    if not os.path.exists(out_loc):
        os.makedirs(out_loc)
    
    df = pd.DataFrame(data_df)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by=['deviceuid', 'timestamp', 'metric'], inplace=True)
    df.to_csv(f'{out_loc}/data.csv', index=False)

    df_flat = pd.DataFrame(data_df_flat)
    df_flat['timestamp'] = pd.to_datetime(df_flat['timestamp'])
    df_flat.sort_values(by=['deviceuid', 'timestamp'], inplace=True)
    df_flat['accelerometer_mag'] = df_flat[['accelerometer_x', 'accelerometer_y', 'accelerometer_z']].apply(lambda x: np.sqrt((x**2).sum()) if not x.isna().any() else np.nan, axis=1)

    df_flat.to_csv(f'{out_loc}/data_flat.csv', index=False)
    
    return df, df_flat, fields
