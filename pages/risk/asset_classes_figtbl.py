# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
import yfinance as yf

DATA = pd.DataFrame(0, index=[0], columns=["NotATicker"])

def get_rets(tickers):

    tickers = [t.upper() for t in tickers]

    global DATA

    if set(tickers) == set(DATA.columns.to_list()):
        return DATA[tickers]

    else:
        try:
            df = yf.download(" ".join(tickers), interval="1mo", start="1970-01-01")
            DATA = df["Close"].pct_change().dropna().iloc[:-1]
            DATA.index = DATA.index.to_period("M").astype(str)
            return DATA
        except:
            return DATA

def figtbl(dates, tickers):

    minyear = str(dates[0])
    maxyear = str(int(dates[1]) + 1)

    df = get_rets(tickers)

    df2 = df[(df.index>=minyear) & (df.index<maxyear)].copy()

    corr = df2.corr()
    for col in corr.columns:
        corr[col] = corr[col].map(lambda c: f"{c:.1%}")
    corr = corr.reset_index()
    corr.columns = [""] + df.columns.to_list()
    return corr.to_dict('records'), df2.index.min() + " through " + df2.index.max()




