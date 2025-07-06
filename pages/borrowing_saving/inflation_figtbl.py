# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import plotly.express as px
from pages.formatting import largefig, blue
from pandas_datareader import DataReader as pdr
import plotly.graph_objects as go
from pages.data.ff_annual import ff3_annual as df

mkt = df["Mkt-RF"] + df.RF
mkt.index.name = "Year"
mkt.index = mkt.index.astype(str).astype(int)
mkt = pd.DataFrame(mkt)
mkt.columns = ["Market"]

df = pdr("CPIAUCSL", "fred", start="1949-12-01")
df = df.resample("Y").last().iloc[:-1]
df = df.pct_change().reset_index()
df.columns = ["Year", "Inflation"]
df["Year"] = df.Year.map(lambda x: x.year)

df = df.merge(mkt, left_on="Year", right_index=True, how="inner")

def figtbl(dates):
    dates = [int(x) for x in dates]
    d = df[(df.Year >= dates[0]) & (df.Year <= dates[1])].copy()
    avg_infl = d.Inflation.mean()
    string = "%{x}<br>Inflation = %{y:.1%}<extra></extra>"
    fig1 = go.Figure(go.Scatter(x=d.Year, y=d.Inflation, hovertemplate=string))
    fig1.update_yaxes(tickformat=".0%", title="Inflation Rate")
    d2 = pd.DataFrame(
        index=[d.Year.min() - 1] + d.Year.to_list(), columns=["Nominal", "CPI", "Real"]
    )
    d2.index.name = "Year"
    d2 = d2.reset_index()
    d2["Nominal"] = [1] + (1 + d.Market).cumprod().to_list()
    d2["CPI"] = [1] + (1 + d.Inflation).cumprod().to_list()
    d2["Real"] = d2.Nominal / d2.CPI
    string1 = "Accumulation in Nominal $ = %{y:0.2f}<extra></extra>"
    trace1 = go.Scatter(
        x=d2.Year, y=d2.Nominal, hovertemplate=string1, name="Nominal $"
    )
    string2 = "Accumulation in Constant $ = %{y:0.2f}<extra></extra>"
    trace2 = go.Scatter(x=d2.Year, y=d2.Real, hovertemplate=string2, name="Constant $")
    fig2 = go.Figure(trace1)
    fig2.add_trace(trace2)
    fig2.update_xaxes(title="Year")
    fig2.update_yaxes(title="Compound Return", tickformat="$.0f")
    fig2.update_layout(hovermode="x unified")
    real = d2.Real.pct_change().mean()
    nominal = d2.Nominal.pct_change().mean()

    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return (
        largefig(fig1),
        largefig(fig2, showlegend=True),
        f"{nominal:.2%}",
        f"{avg_infl:.2%}",
        f"{real: .2%}"
    )
