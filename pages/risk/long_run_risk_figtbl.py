# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 07:37:56 2022

@author: kerry
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import smallfig

numsims = 5000
grid = [i / 100 for i in range(1, 100)]


def data(name, mna, sda, mnb, sdb, T):
    rva = norm(loc=mna, scale=sda)
    rvb = norm(loc=mnb, scale=sdb)
    df = None
    qs = None
    for rv in [rva, rvb]:
        ret = pd.DataFrame(rv.rvs(T * numsims).reshape((T, numsims)))
        d = (1 + ret).prod()
        q = d.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
        qs = pd.concat((qs, q), axis=1)
        df = pd.concat((df, d.quantile(grid)), axis=1)
    df.columns = ["Return 1", "Return 2"]
    df["grid"] = grid
    qs.columns = ["Return 1", "Return 2"]
    qs = qs.loc[["mean", "std", "10%", "25%", "50%", "75%", "90%"]]
    qs.index.name = ""
    qs = qs.round(2).reset_index()
    qs.columns = [name+c for c in qs.columns]
    return df, qs


def figtbl(name, n_clicks, mna, sda, mnb, sdb, T):
    mna /= 100
    sda /= 100
    mnb /= 100
    sdb /= 100
    df, qs = data(name, mna, sda, mnb, sdb, T)
    string = "Return 1 Percentile=$%{y:.2f}<extra></extra>"
    trace1 = go.Scatter(
        x=df["grid"],
        y=df["Return 1"],
        mode="lines",
        hovertemplate=string,
        name="Return 1",
    )
    string = "Return 2 Percentile=$%{y:.2f}<extra></extra>"
    trace2 = go.Scatter(
        x=df["grid"],
        y=df["Return 2"],
        mode="lines",
        hovertemplate=string,
        name="Return 2",
    )
    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_xaxes(title="Percentile")
    fig.update_yaxes(title="Compound Return (from $1)")
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.2f")
    fig.update_layout(xaxis_tickformat=".0%")
    fig.update_layout(hovermode="x unified")
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig1 = fig

    fig = go.Figure()
    trace1 = go.Box(y=df["Return 1"], name="Return 1", hovertemplate="$%{y:.2f}")
    trace2 = go.Box(y=df["Return 2"], name="Return 2", hovertemplate="$%{y:.2f}")
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.2f")
    fig2 = fig

    return qs.to_dict("records"), smallfig(fig2), smallfig(fig1, showlegend=True)
