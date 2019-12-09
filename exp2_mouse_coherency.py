# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:56:02 2019

@author: agleo
"""

import pandas as pd
path = r'C:\Users\agleo\iCloudDrive\Documents\Experiments\5025comparison\mouse_exp_data.csv'
df_exp = pd.read_csv(path, index_col = 0)


def SSRTIntegrationMethod(df):
    try:
        df1 = df.sort_values(by=['RT_exp'])
        df1 = df1.reset_index(drop=True)
        stop_trials = df1.loc[df1['vol'] == 1]
        stop_count = stop_trials['correct'].sum()
        stop_number = stop_trials['soa'].count()
        overall_prob = 1 - stop_count/stop_number 
        go_trials = df1.loc[df1['vol'] == 0]
        nrt = go_trials['RT_exp'].count()
        nthindex = int(round(nrt*overall_prob))
        nthrt = go_trials['RT_exp'].iloc[nthindex]
        meanssd = stop_trials['soa'].mean()
        if meanssd > 0:
            ssrt =  nthrt - meanssd
            return ssrt
        else:
            return float("nan")
    except:
        pass

coh_list = [0.1, 0.5, 0.8]


appended_data = []
for coherency in coh_list:
    df =  df_exp.loc[df_exp['coh'] == coherency]
    final = df.groupby(['UIN']).apply(SSRTIntegrationMethod)
    final = final.to_frame()
    ssrt_name = 'ssrt' + str(coherency)
    final = final.rename(columns={0:ssrt_name})
    appended_data.append(final)

appended_data = pd.concat(appended_data, axis=1)
appended_data.to_csv('exp2_mouse_coherency.csv')