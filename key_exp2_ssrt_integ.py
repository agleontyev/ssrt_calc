# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:44:11 2019

@author: agleo
"""

import pandas as pd
path = r'C:\Users\agleo\Documents\Programming projects\Recalculating SSRT PLOS\key_exp_summer_fall2018.csv'
df_exp = pd.read_csv(path, index_col = 0)

#4.850484265222223

#df = df_exp.loc[df_exp['UIN'] == 225008825]
def SSRTIntegrationMethod(df):
    df1 = df.sort_values(by=['key_resp_2.rt'])
    df1 = df1.reset_index(drop=True)
    stop_trials = df1.loc[df1['vol'] == 1]
    stop_count = stop_trials['key_resp_2.corr'].sum()
    overall_prob = 1 - stop_count/144 
    go_trials = df1.loc[df1['vol'] == 0]
    nrt = go_trials['key_resp_2.rt'].count()
    nthindex = int(round(nrt*overall_prob))
    nthrt = go_trials['key_resp_2.rt'].iloc[nthindex]
    meanssd = stop_trials['soa'].mean()
    if meanssd > 0:
        ssrt =  nthrt - meanssd
        return ssrt
    else:
        return float("nan")


final = df_exp.groupby(['UIN']).apply(SSRTIntegrationMethod)

final.to_csv('ssrt_integration_key.csv')

final = final.to_frame()
key_integ = pd.read_csv('ssrt_integration_key.csv')
exp2 = pd.read_csv('key_exp1.csv')
exp2.set_index('UIN', inplace=True)

exp2_final = pd.merge(exp2, final, left_index=True, right_index=True)

exp2_final.to_csv('exp2_key_integ_ssrt.csv')

