# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import plotly.express as px
from pandas_datareader import DataReader as pdr
from pages.formatting import smallfig


files = {
    "Earnings to price ratio": "Portfolios_Formed_on_E-P",
    "Variance": "Portfolios_Formed_on_VAR",
    "Accruals": "Portfolios_Formed_on_AC",
    "Residual variance": "Portfolios_Formed_on_RESVAR",
    "Net equity issuance": "Portfolios_Formed_on_NI",
    "Beta": "Portfolios_Formed_on_BETA",
    "Cash flow to price": "Portfolios_Formed_on_CF-P",
    "Market equity": "Portfolios_Formed_on_ME",
    "Book to market ratio": "Portfolios_Formed_on_BE-ME",
    "Dividend to price ratio": "Portfolios_Formed_on_D-P",
    "Investment rate": "Portfolios_Formed_on_INV",
    "Momentum": "10_Portfolios_Prior_12_2",
    "Short term reversal": "10_Portfolios_Prior_1_0",
    "Long term reversal": "10_Portfolios_Prior_60_13",
}

keys = np.sort(list(files.keys()))

quintiles = ["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]

CHAR = None
DATA = None

def figtbl(key, dates):

    global CHAR, DATA

    if key != CHAR:
        f = files[key]

        # annual value-weighted returns
        d = pdr(f, "famafrench", start=1926)[2] / 100

        # combine deciles for momentum, short-term reversal, and long-term reversal
        if "Portfolios_Formed_on" not in f:
            cols = d.columns.to_list()
            d["Lo 20"] = d[cols[:2]].mean(axis=1)
            d["Qnt 2"] = d[cols[2:4]].mean(axis=1)
            d["Qnt 3"] = d[cols[4:6]].mean(axis=1)
            d["Qnt 4"] = d[cols[6:8]].mean(axis=1)
            d["Hi 20"] = d[cols[8:]].mean(axis=1)
        d = d[quintiles]
        d = d.reset_index()
        d["Date"] = d.Date.astype(str).astype(int)
        d = d.set_index("Date").dropna()
        CHAR = key
        DATA = d

    rets = DATA.copy()

    mindate = max(dates[0], rets.index[0])
    rets = rets.loc[mindate : dates[1]]

    accum = (1 + rets).cumprod()
    accum.loc[mindate - 1] = 1
    accum = accum.sort_index()

    rets = rets.stack().reset_index()
    rets.columns = ["Date", "Quintile", "Return"]

    accum = accum.stack().reset_index()
    accum.columns = ["Date", "Quintile", "Accumulation"]

    fig1 = px.line(accum, x="Date", y="Accumulation", color="Quintile")
    fig2 = px.line(accum, x="Date", y="Accumulation", color="Quintile", log_y=True)
    fig3 = px.box(rets, x="Quintile", y="Return", color="Quintile")

    string = "$%{y:,.2f}<extra></extra>"
    for fig in [fig1, fig2]:
        fig.update_traces(mode="lines", hovertemplate=string)
        fig.update_layout(hovermode="x unified")
        fig.layout.xaxis["title"] = "Date"

    fig1.layout.yaxis["title"] = "Compound Return"
    fig2.layout.yaxis["title"] = "Compound Return (Log Scale)"
    fig3.layout.xaxis["title"] = ""
    fig3.layout.yaxis["title"] = "Return"
    fig3.update_yaxes(tickformat=".0%")

    rets = rets.set_index(["Date", "Quintile"]).unstack("Quintile")
    data = rets.describe()["Return"].iloc[1:]
    data.index.name = "Statistic"
    data = data.reset_index()

    fig1.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return (
        smallfig(fig1, showlegend=True),
        smallfig(fig2, showlegend=True),
        smallfig(fig3),
        data,
    )
