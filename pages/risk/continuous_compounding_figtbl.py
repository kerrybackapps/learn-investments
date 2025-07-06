# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import yfinance as yf
from pages.formatting import smallfig
from pages.data.ff_annual import ff3_annual as df

mkt = df["Mkt-RF"] + df.RF
mkt.index = mkt.index.astype(str)
mkt.index.name = "date"
mkt.name = "ret"


ANNUAL = None
TICKER = None

def figtbl(name, dates, radio, ticker=None):

    dates = [str(x) for x in dates]

    global ANNUAL, TICKER

    if radio == "Ticker":

        tick = ticker.upper()

        if tick != TICKER:

            close = yf.download(tick, start="1970-01-01")["Close"]
            close = close.resample("YE").last().pct_change()
            close = close.dropna().squeeze()
            close.index = close.index.to_period("Y").astype(str)
            close.index.name = "date"
            close.name = "ret"
            TICKER, ANNUAL = tick, close

        df = ANNUAL[(ANNUAL.index >= dates[0]) & (ANNUAL.index <= dates[1])].copy()

    else:

        df = mkt[(mkt.index >= dates[0]) & (mkt.index <= dates[1])].copy()
        tick = "Mkt"

    df = pd.DataFrame(df).reset_index()
    df['log'] = np.log(1+df.ret)

    trace = go.Scatter(
        x=df.ret,
        y=df.log,
        text=df.date,
        mode="markers",
        hovertemplate="%{text}<br>Return=%{x:.2%}<br>CC Return=%{y:.2%}<extra></extra>"
    )
    fig1 = go.Figure(trace)
    # fig1.layout.xaxis['title'] = 'Return'
    # fig1.layout.yaxis['title'] = 'Continuously Compounded Return'
    fig1.update_xaxes(tickformat=".0%", title="Return")
    fig1.update_yaxes(tickformat=".0%", title=f"Continuously Compounded {tick} Return")

    fig2 = ff.create_distplot([df.ret, df.log], group_labels=["Return", "CC Return"], show_rug=False, show_hist=False)
    fig2.update_yaxes(tickvals=[])
    fig2.update_xaxes(tickformat=".0%", title="")
    fig2.update_traces(hovertemplate="<extra></extra>")
    fig2.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    tbl = df[['ret', 'log']].describe().iloc[1:]
    tbl = tbl.reset_index()
    tbl.columns = [name + x for x in ["", "Return", "CC Return"]]


    return (
        smallfig(fig1),
        smallfig(fig2, showlegend=True),
        tbl.to_dict('records')
    )
