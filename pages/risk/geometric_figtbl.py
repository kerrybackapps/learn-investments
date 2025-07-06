# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 07:37:56 2022

@author: kerry
"""

import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig
import numpy as np
from pages.data.ff_annual import ff3_annual as df
import yfinance as yf

mkt = df["Mkt-RF"] + df.RF
mkt.index = mkt.index.astype(str).astype(int)
mkt.name = "mkt"
mkt.index.name = "date"

ANNUAL = None
TICKER = None

def figtbl(dates, radio, ticker=None):

    dates = [int(x) for x in dates]

    global ANNUAL, TICKER

    if radio == "Ticker":

        tick = ticker.upper()

        if tick != TICKER:

            close = yf.download(tick, start="1970-01-01")
            close = close.resample("YE").last()["Close"].squeeze()
            close.index = close.index.to_period("Y").astype(str).astype(int)
            annual = close.pct_change().dropna()
            annual.name = "ret"
            annual.index.name = "date"
            TICKER, ANNUAL = tick, annual

        ret = ANNUAL[(ANNUAL.index >= dates[0]) & (ANNUAL.index <= dates[1])].copy()

    else:

        tick = "Mkt"
        ret = mkt[(mkt.index >= dates[0]) & (mkt.index <= dates[1])].copy()

    T = ret.shape[0]
    dmin = ret.index.min()

    arith = ret.mean()
    geom = (1 + ret).prod() ** (1 / T) - 1

    ret.loc[dmin - 1] = 0
    ret = ret.sort_index()
   
    trace = go.Scatter(x=ret.index.to_list()[1:], y=ret.iloc[1:], mode="lines", hovertemplate="%{x}<br>%{y:.1%}")
    fig1 = go.Figure(trace)
    fig1.update_yaxes(tickformat=".0%")
    fig1.layout.yaxis["title"] = f"{tick} Return"

    trace1 = go.Scatter(
        x=ret.index.to_list(),
        y=(1+ret).cumprod(),
        mode="lines",
        name="Actual Accumulation",
        hovertemplate="%{y:.2f}"
    )
    trace2 = go.Scatter(
        x=ret.index.to_list(),
        y=(1+arith)**np.arange(T+1),
        mode="lines",
        name="Compounded Arithmetic Avg",
        hovertemplate="%{y:.2f}"
    )
    trace3 = go.Scatter(
        x=ret.index.to_list(),
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


    string1 = f"{arith:.2%}"
    string2 = f"{geom:.2%}"
    string0 = f"{ret.iloc[1:].std():.2%}"

    return largefig(fig1), largefig(fig2, showlegend=True), string0, string1, string2

