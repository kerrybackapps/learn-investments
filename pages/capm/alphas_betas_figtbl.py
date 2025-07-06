# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 17:21:32 2022

@author: kerry
"""

import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from pages.formatting import largefig
from pages.data.ff_monthly import ff3 as ff
import yfinance as yf



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

    result = sm.OLS(df.ret, sm.add_constant(df.mkt)).fit()
    alpha = round(100*100*result.params["const"], 2)
    beta = round(result.params["mkt"], 2)
    indx = [
        ticker + " Alpha (bps)",
        ticker + " Beta",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    tbl.index.name = "index"
    tbl.loc[ticker + " Alpha (bps)"] = alpha
    tbl.loc[ticker + " Beta"] = beta
    tbl = tbl.reset_index().to_dict("records")

    return largefig(fig), tbl
