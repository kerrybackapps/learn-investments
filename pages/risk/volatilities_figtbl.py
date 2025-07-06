# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages.data.ff_daily import ff3_daily as ffd
from pages.formatting import largefig
from pandas_datareader import data as pdr
import yfinance as yf

mktd = ffd["Mkt-RF"] + ffd.RF
mktd = pd.DataFrame(mktd).reset_index()
mktd.columns = ['date', 'ret']
mktd['month'] = mktd.date.dt.to_period('M').astype(str)
mktm = pd.DataFrame(mktd.groupby('month').ret.std())
mktm.columns = ['vol']
mktm['ret'] = mktd.groupby('month').ret.apply(lambda x: (1+x).prod()-1)
mktm['vol_lag'] = mktm.vol.shift()
mktm = mktm.reset_index()

MONTHLY = None
TICKER = None

def figtbl(dates, radio, ticker=None):

    dates = [str(x) for x in dates]

    global MONTHLY, TICKER

    if radio == "Ticker":

        tick = ticker.upper()

        if tick != TICKER:

            close = yf.download(tick, start="1970-01-01")["Close"]
            daily = close.pct_change().dropna()
            daily = pd.DataFrame(daily).reset_index()
            daily.columns = ['date', 'ret']
            daily['month'] = daily.date.dt.to_period('M').astype(str)
            monthly = pd.DataFrame(daily.groupby('month').ret.std())
            monthly.columns = ['vol']
            monthly['ret'] = daily.groupby('month').ret.apply(lambda x: (1+x).prod() - 1)
            monthly['vol_lag'] = monthly.vol.shift()
            monthly = monthly.reset_index()

            TICKER, MONTHLY = ticker, monthly

        m = MONTHLY[(MONTHLY.month >= dates[0]) & (MONTHLY.month <= dates[1])]

    else:

        tick = "Mkt"
        m = mktm[(mktm.month >= dates[0]) & (mktm.month <= dates[1])]

    trace = go.Scatter(x=m.month, y=m.vol, mode="lines", hovertemplate="%{x}<br>%{y:.1%}<extra></extra>")
    fig1 = go.Figure(trace)
    fig1.update_yaxes(tickformat=".0%")
    fig1.layout.yaxis["title"] = f"{tick} Volatility"

    fig = px.scatter(
        m,
        x="vol_lag",
        y="vol",
        trendline="ols",
        hover_data=dict(ret=False, vol=False, month=False, vol_lag=False),
        hover_name="month",
    )
    fig.layout.xaxis["title"] = f"Lagged {tick} Volatility"
    fig.layout.yaxis["title"] = f"{tick} Volatility"
    fig.update_traces(
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    fig2 = fig

    fig = px.scatter(
        m,
        x="vol_lag",
        y="ret",
        trendline="ols",
        hover_data=dict(ret=False, vol=False, month=False, vol_lag=False),
        hover_name="month",
    )
    fig.layout.xaxis["title"] = f"Lagged {tick} Volatility"
    fig.layout.yaxis["title"] = f"Monthly {tick} Return"
    fig.update_traces(
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    fig3 = fig

    fig = px.scatter(
        m,
        x="vol",
        y="ret",
        trendline="ols",
        hover_data=dict(ret=False, vol=False, month=False, vol_lag=False),
        hover_name="month",
    )
    fig.layout.xaxis["title"] = f"{tick} Volatility"
    fig.layout.yaxis["title"] = f"Monthly {tick} Return"
    fig.update_traces(
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    fig4 = fig


    return (
        largefig(fig1),
        largefig(fig2),
        largefig(fig3),
        largefig(fig4)
    )

