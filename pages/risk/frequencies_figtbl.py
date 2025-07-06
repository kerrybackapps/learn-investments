# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
import plotly.graph_objects as go
from pages.data.ff_daily import ff3_daily as ffd
from pages.data.ff_monthly import ff3 as ffm
from pages.data.ff_annual import ff3_annual as ffa
from pages.formatting import largefig, smallfig
from pandas_datareader import data as pdr
import plotly.figure_factory as ff
import numpy as np
from scipy.stats import norm
import yfinance as yf


mktd = ffd["Mkt-RF"] + ffd.RF
mktd.index.name="date"
mktd = mktd[mktd.index>="1927"]

mktm = ffm["Mkt-RF"] + ffm.RF
mktm.index.name="date"
mktm = mktm[mktm.index>='1927']

mkta = ffa["Mkt-RF"] + ffa.RF
mkta.index.name="date"
mkta = mkta[mkta.index>='1927']

DAILY = None
MONTHLY = None
ANNUAL = None
TICKER = None

def figtbl(name, dates, radio, ticker=None):

    dates = [str(x) for x in dates]

    global DAILY, MONTHLY, ANNUAL, TICKER

    if (radio == "Ticker") and (ticker is not None):

        tick = ticker.upper()

        if tick != TICKER:

            close = yf.download(tick, start="1970-01-01")["Close"]

            daily = close.pct_change().dropna().squeeze()
            daily.name="ret"
            daily.index.name="date"

            monthly = close.resample('ME').last().pct_change().dropna().squeeze()
            monthly.name="ret"
            monthly.index.name="date"

            annual = close.resample('YE').last().pct_change().dropna().squeeze()
            annual.name="ret"
            annual.index.name="date"

            TICKER, DAILY, MONTHLY, ANNUAL = ticker, daily, monthly, annual

        d = DAILY[(DAILY.index >= dates[0]) & (DAILY.index <= dates[1])]
        m = MONTHLY[(MONTHLY.index >= dates[0]) & (MONTHLY.index <= dates[1])]
        a = ANNUAL[(ANNUAL.index >= dates[0]) & (ANNUAL.index <= dates[1])]

    else:

        tick = "Mkt"
        d = mktd[(mktd.index >= dates[0]) & (mktd.index <= dates[1])]
        m = mktm[(mktm.index >= dates[0]) & (mktm.index <= dates[1])]
        a = mkta[(mkta.index >= dates[0]) & (mkta.index <= dates[1])]

    trace1 = go.Box(y=d, text=d.index.to_list(), name=tick+" Daily", hovertemplate="%{text}<br>%{y:.1%}<extra></extra>")
    trace2 = go.Box(y=m, text=m.index.to_list(), name=tick+" Monthly", hovertemplate="%{text}<br>%{y:.1%}<extra></extra>")
    trace3 = go.Box(y=a, text=a.index.to_list(), name=tick+" Annual", hovertemplate="%{text}<br>%{y:.1%}<extra></extra>")
    fig = go.Figure()
    for trace in [trace1, trace2, trace3]:
        fig.add_trace(trace)
    fig.update_yaxes(tickformat=".0%")

    tbld = pd.DataFrame(d.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).iloc[1:])
    tblm = pd.DataFrame(m.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).iloc[1:])
    tbla = pd.DataFrame(a.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).iloc[1:])
    tbl = pd.concat((tbld, tblm, tbla), axis=1)
    tbl = tbl.reset_index()
    tbl.columns = [name + x for x in ['', 'Daily', 'Monthly', 'Annual']]

    trace1 = ff.create_distplot([d], group_labels=["actual"], show_rug=False, show_hist=False)
    mn = d.mean()
    sd = d.std()
    grid = np.linspace(mn - 3 * sd, mn + 3 * sd, 201)
    trace2 = go.Scatter(x=grid, y=norm.pdf(grid, loc=mn, scale=sd), mode="lines", name="normal")
    figd = go.Figure(trace1)
    figd.add_trace(trace2)

    trace1 = ff.create_distplot([m], group_labels=["actual"], show_rug=False, show_hist=False)
    figm = go.Figure(trace1)
    mn = mktm.mean()
    sd = mktm.std()
    grid = np.linspace(mn - 3 * sd, mn + 3 * sd, 201)
    trace2 = go.Scatter(x=grid, y=norm.pdf(grid, loc=mn, scale=sd), mode="lines", name="normal")
    figm.add_trace(trace2)

    trace1 = ff.create_distplot([a], group_labels=["actual"], show_rug=False, show_hist=False)
    figa = go.Figure(trace1)
    mn = mkta.mean()
    sd = mkta.std()
    grid = np.linspace(mn - 3 * sd, mn + 3 * sd, 201)
    trace2 = go.Scatter(x=grid, y=norm.pdf(grid, loc=mn, scale=sd), mode="lines", name="normal")
    figa.add_trace(trace2)

    for f in [figd, figm, figa]:
        f.update_xaxes(tickformat=".0%")
        f.update_yaxes(tickvals=[])
        string = "Daily" if f==figd else ("Monthly" if f==figm else "Annual")
        string = tick + " " + string
        f.update_layout(
            title={
                "text": string,
                "y": 0.96,
                "x": 0.2,
                "xanchor": "center",
                "yanchor": "bottom",
            }
        )
        f.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))



    return (
        tbl.to_dict('records'),
        largefig(fig),
        smallfig(figd, showlegend=True),
        smallfig(figm, showlegend=True),
        smallfig(figa, showlegend=True)
    )

