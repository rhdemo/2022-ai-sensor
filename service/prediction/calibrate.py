import pandas as pd
import config
import os
import numpy as np
import matplotlib.pylab as plt

plt.ion()

def calibrate(df, df_flat, plot_loc):
    p_list = config.perc_list
    low_p = config.low_p
    high_p = config.high_p
        
    if not os.path.exists(plot_loc):
        os.makedirs(plot_loc)

    uniq_dids = df['deviceuid'].unique()
    
    cals = {} #deviceuid -> feature name -> low, high

    for did in list(uniq_dids) + ['global']:
        if did == 'global':
            temp_df = df_flat.sort_values(by='timestamp')
        else:
            temp_df = df_flat[df_flat['deviceuid']==did].sort_values(by='timestamp')
        
        cals[did] = {}
        
        for k in temp_df.columns: #loop over each metric
            cals[did][k] = {}
            
            if k=='deviceuid' or k=='timestamp': #index columns
                continue 
            
            d = temp_df[k].copy()
            
            if d.dropna().shape[0] == 0: #don't have data
                cals[did][k]['low'] = cals[did][k]['high'] = None
                
            else: #have data                
                d = d.dropna()
    
                plt.figure()
                n,b,p = plt.hist(d, bins=10) #plot distribution of values
                plt.title(did)
                plt.xlabel(k)
                
                t = np.percentile(d, q=p_list)
                
                mapping = dict(zip(p_list, t))
                print(did, k, mapping)
                cals[did][k]['low'] = mapping[low_p]
                cals[did][k]['high'] = mapping[high_p]
    
                #plot percentiles on histogram
                for p in p_list:
                    plt.vlines(mapping[p], 0, n.max()*1.2, color='r', label=p)
                plt.savefig(f'{plot_loc}/{did}_{k}_hist.png')
                
                plt.figure()
                plt.plot(d.tolist(), 'p-')
                plt.xlabel('time')
                plt.ylabel(k)
                plt.title(did)

                plt.hlines(mapping[low_p], 0, d.shape[0], color='r')
                plt.hlines(mapping[high_p], 0, d.shape[0], color='r')    
                plt.savefig(f'{plot_loc}/{did}_{k}_ts.png')
    
    return cals
