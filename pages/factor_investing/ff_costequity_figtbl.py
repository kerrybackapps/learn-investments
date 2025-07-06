# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 17:21:32 2022

@author: kerry
"""


import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from pandas_datareader import DataReader as pdr
from pages.data.tbond10 import dgs3mo
import yfinance as yf

ff3 = F_F_Research_Data_Factors = pdr(
    "F-F_Research_Data_Factors", "famafrench", start=1926
)
ff5 = F_F_Research_Data_5_Factors_2x3 = pdr(
    "F-F_Research_Data_5_Factors_2x3", "famafrench", start=1964
)

# annual 3 factors from 1926
ff3 = ff3[1]
fprem = ff3[["Mkt-RF", "SMB", "HML"]].mean()

# add annual 5 factors from 1964
fprem = pd.concat((fprem, ff5[1][["RMW", "CMA"]].mean()))
fprem = fprem.round(2)
factors = fprem.index.to_list()

# monthly 5 factors for last 60 months
ff = ff5[0].iloc[-60:] / 100

rf = dgs3mo.iloc[-1].item()
rf = round(rf, 2)



def data(ticker):
    ticker = ticker.upper()
    ret = yf.download(ticker, start="2017-01-01")
    ret = ret["Close"].resample("M").last()
    ret = ret.pct_change()
    ret.index = ret.index.to_period("M")
    ret.columns = ["ret"]
    df = ff.join(ret, how="left")
    df["ret"] -= df.RF
    df = df[factors + ["ret"]].reset_index()
    df.columns = ["date"] + factors + ["ret"]
    df["date"] = df.date.astype(str)
    return df


def figtbl(ticker):
    ticker = ticker.upper()
    df = data(ticker)
    result = sm.OLS(df.ret, sm.add_constant(df[factors])).fit()
    betas = result.params[1:]
    betas = np.round(betas, 2)

    tbl = pd.DataFrame(
        dtype=float,
        index=factors + ["Total", "Risk-Free Rate", "Cost of Equity"],
        columns=["Factor Risk Premium", "Beta", "Risk Premium"],
    )
    tbl.index.name = "Factor"
    tbl.loc[factors, "Factor Risk Premium"] = fprem
    tbl.loc[factors, "Beta"] = betas
    tbl.loc[factors, "Risk Premium"] = (
        tbl.loc[factors, "Factor Risk Premium"] * tbl.loc[factors, "Beta"]
    ).round(2)
    tbl.loc["Total", "Risk Premium"] = np.round(
        tbl.loc[factors, "Risk Premium"].sum(), 2
    )
    tbl.loc["Risk-Free Rate", "Risk Premium"] = rf
    tbl.loc["Cost of Equity", "Risk Premium"] = np.round(
        tbl.loc["Total", "Risk Premium"] + rf, 2
    )

    tbl = tbl.reset_index()
    name = "ff-costequity"
    tbl.columns = [name + c for c in tbl.columns.to_list()]
    tbl["Factor"] = factors + ["Total", "Risk-Free Rate", ticker + " Cost of Equity"]

    return tbl.to_dict("records")
