# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 21:40:45 2019

@author: agleo
"""

import pandas as pd

df = pd.read_csv("EXP1_KEY_EXPDATA.csv")
list(df)
#df = df.loc[df['coh'] == 0.8]

def SSRTIntegrationMethod_fixedSSD(df, ssd):
    try:
        go_trials = df.loc[df['vol'] == 0]
        go_trials = go_trials.sort_values(by=['key_resp_2.rt'])
        go_trials = go_trials.reset_index(drop=True)
        df1 = df.loc[df['soa'] == ssd]
        stop_trials = df1.loc[df1['vol'] == 1]
        stop_correct = stop_trials['key_resp_2.corr'].sum()
        nrt = go_trials['key_resp_2.rt'].count()
        stop_count = stop_trials['soa'].count()
        stop_accuracy = 1 - stop_correct/stop_count
        nthindex = int(round(nrt*stop_accuracy))
        nthrt = go_trials['key_resp_2.rt'].iloc[nthindex]
        ssrt =  nthrt - (ssd-0.5)
        return ssrt
    except:
        pass

ssd_list = [0.6,0.7, 0.8, 0.9, 1.0, 1.1]

appended_data = []
for ssd_value in ssd_list:
    final = df.groupby(['UIN']).apply(SSRTIntegrationMethod_fixedSSD, ssd = ssd_value)
    final = final.to_frame()
    ssrt_name = 'ssrt' + str(ssd_value)
    final = final.rename(columns={0:ssrt_name})
    appended_data.append(final)
    
    
appended_data = pd.concat(appended_data, axis=1)

appended_data['ssrt_mean'] = appended_data.mean(axis=1)

#appended_data.to_csv('exp1_key_ssrt_integ80percent.csv')