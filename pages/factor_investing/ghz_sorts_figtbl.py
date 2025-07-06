# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import plotly.express as px
from pages.formatting import smallfig
import urllib.parse
from sqlalchemy import create_engine

chars = [
    "bm",
    "ep",
    "cashpr",
    "dy",
    "lev",
    "sp",
    "roic",
    "rd_sale",
    "rd_mve",
    "agr",
    "gma",
    "chcsho",
    "lgr",
    "acc",
    "pctacc",
    "cfp",
    "absacc",
    "age",
    "chinv",
    "hire",
    "sgr",
    "pchsale_pchinvt",
    "pchsale_pchrect",
    "pchgm_pchsale",
    "pchsale_pchxsga",
    "depr",
    "pchdepr",
    "invest",
    "egr",
    "grcapx",
    "tang",
    "sin",
    "currat",
    "pchcurrat",
    "quick",
    "pchquick",
    "salecash",
    "salerec",
    "saleinv",
    "pchsaleinv",
    "cashdebt",
    "realestate",
    "divi",
    "divo",
    "securedind",
    "secured",
    "convind",
    "grltnoa",
    "rd",
    "operprof",
    "ps",
    "chpmia",
    "chatoia",
    "chempia",
    "bm_ia",
    "pchcapx_ia",
    "tb",
    "cfp_ia",
    "mve_ia",
    "herf",
    "orgcap",
    "mve",
    "chtx",
    "roaq",
    "roeq",
    "rsup",
    "stdacc",
    "roavol",
    "stdcf",
    "cash",
    "cinvest",
    "nincr",
    "sue",
    "aeavol",
    "ear",
    "ms",
    "disp",
    "chfeps",
    "fgr5yr",
    "nanalyst",
    "sfe",
    "chnanalyst",
    "mom6m",
    "mom12m",
    "mom36m",
    "mom1m",
    "dolvol",
    "chmom",
    "turn",
    "ipo",
    "indmom",
    "maxret",
    "retvol",
    "baspread",
    "std_dolvol",
    "std_turn",
    "ill",
    "zerotrade",
    "beta",
    "betasq",
    "pricedelay",
    "idiovol",
]

intchars = [
    "age",
    "sin",
    "divi",
    "divo",
    "securedind",
    "convind",
    "rd",
    "ps",
    "nincr",
    "ms",
    "ipo",
]

chars = [x for x in chars if x not in intchars]
chars = np.sort(chars)
labels = ["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]




def data(char):
    server = "eu-az-sql-serv1.database.windows.net:1433"
    database = "dgn022k6348dcyh"
    username = "uhgrque4d8p77hf"
    password = "FfWrgFcK$Vnk@9BAgKH4nbEDF"
    password = urllib.parse.quote_plus(password)

    string = "mssql+pymssql://" + username + ":" + password + "@" + server + "/" + database
    conn = create_engine(string).connect()
    df = pd.read_sql(
        " select date, ret, " + char + " from ghz where date>='2000-01-01' ", conn
    )
    df = df.dropna()

    def cut(x):
        try:
            out = pd.qcut(x, 5, labels=labels)
        except:
            out = pd.Series(np.nan, index=x.index)
        return out

    df["quintile"] = df.groupby("date")[char].apply(cut)
    df = df.dropna(subset=["quintile"])
    rets = df.groupby(["date", "quintile"]).ret.mean().unstack()
    return rets


def figtbl(char, n_clicks):
    rets = data(char)
    accum = (1 + rets).cumprod()

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
    d = rets.describe()["Return"].iloc[1:]
    d.index.name = "Statistic"
    d = d.reset_index()
    rets.columns = labels
    rets.index.name = None
    rets.index = pd.to_datetime(rets.index).to_period("M")

    fig1.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return (
        smallfig(fig1, showlegend=True),
        smallfig(fig2, showlegend=True),
        smallfig(fig3),
        d,
        rets,
    )
