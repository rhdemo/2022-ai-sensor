import matplotlib.pylab as plt
import pandas as pd

plt.ion()

def plot_data(df, df_flat):
    features = ['light', 'temperature', 'accelerometer'] #should be in config

    uniq_dids = df['deviceuid'].unique()
    
    for did in uniq_dids:
        plt.figure(figsize=(15,15))
        fig, ax = plt.subplots(nrows=1, ncols=len(features))

        for idx, m in enumerate(features):
            #plt.subplot(f'{len(features)}1{idx+1}')

            if m=='accelerometer':
                filtered = df[(df['deviceuid']==did) & (df['metric']==m) & (df['key']=='mag')]['val']
            else:
                filtered = df[(df['deviceuid']==did) & (df['metric']==m)]['val']

            if filtered.shape[0] > 0:
                ax[idx].plot(filtered)
                ax[idx].set_title(m)

        temp_df = df_flat[(df_flat['deviceuid']==did)].dropna().sort_values(by='timestamp')        
        if temp_df.shape[0] > 0:
            _ = plt.figure()
            plt.plot(temp_df['temperature_value'], temp_df['light_value'], 'p')
            plt.xlabel('temperature')
            plt.ylabel('light')

            _ = plt.figure()
            plt.plot(temp_df['temperature_value'], temp_df['accelerometer_mag'], 'p')
            plt.xlabel('temperature')
            plt.ylabel('acceleration magnitude')

            _ = plt.figure()
            plt.plot(temp_df['light_value'], temp_df['accelerometer_mag'], 'p')
            plt.xlabel('light')
            plt.ylabel('acceleration magnitude')
