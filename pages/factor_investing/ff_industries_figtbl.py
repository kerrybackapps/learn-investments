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
from pages.data.ff_monthly import ff5 as ff, ff48 as df

d = dict(
    Agric="Agriculture",
    Food="Food Products",
    Soda="Candy & Soda",
    Beer="Beer & Liquor",
    Smoke="Tobacco Products",
    Toys="Recreation",
    Fun="Entertainment",
    Books="Printing & Publishing",
    Hshld="Consumer Goods",
    Clths="Apparel",
    Hlth="Health Care",
    MedEq="Medical Equipment",
    Drugs="Pharmaceutical Products",
    Chems="Chemicals",
    Rubbr="Rubber and Plastic Products",
    Txtls="Textiles",
    BldMt="Construction Materials",
    Cnstr="Construction",
    Steel="Steel Works Etc",
    FabPr="Fabricated Products",
    Mach="Machinery",
    ElcEq="Electrical Equipment",
    Autos="Automobiles & Trucks",
    Aero="Aircraft",
    Ships="Shipbuilding & Railroad Equipment",
    Guns="Defense",
    Gold="Precious Metals",
    Mines="Non-Metallic & Industrial Metal Mining",
    Coal="Coal",
    Oil="Petroleum & Natural Gas",
    Util="Utilities",
    Telcm="Communication",
    PerSv="Personal Services",
    BusSv="Business Services",
    Comps="Computers",
    Chips="Electronic Equipment",
    LabEq="Measuring & Control Equipment",
    Paper="Business Supplies",
    Boxes="Shipping Containers",
    Trans="Transportation",
    Whlsl="Wholesale",
    Rtail="Retail",
    Meals="Restaurants, Hotels, & Motels",
    Banks="Banking",
    Insur="Insurance",
    RlEst="Real Estate",
    Fin="Trading",
    Other="Almost Nothing",
)



df.columns = [x.strip() for x in df.columns]
df = df.rename(columns=d)
inds = df.columns.to_list()
df = df.join(ff, how="inner")
df[inds] = df[inds].subtract(df.RF, axis="index")

factors = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]


def figtbl(dates):
    start = str(dates[0]) + "-01"
    stop = str(dates[1]) + "-12"
    d1 = df.loc[start:stop]

    d2 = pd.DataFrame(dtype=float, index=inds, columns=["empirical", "theoretical"])
    d2.index.name = "industry"
    d2["empirical"] = 12 * d1[inds].mean()

    X = sm.add_constant(d1[factors])

    def beta(y):
        return sm.OLS(y, X).fit().params[1:]

    betas = d1[inds].apply(beta)
    fprem = 12 * d1[factors].mean()
    d2["theoretical"] = fprem @ betas

    d2 = d2.reset_index()

    fig1 = px.scatter(
        d2,
        x="theoretical",
        y="empirical",
        hover_name="industry",
        trendline="ols",
        hover_data={"theoretical": False, "empirical": True},
    )
    fig1.update_traces(
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )

    fig2 = px.scatter(d2, x="theoretical", y="theoretical", hover_name="industry")
    fig2.update_traces(
        marker=dict(size=12, color=green, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig = go.Figure(data=fig1.data + fig2.data)

    fig.layout.xaxis["title"] = "Theoretical Mean Excess Return (Annualized)"
    fig.layout.yaxis["title"] = "Empirical Mean Excess Return (Annualized)"
    fig.update_yaxes(tickformat=".1%")
    fig.update_xaxes(tickformat=".1%")
    return largefig(fig)
