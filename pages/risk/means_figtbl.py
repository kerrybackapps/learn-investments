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

numsims = 5000

def figtbl(name, n_clicks, mn, sd, T):

    mn /= 100
    sd /= 100

    rv = norm(loc=mn, scale=sd)
    ret = pd.DataFrame(rv.rvs(T * 2 * numsims).reshape((T, 2 * numsims)))
    past = ret[ret.columns[:numsims]]
    futures =ret[ret.columns[numsims:]]
    futures_mean = futures.mean()
    futures_mean.index = range(numsims)

    arith = past.mean()
    geom = (1 + past).prod() ** (1 / T) - 1

    arith_mean_error = arith - futures_mean
    geom_mean_error = geom - futures_mean

    arith_forecast = (1+arith)**T
    geom_forecast = (1 + past).prod()
    futures = (1+futures).prod()
    futures.index = range(numsims)
    arith_error = arith_forecast - futures
    geom_error = geom_forecast - futures

    fig = go.Figure()
    trace1 = go.Box(y=arith_error, name='Arithmetic', hovertemplate="$%{y:.2f}<extra></extra>")
    trace2 = go.Box(y=geom_error, name='Geometric', hovertemplate="$%{y:.2f}<extra></extra>")
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_yaxes(tickformat=".1%")
    fig.layout.yaxis['title'] = ''
    fig.update_layout(
        title={
            "text": "Error for Compound Return",
            "y": 0.96,
            "x": 0.50,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )
    fig1 = fig

    df = pd.concat((arith_error, geom_error), axis=1)
    df.columns = ['Arithmetic', 'Geometric']
    tbl = df.describe().iloc[1:]
    tbl.loc['RMSE'] = np.sqrt((df**2).mean())
    tbl.loc['Mean AD'] = (df.abs()).mean()
    tbl.loc['Med AD'] = (df.abs()).median()
    for col in tbl.columns:
        tbl[col] = tbl[col].map(lambda x: f"{x:.1%}")
    tbl = tbl.reset_index()
    tbl.columns = [name + c for c in [''] + df.columns.to_list()]
    tbl1 = tbl

    fig = go.Figure()
    trace1 = go.Box(y=arith_mean_error, name='Arithmetic', hovertemplate="%{y:.1%}<extra></extra>")
    trace2 = go.Box(y=geom_mean_error, name='Geometric', hovertemplate="%{y:.1%}<extra></extra>")
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_yaxes(tickformat=".1%")
    fig.layout.yaxis['title'] = ''
    fig.update_layout(
        title={
            "text": "Error for Average Return",
            "y": 0.96,
            "x": 0.50,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )
    fig2 = fig

    df = pd.concat((arith_mean_error, geom_mean_error), axis=1)
    df.columns = ['Arithmetic', 'Geometric']
    tbl = df.describe().iloc[1:]
    tbl.loc['RMSE'] = np.sqrt((df ** 2).mean())
    tbl.loc['Mean AD'] = (df.abs()).mean()
    tbl.loc['Med AD'] = (df.abs()).median()
    for col in tbl.columns:
        tbl[col] = tbl[col].map(lambda x: f"{x:.2%}")
    tbl = tbl.reset_index()
    tbl.columns = [name + "2" + c for c in [''] + df.columns.to_list()]
    tbl2 = tbl

    return tbl1.to_dict('records'), smallfig(fig1), tbl2.to_dict('records'), smallfig(fig2)

