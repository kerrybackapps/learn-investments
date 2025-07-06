# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
import plotly.express as px
from pages.formatting import largefig
from pages.data.sbb import nominal
from pages.data.inflation import inflation

df = pd.concat((nominal, inflation), axis=1).dropna()
assets = ['S&P 500', 'Gold', 'Corporates', 'Treasuries', 'TBills']
df = df[assets + ['Inflation']]
for asset in assets:
    df[asset] = (1+df[asset]) / (1+df.Inflation) - 1
df = df[assets]


def figtbl(name, dates):

    rets = df.loc[dates[0]:dates[1]]

    accum = (1 + rets).cumprod()
    accum.loc[dates[0] - 1] = 1
    accum = accum.sort_index()

    rets = rets.stack().reset_index()
    rets.columns = ["Year", "Asset", "Return"]

    accum = accum.stack().reset_index()
    accum.columns = ["Year", "Asset", "Compound Return"]

    fig1 = px.line(
        accum,
        x="Year",
        y="Compound Return",
        color="Asset",
        category_orders={"Asset": assets},
    )
    fig2 = px.line(
        accum,
        x="Year",
        y="Compound Return",
        log_y=True,
        color="Asset",
        category_orders={"Asset": assets},
    )
    fig2.update_yaxes(title="Compound Return (Log Scale)")

    fig3 = px.box(
        rets, x="Asset", y="Return", color="Asset", category_orders={"Asset": assets}
    )
    fig3.update_yaxes(title=None, tickformat=".1%")
    fig3.update_xaxes(title=None)
    fig3.update_traces(hovertemplate="%{y:.1%}<extra></extra>")

    string = "$%{y:,.2f}<extra></extra>"
    for fig in [fig1, fig2]:
        fig.update_traces(mode="lines", hovertemplate=string)
        fig.update_layout(hovermode="x unified")

    rets = rets.set_index(["Year", "Asset"]).Return.unstack("Asset")
    rets = rets[assets]

    tbl = pd.DataFrame(rets.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).iloc[1:]).reset_index()
    tbl.columns = [name+x for x in [""] + assets]

    fig1.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return [largefig(fig, showlegend=True) for fig in [fig1, fig2, fig3]] + [tbl.to_dict('records')]

