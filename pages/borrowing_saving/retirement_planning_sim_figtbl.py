# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 07:37:56 2022

@author: kerry
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import largefig

numsims = 1000


def figtbl(
    name,
    n_clicks,
    initial_balance,
    years_saving,
    years_withdrawing,
    initial_deposit,
    deposit_growth_rate,
    withdrawal,
    mn,
    sd,
):

    M = years_saving  # number of years to save
    N = M + years_withdrawing   # total number of years
    B0 = initial_balance  # start with $100,000
    S1 = initial_deposit   # initial saving is $10,000 per year
    g = deposit_growth_rate / 100  # savings grow at 2% per year
    W = withdrawal
    mn = mn / 100
    sd = sd / 100

    S = S1 * (1 + g) ** np.arange(years_saving)
    W = W * np.ones(years_withdrawing)
    B0 = np.concatenate(([B0], np.zeros(N)))
    S = np.concatenate(([0], S, np.zeros(years_withdrawing)))
    W = np.concatenate((np.zeros(years_saving + 1), W))
    CF = B0 + S - W

    rets = np.random.normal(loc=mn, scale=sd, size=(N, numsims))
    rets = pd.DataFrame(rets)

    def fvs(rets):
        x = np.flip(np.cumprod(1 + np.flip(rets, axis=0), axis=0), axis=0)
        return np.concatenate((x, [1]))

    fvFactors = rets.apply(fvs)
    B = fvFactors.multiply(CF, axis=0).sum()
    B2 = (B / 1000000).round(1)

    trace = go.Box(x=B2, hovertemplate="%{x}", name="")
    fig1 = go.Figure(trace)
    fig1.layout.yaxis['title'] = ''
    fig1.layout.xaxis['title'] = 'Ending Balance'
    fig1.update_xaxes(ticksuffix="MM")


    grid = [i / 100 for i in range(1, 100)]
    pcts = B2.quantile(grid).to_numpy()
    trace = go.Scatter(
        x=grid,
        y=pcts,
        mode="lines",
        hovertemplate="%{x:.0%} Percentile=%{y:,.1f}MM<extra></extra>"
    )
    fig = go.Figure(trace)
    fig.update_xaxes(title="Percentile")
    fig.update_yaxes(title="Ending Balance")
    fig.update_layout(yaxis_tickformat=",.0f", yaxis_ticksuffix="MM")
    fig.update_layout(xaxis_tickformat=".0%")
    fig2 = fig

    tbl = B.describe(percentiles=[0.1,0.25,0.5,0.75,0.9]).iloc[1:]
    tbl = pd.DataFrame(tbl).reset_index()
    tbl.columns = [name + c for c in ['col1', 'col2']]

    def dollarString(x):
        y = f"${x:,.0f}"
        return y[1]+y[0]+y[2:] if y[1] == "-" else y

    tbl[name + 'col2'] = tbl[name + 'col2'].map(dollarString)

    return largefig(fig1), largefig(fig2), tbl.to_dict('records')
