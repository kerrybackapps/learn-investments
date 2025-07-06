# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 09:23:46 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig


def data(mn1, mn2, sd1, sd2, c):
    c = c / 100
    mns = [mn1, mn2]
    sds = [sd1, sd2]
    grid = np.linspace(-1, 2, 151)
    ports = [np.array([w, 1 - w]) for w in grid]
    means = [p.T @ np.array(mns) for p in ports]
    df = pd.DataFrame(means)
    df.columns = ["mean"]
    cov = np.array(
        [[sds[0] ** 2, sds[0] * sds[1] * c], [sds[0] * sds[1] * c, sds[1] ** 2]]
    ).reshape(2, 2)
    df["stdev"] = [np.sqrt(p.T @ cov @ p) for p in ports]
    df["wt1"] = grid
    df["wt2"] = 1 - df.wt1
    for col in ["mean", "stdev"]:
        df[col] = df[col] / 100
    return df


def figtbl(mn1, mn2, sd1, sd2, c):
    df = data(mn1, mn2, sd1, sd2, c)
    trace1 = go.Scatter(
        x=df["stdev"],
        y=df["mean"],
        mode="lines",
        text=df["wt1"],
        customdata=df["wt2"],
        hovertemplate="asset 1: %{text:.1%}<br>asset 2: %{customdata:.1%}<extra></extra>",
    )
    df = df[df.wt1.isin([0, 1])]
    df["text"] = np.where(df.wt1 == 1, "asset 1", "asset 2")
    trace2 = go.Scatter(
        x=df["stdev"],
        y=df["mean"],
        mode="markers",
        text=df["text"],
        hovertemplate="%{text}<extra></extra>",
        marker=dict(size=15),
    )
    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    fig.update_xaxes(range=[0, 1.25 * df["stdev"].max()])
    fig.update_yaxes(range=[0, 1.25 * df["mean"].max()])
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    return largefig(fig)
