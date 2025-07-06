# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

import pandas as pd
from pages.formatting import smallfig
import plotly.express as px

#
df = pd.read_csv("assets/_outliers_df.csv")

def figtbl(addtox, addtoy):
    df2 = df.copy()
    df2.loc[0, "x"] += addtox
    df2.loc[0, "y"] += addtoy

    fig = px.scatter(
        df2,
        x="x",
        y="y",
        trendline="ols",
        color="color",
        category_orders={"color": ["default", "special"]},
        trendline_scope="overall",
        width=1000,
        height=500
    )
    fig.update_traces(
        marker=dict(
            size=8,
            line=dict(width=2, color='DarkSlateGrey')
        ),
        selector=dict(
            mode='markers'
        )
    )
    fig.update_layout(
        xaxis_range=[-25, 25],
        yaxis_range=[-25, 25],
    )

    fig.layout.template = "plotly_dark"
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=25))
    fig.update_xaxes(title_font_size=16, showgrid=True)
    fig.update_yaxes(title_font_size=16, showgrid=True)
    fig.update_layout(font_size=14, showlegend=False)

    return fig
