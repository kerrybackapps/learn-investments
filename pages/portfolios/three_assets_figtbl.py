# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 10:28:20 2022

@author: kerry
"""

import pandas as pd
import numpy as np
from scipy.stats import uniform
import plotly.graph_objects as go
from pages.formatting import largefig, red, green, orange, purple

def random_wts(num):
    w = uniform.rvs(0, 1, num)
    return w / w.sum()


ports = [random_wts(3) for i in range(3000)]
ports1 = [(0, x, 1 - x) for x in np.linspace(0, 1, 21)]
ports2 = [(x, 0, 1 - x) for x in np.linspace(0, 1, 21)]
ports3 = [(x, 1 - x, 0) for x in np.linspace(0, 1, 21)]
ports = ports + ports1 + ports2 + ports3

ports23 = ports1
ports13 = ports2
ports12 = ports3

def is_pos_def(x):
    if np.all(np.linalg.eigvals(x) > 0):
        return 'True'
    else:
        return 'False'

def data(mn1, mn2, mn3, sd1, sd2, sd3, c12, c13, c23):
    mns = pd.Series(np.array([mn1, mn2, mn3]), index=["stock1", "stock2", "stock3"])
    sds = np.array([sd1, sd2, sd3])
    C = np.diag([1.0, 1.0, 1.0])
    C[0, 1] = c12 / 100
    C[0, 2] = c13 / 100
    C[1, 0] = c12 / 100
    C[1, 2] = c23 / 100
    C[2, 0] = c13 / 100
    C[2, 1] = c23 / 100
    D = np.diag(sds / 100)
    C = D @ C @ D
    
    # Random investment opportunity set (3-asset)
    df = pd.DataFrame(
        dtype=float,
        index=range(len(ports)),
        columns=["mean", "stdev", "wt1", "wt2", "wt3"],
    )
    df["mean"] = [p @ mns / 100 for p in ports]
    df["stdev"] = [np.sqrt(p @ C @ p) for p in ports]
    df["wt1"] = [100 * p[0] for p in ports]
    df["wt2"] = [100 * p[1] for p in ports]
    df["wt3"] = [100 * p[2] for p in ports]
    df = df.sort_values(by="mean")
    
    
    # Dataframes of 2-asset portfolios
    df12 = pd.DataFrame(dtype=float,index=range(len(ports12)),\
                    columns=['mean','stdev','wt1','wt2','wt3'])
    df12['mean'] = [p @ mns/100 for p in ports12]
    df12['stdev'] = [np.sqrt(p @ C @ p) for p in ports12]
    df12['wt1'] = [100*p[0] for p in ports12]
    df12['wt2'] = [100*p[1] for p in ports12]
    df12['wt3'] = [100*p[2] for p in ports12]
    df12 = df12.sort_values(by='mean')

    df13 = pd.DataFrame(dtype=float,index=range(len(ports13)),\
                    columns=['mean','stdev','wt1','wt2','wt3'])
    df13['mean'] = [p @ mns/100 for p in ports13]
    df13['stdev'] = [np.sqrt(p @ C @ p) for p in ports13]
    df13['wt1'] = [100*p[0] for p in ports13]
    df13['wt2'] = [100*p[1] for p in ports13]
    df13['wt3'] = [100*p[2] for p in ports13]
    df13 = df13.sort_values(by='mean')

    df23 = pd.DataFrame(dtype=float,index=range(len(ports23)),\
                    columns=['mean','stdev','wt1','wt2','wt3'])
    df23['mean'] = [p @ mns/100 for p in ports23]
    df23['stdev'] = [np.sqrt(p @ C @ p) for p in ports23]
    df23['wt1'] = [100*p[0] for p in ports23]
    df23['wt2'] = [100*p[1] for p in ports23]
    df23['wt3'] = [100*p[2] for p in ports23]
    df23 = df23.sort_values(by='mean')   
    
    
    return df, mns / 100, sds / 100, C, df12, df13, df23


def figtbl(mn1, mn2, mn3, sd1, sd2, sd3, c12, c13, c23):
    df, mns, sds, C, df12, df13, df23 = data(mn1, mn2, mn3, sd1, sd2, sd3, c12, c13, c23)
    cd = np.empty(shape=(df.shape[0], 3, 1), dtype=float)
    cd[:, 0] = np.array(df.wt1).reshape(-1, 1)
    cd[:, 1] = np.array(df.wt2).reshape(-1, 1)
    cd[:, 2] = np.array(df.wt3).reshape(-1, 1)
    string = "asset 1: %{customdata[0]:.0f}%<br>"
    string += "asset 2: %{customdata[1]:.0f}%<br>"
    string += "asset 3: %{customdata[2]:.0f}%<br>"
    string += "<extra></extra>"
    trace1 = go.Scatter(
        x=df["stdev"], y=df["mean"], mode="markers", customdata=cd, hovertemplate=string
    )
    trace2 = go.Scatter(
        x=sds,
        y=mns,
        mode="markers",
        text=["asset 1", "asset 2", "asset 3"],
        hovertemplate="%{text}<extra></extra>",
        marker=dict(size=15, color="red"),
    )
    
    #--------------
    # 2-asset frontiers
    #--------------
    #12
    cd12 = np.empty(shape=(df12.shape[0],3,1), dtype=float)
    cd12[:,0] = np.array(df12.wt1).reshape(-1,1)
    cd12[:,1] = np.array(df12.wt2).reshape(-1,1)
    cd12[:,2] = np.array(df12.wt3).reshape(-1,1)
    string12 = 'asset 1: %{customdata[0]:.0f}%<br>'
    string12+= 'asset 2: %{customdata[1]:.0f}%<br>'
    string12+= 'asset 3: %{customdata[2]:.0f}%<br>'
    string12+= '<extra></extra>'
    trace12 = go.Scatter(x=df12['stdev'],y=df12['mean'],mode='lines',customdata=cd12,hovertemplate=string12, line=dict(color=red, width=5))

    #23
    cd23 = np.empty(shape=(df23.shape[0],3,1), dtype=float)
    cd23[:,0] = np.array(df23.wt1).reshape(-1,1)
    cd23[:,1] = np.array(df23.wt2).reshape(-1,1)
    cd23[:,2] = np.array(df23.wt3).reshape(-1,1)
    string23 = 'asset 1: %{customdata[0]:.0f}%<br>'
    string23+= 'asset 2: %{customdata[1]:.0f}%<br>'
    string23+= 'asset 3: %{customdata[2]:.0f}%<br>'
    string23+= '<extra></extra>'
    trace23 = go.Scatter(x=df23['stdev'],y=df23['mean'],mode='lines',customdata=cd23,hovertemplate=string23, line=dict(color=red, width=5))

    #13
    cd13 = np.empty(shape=(df13.shape[0],3,1), dtype=float)
    cd13[:,0] = np.array(df13.wt1).reshape(-1,1)
    cd13[:,1] = np.array(df13.wt2).reshape(-1,1)
    cd13[:,2] = np.array(df13.wt3).reshape(-1,1)
    string13 = 'asset 1: %{customdata[0]:.0f}%<br>'
    string13+= 'asset 2: %{customdata[1]:.0f}%<br>'
    string13+= 'asset 3: %{customdata[2]:.0f}%<br>'
    string13+= '<extra></extra>'
    trace13 = go.Scatter(x=df13['stdev'],y=df13['mean'],mode='lines',customdata=cd13,hovertemplate=string13, line=dict(color=red, width=5))

    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.add_trace(trace12)
    fig.add_trace(trace23)
    fig.add_trace(trace13)
    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    fig.update_xaxes(range=[0, 1.25 * np.max(sds)])
    fig.update_yaxes(range=[0, 1.25 * np.max(mns)])
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    return largefig(fig), is_pos_def(C)
