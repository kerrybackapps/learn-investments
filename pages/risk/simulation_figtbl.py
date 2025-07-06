# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 07:37:56 2022

@author: kerry
"""

import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import smallfig
import numpy as np


def figtbl(n_clicks, mn, sd, T):

    mn /= 100
    sd /= 100

    rv = norm(loc=mn, scale=sd)
    ret = pd.Series(rv.rvs(T), index=range(1,T+1))

    arith = ret.mean()
    geom = (1 + ret).prod() ** (1 / T) - 1

    ret.loc[0] = 0
    ret = ret.sort_index()
    ret = pd.DataFrame(ret).reset_index()
    ret.columns = ['date','ret']

    trace = go.Scatter(x=ret.date.iloc[1:], y=ret.ret.iloc[1:], mode="lines", hovertemplate="%{y:.1%}")
    minr = min(ret.ret.min(), -0.3)-0.02
    maxr = max(ret.ret.max(), 0.3)+0.02
    fig1 = go.Figure(trace)
    fig1.update_yaxes(tickformat=".0%", range=[minr, maxr])
    fig1.layout.xaxis['title'] = "Period"
    fig1.layout.yaxis["title"] = "Simulated Return"

    trace1 = go.Scatter(
        x=ret.date,
        y=(1+ret.ret).cumprod(),
        mode="lines",
        name="Simulated Accumulation",
        hovertemplate="%{y:.2f}"
    )
    trace2 = go.Scatter(
        x=ret.date,
        y=(1+arith)**np.arange(T+1),
        mode="lines",
        name="Compounded Arithmetic Avg",
        hovertemplate="%{y:.2f}"
    )
    trace3 = go.Scatter(
        x=ret.date,
        y=(1+geom)**np.arange(T+1),
        mode="lines",
        name="Compounded Geometric Avg",
        hovertemplate="%{y:.2f}"
    )

    fig2 = go.Figure()
    for trace in (trace1, trace2, trace3):
        fig2.add_trace(trace)
    fig2.update_layout(
        hovermode="x unified",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    fig2.layout.xaxis["title"] = "Period"
    fig2.update_yaxes(range=[0,max(4,(1+arith)**T+0.1)])

    string1 = f"{arith:.2%}"
    string2 = f"{geom:.2%}"
    string0 = f"{ret.ret.iloc[1:].std():.2%}"

    return smallfig(fig1), smallfig(fig2, showlegend=True), string0, string1, string2

