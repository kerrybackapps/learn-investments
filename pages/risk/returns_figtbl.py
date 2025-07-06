# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from pages.formatting import smallfig
from pages.data.ff_annual import ff3_annual as df

mkt = (df["Mkt-RF"] + df.RF).squeeze()
mkt.index.name = "Year"
mkt.index = mkt.index.astype(str)


def figtbl(dates, radio="Market", ticker=None):
    dates = [str(x) + "-01-01" for x in dates]
    if radio == "Ticker":
        ticker = ticker.upper()
        rets = yf.download(ticker, start='1970-01-01')["Close"]
        rets = rets.resample('YE').last().squeeze()
        rets.index = rets.index.to_period("Y").astype(str)
        rets = rets.pct_change().dropna()
    else:
        rets = mkt
        ticker = "Market"

    mindate = max(dates[0], rets.index[0])
    rets = rets.loc[mindate : dates[1]]

    accum = (1 + rets).cumprod()
    # accum.loc[mindate - 1] = 1
    accum = accum.sort_index()

    rets = pd.DataFrame(rets).reset_index()
    rets.columns = ["Year", "Return"]

    accum = pd.DataFrame(accum).reset_index()
    accum.columns = ["Year", "Compound Return"]

    fig1 = px.line(accum, x="Year", y="Compound Return")
    fig2 = px.line(accum, x="Year", y="Compound Return", log_y=True)
    z = rets.copy()
    tick = ticker.upper() if radio == "Ticker" else "Mkt"
    z.columns = ["Year", tick]
    trace = go.Box(y=z[tick], text=z.Year, name=tick, hovertemplate="%{text}<br>%{y:.1%}<extra></extra>")
    fig3 = go.Figure(trace)
    fig3.update_yaxes(tickformat=".1%")

    fig4 = px.histogram(rets["Return"])
    fig5 = px.line(rets, x="Year", y="Return")

    string = "%{x}<br>$%{y:,.2f}<extra></extra>"
    for fig in [fig1, fig2]:
        fig.update_traces(mode="lines", hovertemplate=string)
        fig.layout.xaxis["title"] = "Year"
    fig1.layout.yaxis["title"] = ticker + " Accumulation (from $1)"
    fig2.layout.yaxis["title"] = ticker + " Accumulation (Log Scale)"

    fig3.layout.xaxis["title"] = None
    fig3.update_yaxes(title=None, tickformat=".0%")

    fig4.layout.xaxis["title"] = ticker + " Return"
    fig4.layout.yaxis["title"] = "Number of Years"
    fig4.update_xaxes(tickformat=".0%")

    fig5.layout.xaxis["title"] = "Year"
    fig5.update_layout(yaxis_tickformat=".0%")
    fig5.layout.yaxis["title"] = ticker + " Return"

    tbl = pd.DataFrame(rets["Return"].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).iloc[1:]).reset_index()
    tbl.columns = ["Statistic", "Return"]

    return (
        smallfig(fig1),
        smallfig(fig2),
        smallfig(fig3),
        smallfig(fig4),
        smallfig(fig5),
        tbl,
    )
