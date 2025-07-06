# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
import plotly.express as px
from pandas_datareader import DataReader as pdr
from pages.formatting import largefig

def figtbl(nclicks):
    files = ["DGS" + x for x in ["1MO", "3MO", "1", "2", "3", "5", "10", "20", "30"]]
    df = pdr(files, "fred", start='2000-01-01') / 100

    df.index.name = "date"
    df = df.reset_index()

    df["month"] = df.date.dt.to_period("M").astype(str)
    df = df.groupby("month").first()
    df = df.drop(columns=["date"])
    df = df.dropna(subset=["DGS3MO", "DGS30"])
    df.columns = [1 / 12, 1 / 4, 1, 2, 3, 5, 10, 20, 30]

    df = df.stack()
    df = df.reset_index()
    df.columns = ["date", "years to maturity", "yield"]

    fig = px.line(
        df,
        x="years to maturity",
        y="yield",
        animation_frame="date",
        hover_data={"date": True, "years to maturity": True, "yield": True}
    )
    fig.layout.xaxis["title"] = "Years to Maturity"
    fig.layout.yaxis["title"] = "Yield"
    fig.update_yaxes(tickformat=".1%", range=[0, df["yield"].max() + 0.001])
    fig.update_xaxes(tickvals=[1, 3, 5, 10, 20, 30], range=[0, 30])
    fig.for_each_trace(lambda t: t.update(mode='lines+markers', marker=dict(size=10)))
    for fr in fig.frames:
        for d in fr.data:
            d.update(mode='markers+lines', marker=dict(size=10))
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    return largefig(fig)

