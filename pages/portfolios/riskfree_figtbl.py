# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 09:23:46 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig, blue, yellow, red


def data(mn, sd, s, b):
    grid = np.linspace(0, 2, 201)
    mns = [(s + w * (mn - s) if w <= 1 else b + w * (mn - b)) for w in grid]
    sds = [w * sd for w in grid]
    return grid, mns, sds


def figtbl(mn, sd, s, extra):
    mn /= 100
    sd /= 100
    b = s+extra
    s /= 100
    b /= 100
    grid, mns, sds = data(mn, sd, s, b)
    string = "wealth in risky asset = %{text:.1%}<extra></extra>"
    trace1 = go.Scatter(
        x=sds, y=mns, mode="lines", text=grid, hovertemplate=string, line=dict(color=blue)
    )

    x = np.linspace(0, sd, 51)
    y = b + (mn-b)*x / sd
    string = "infeasible saving at borrowing rate<extra></extra>"
    trace1a = go.Scatter(
        x=x, y=y, mode="lines", hovertemplate=string, line=dict(color=yellow, dash="dot")
    )

    x = np.linspace(sd, 2*sd, 51)
    y = mn + (mn - s) * (x-sd) / sd
    string = "infeasible borrowing at saving rate<extra></extra>"
    trace1b = go.Scatter(
        x=x, y=y, mode="lines", hovertemplate=string, line=dict(color=yellow, dash="dot")
    )

    string = "wealth in risky asset = 100%<extra></extra>"
    trace2 = go.Scatter(
        x=[sd], y=[mn], mode="markers", hovertemplate=string, marker=dict(size=15, color=red)
    )
    fig = go.Figure()
    fig.add_trace(trace1a)
    fig.add_trace(trace1b)
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    return largefig(fig)
