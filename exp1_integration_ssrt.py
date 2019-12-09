# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 20:28:52 2019

@author: agleo

In the integration method, the point at which the stop process finishes is 
estimated by integrating the RT distribution and finding the point at which 
the integral equals the probability of responding, 
p(respond|signal), for a specific delay. 
SSRT is then calculated by subtracting SSD from the finishing time.

"""
import os
os.chdir(r"C:\Users\agleo\Documents\Programming projects\Recalculating SSRT PLOS")

import pandas as pd

df = pd.read_csv("exp1_mouse_expdata.csv")
#df = df.loc[df['coh'] == 0.1]


def SSRTIntegrationMethod_fixedSSD(df, ssd):
    try:
        go_trials = df.loc[df['vol'] == 0]
        go_trials = go_trials.sort_values(by=['RT_exp'])
        go_trials = go_trials.reset_index(drop=True)
        df1 = df.loc[df['soa'] == ssd]
        stop_trials = df1.loc[df1['vol'] == 1]
        stop_correct = stop_trials['correct'].sum()
        nrt = go_trials['RT_exp'].count()
        stop_count = stop_trials['soa'].count()
        stop_accuracy = 1 - stop_correct/stop_count
        nthindex = int(round(nrt*stop_accuracy))
        nthrt = go_trials['RT_exp'].iloc[nthindex]
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

appended_data.to_csv('exp1_mouse_ssrt_integ.csv')