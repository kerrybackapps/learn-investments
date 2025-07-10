# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import plotly.express as px
import plotly.graph_objects as go
from pandas_datareader import DataReader as pdr
from pages.formatting import largefig, green
from pages.factor_investing.two_way_sorts_figtbl import charsDict
from pages.data.ff_monthly import ff5 as ff

files = [
    '25_Portfolios_5x5',
    '25_Portfolios_ME_INV_5x5',
    '25_Portfolios_ME_Prior_12_2',
    '25_Portfolios_ME_Prior_1_0',
    '25_Portfolios_ME_Prior_60_13',
    '25_Portfolios_ME_AC_5x5',
    '25_Portfolios_ME_BETA_5x5',
    '25_Portfolios_ME_NI_5x5',
    '25_Portfolios_ME_VAR_5x5',
    '25_Portfolios_ME_RESVAR_5x5'
]

chars = [
    "Book to market ratio",
    "Investment rate",
    "Momentum",
    "Short term reversal",
    "Long term reversal",
    "Accruals",
    "Beta",
    "Net equity issuance",
    "Variance",
    "Residual variance",
]

charsDict = dict(zip(chars, files))
chars.sort()

RETS = None
CHAR = None

def table(data):
    table = data.unstack().round(2).reset_index()
    table = table.rename(columns={'index': ''})
    return table

def figtbl(char, dates):

    global CHAR, RETS

    if char != CHAR:
        CHAR = char
        RETS = pdr(charsDict[char], "famafrench", start=1963)[0] / 100
        RETS = RETS.subtract(ff.RF, axis="index")
        if char == "Net equity issuance":
            for x in RETS.columns:
                if x.split(" ")[1][0] == "Z" or x.split(" ")[1][0:2] == "Ne":
                    RETS = RETS.drop(columns=x)

    start = str(dates[0]) + "-01"
    stop = str(dates[1]) + "-12"
    df = RETS.loc[start:stop].copy()

    # see what the two chars are in the two-way sort
    s = df.columns[1].split(" ")
    s1 = s[0][:-1]             # market equity
    s2 = s[1][:-1]             # other characteristic

    def splitName(x):
        x1 = x.split(" ")[0]
        x1 = x1 if x1[0] == "M" else ("ME1" if x1[0] == "S" else "ME5")
        x2 = x.split(" ")[1]
        x2 = x2 if x2[0] == s2[0] else (s2 + "1" if x2[0] == "L" else s2 + "5")
        return x1, x2

    splits = [splitName(x) for x in df.columns]

    df.columns = pd.MultiIndex.from_tuples(splits)

    # multi-indexed index, for unstacking
    factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    regr = pd.DataFrame(
        dtype=float,
        index=df.columns,
        columns=factors + ['alpha', 'tstat', 'empirical', 'theoretical']
    )
    print(df.head())
    print(ff.head())
    df = df.join(ff).dropna()

    for port in regr.index:
        result = sm.OLS(df[port], sm.add_constant(df[factors])).fit()
        regr.loc[port, factors] = result.params[factors]
        regr.loc[port, 'alpha'] = 12 * result.params['const']
        regr.loc[port, 'tstat'] = result.tvalues['const']
        regr.loc[port, 'empirical'] = 12 * df[port].mean()
        regr.loc[port, 'theoretical'] = 12 * result.params[factors] @ df[factors].mean()

    regr['port'] = splits

    # 5 x 5 tables

    alpha_tbl = regr.alpha.unstack()
    tstat_tbl = regr.tstat.unstack()

    trace = go.Heatmap(
        x=alpha_tbl.columns.to_list(),
        y=alpha_tbl.index.to_list(),
        z=alpha_tbl,
        colorscale='Viridis',
        texttemplate="%{z:.2%}",
        hovertemplate="%{x} / %{y}<br>%{z:.3%}<extra></extra>"
    )
    alpha_tbl = go.Figure(trace)

    trace = go.Heatmap(
        x=tstat_tbl.columns.to_list(),
        y=tstat_tbl.index.to_list(),
        z=tstat_tbl,
        colorscale='Viridis',
        texttemplate="%{z:.2f}",
        hovertemplate="%{x} / %{y}<br>%{z:.3f}<extra></extra>"
    )
    tstat_tbl = go.Figure(trace)

    return largefig(alpha_tbl), largefig(tstat_tbl)

