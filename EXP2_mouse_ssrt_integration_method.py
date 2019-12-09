# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:45:55 2019

@author: agleo


The integration method assumes that the finishing time of the stop process 
corresponds to the nth RT, 
with n equal to the number of RTs in the RT distribution 
multiplied by the overall p(respond|signal) 
(Logan, 1981); SSRT can then be estimated by subtracting the mean 
SSD from the nth RT 
(taken from Verbruggen 2013)

"""
import pandas as pd
path = r'C:\Users\agleo\iCloudDrive\Documents\Experiments\5025comparison\mouse_exp_data.csv'
df_exp = pd.read_csv(path, index_col = 0)

#4.850484265222223

#df = df_exp.loc[df_exp['UIN'] == 225008825]
def SSRTIntegrationMethod(df):
    df1 = df.sort_values(by=['RT_exp'])
    df1 = df1.reset_index(drop=True)
    stop_trials = df1.loc[df1['vol'] == 1]
    stop_count = stop_trials['correct'].sum()
    overall_prob = 1 - stop_count/144 
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


final = df_exp.groupby(['UIN']).apply(SSRTIntegrationMethod)

final.to_csv('ssrt_integration.csv')