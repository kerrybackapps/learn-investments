# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 17:21:32 2022

@author: kerry
"""

import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from pages.formatting import largefig
from pages.data.ff_annual import ff3_annual
from pages.data.ff_monthly import ff3 as ff
from pages.data.tbond10 import dgs3mo
from pandas_datareader import data as pdr
import yfinance as yf

# annual data from 1926
mprem = 100 * ff3_annual["Mkt-RF"].mean()
mprem = round(mprem, 2)

# 3-month rate

rf = dgs3mo.iloc[-1].item()
rf = round(rf, 2)

# monthly data for last 60 months
ff = ff.iloc[-60:]

def figtbl(ticker):

    ticker = ticker.upper()
    ret = yf.download(ticker, start="2017-01-01")
    ret = ret["Close"].resample("M").last()
    ret = ret.pct_change()
    ret.index = ret.index.to_period("M")
    ret.columns = ["ret"]
    df = ff.join(ret, how="left")
    df["ret"] -= df.RF
    df = df[["Mkt-RF", "ret"]].reset_index()
    df.columns = ["date", "mkt", "ret"]
    df["date"] = df.date.astype(str)

    fig = px.scatter(
        df,
        x="mkt",
        y="ret",
        trendline="ols",
        hover_data=dict(ret=False, mkt=False, date=False),
        hover_name="date",
    )
    fig.layout.xaxis["title"] = "Market Excess Return"
    fig.layout.yaxis["title"] = ticker.upper() + " Excess Return"
    fig.update_traces(
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")

    beta = sm.OLS(df.ret, sm.add_constant(df.mkt)).fit().params["mkt"]
    beta = round(beta, 2)
    indx = [
        "Beta",
        "Market Risk Premium",
        ticker + " Risk Premium",
        "Risk Free Rate",
        ticker + " Cost of Equity",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    tbl.loc["Beta"] = beta
    tbl.loc["Market Risk Premium"] = mprem
    tbl.loc[ticker + " Risk Premium"] = round(beta * mprem, 2)
    tbl.loc["Risk Free Rate"] = round(rf, 2)
    tbl.loc[ticker + " Cost of Equity"] = round(beta * mprem + rf, 2)
    tbl = tbl.reset_index().to_dict("records")

    return largefig(fig), tbl
