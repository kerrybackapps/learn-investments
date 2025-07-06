# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
import plotly.express as px
from pandas_datareader import data as pdr
from pages.formatting import smallfig
from pages.data.ff_annual import ff3_annual as df
import plotly.graph_objects as go
import yfinance as yf

mkt = df["Mkt-RF"] + df.RF
mkt.index.name = "Year"
mkt.index = [int(str(x)) for x in mkt.index]


def figtbl(numyears, radio="Market", ticker=None):
    numyears = numyears.split(" ")[0]
    numyears = int(numyears)
    if radio == "Ticker":
        rets = yf.download(ticker, start="1970-01-01")["Close"]
        rets = rets.resample("YE").last()
        rets = rets.pct_change().dropna().squeeze()
        rets.index = rets.index.to_period("Y").astype(str).astype(int)
        rets.name = "ret"
        rets.index.name = "date"
        numyears = min(numyears, len(rets.index))
    else:
        rets = mkt

    label = ticker.upper() if radio == "Ticker" else "Market"

    compound = rets.rolling(numyears).apply(lambda x: (1 + x).prod())
    bestyear = compound.idxmax()
    worstyear = compound.idxmin()

    compound = compound.dropna()
    compound = compound**(1/numyears) - 1
    compound = compound.reset_index()
    compound.columns = ["Date", "Geometric"]
    compound["StartDate"] = compound.Date-(numyears-1)

    best = rets.loc[(bestyear - numyears + 1) : bestyear]
    best = (1 + best).cumprod()
    best = pd.DataFrame(best).reset_index()
    best.columns = ["Date", "Compounded Return"]    
    best['StartDate'] = best.Date.iloc[0]

    worst = rets.loc[(worstyear - numyears + 1) : worstyear]
    worst = (1 + worst).cumprod()
    worst = pd.DataFrame(worst).reset_index()
    worst.columns = ["Date", "Compounded Return"]
    worst['StartDate'] = worst.Date.iloc[0]

    fig1 = px.line(compound, x="Date", y="Geometric", text="StartDate")
    fig2 = px.line(best, x="Date", y="Compounded Return", text="StartDate")
    fig3 = px.line(worst, x="Date", y="Compounded Return", text="StartDate")
    trace = go.Box(y=compound.Geometric, name="", hovertemplate="%{y:.1%}")
    fig4 = go.Figure(trace)

    fig1.layout.xaxis["title"] = ""
    fig1.layout.yaxis["title"] = str(numyears) + " Year " + label + " Geometric Average Return"


    fig2.layout.yaxis["title"] = label + " Accumulation from $1"
    fig2.update_layout(
        title={
            "text": "Best " + str(numyears) + " Year Period",
            "y": 0.96,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )
    fig2.layout.xaxis['title'] = ""

    fig3.layout.yaxis["title"] = label + " Accumulation from $1"
    fig3.update_layout(
        title={
            "text": "Worst " + str(numyears) + " Year Period",
            "y": 0.96,
            "x": 0.50,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )
    fig3.layout.xaxis['title'] = ""
    string = "%{text}-%{x}<br>$%{y:.2f}<extra></extra>"
    for fig in [fig2, fig3]:
        fig.update_yaxes(tickprefix="$")
        fig.update_traces(mode="lines", hovertemplate=string)

    string = "%{text}-%{x}<br>%{y:,.1%}<extra></extra>"
    for fig in [fig1]:
        fig.update_yaxes(tickformat="0%")
        fig.update_traces(mode="lines", hovertemplate=string)


    fig4.layout.yaxis["title"] = str(numyears) + " Year " + label + " Geometric Average Return"
    fig4.update_yaxes(tickformat=".1%")
    fig4.layout.xaxis["title"] = ""


    return smallfig(fig1), smallfig(fig2), smallfig(fig3), smallfig(fig4)
