# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 10:28:20 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.three_assets_figtbl import figtbl
from pages.formatting import Slider, Layout, blue

title = "Diversification benefit of adding a third risky asset"
runtitle = "Three Asset Diversification"
chapter = "Portfolios"
chapter_url = chapter.lower()

urls = {
    "Python notebook": "https://github.com/bbcx-investments/notebooks/blob/788aaf8c83ea7bed98331c85666379fd7ec64d6b/portfolios/three_assets.ipynb"
}

text = """ Expected returns and risks are shown for various portfolios.  The portfolios
             do not have short positions (all weights are nonnegative) and are fully invested 
             (weights sum to 1).  Hover over the points to see each portfolio's
             composition."""

name = "random3"
inputs = [name + "input" + str(i) for i in range(9)]

slider1 = Slider(
    "Expected return of asset 1",
    mn=5,
    mx=20,
    step=1,
    value=8,
    tick=5,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Expected return of asset 2",
    mn=5,
    mx=20,
    step=1,
    value=12,
    tick=5,
    kind="pct",
    name=inputs[1],
)
slider3 = Slider(
    "Expected return of asset 3",
    mn=5,
    mx=20,
    step=1,
    value=15,
    tick=5,
    kind="pct",
    name=inputs[2],
)
slider4 = Slider(
    "Standard deviation of asset 1",
    mn=5,
    mx=45,
    step=1,
    value=15,
    tick=10,
    kind="pct",
    name=inputs[3],
)
slider5 = Slider(
    "Standard deviation of asset 2",
    mn=5,
    mx=45,
    step=1,
    value=25,
    tick=10,
    kind="pct",
    name=inputs[4],
)
slider6 = Slider(
    "Standard deviation of asset 3",
    mn=5,
    mx=45,
    step=1,
    value=25,
    tick=10,
    kind="pct",
    name=inputs[5],
)
slider7 = Slider(
    "Correlation of asset 1 with asset 2",
    mn=-100,
    mx=100,
    step=1,
    value=15,
    tick=50,
    kind="pct",
    name=inputs[6],
)
slider8 = Slider(
    "Correlation of asset 1 with asset 3",
    mn=-100,
    mx=100,
    step=1,
    value=50,
    tick=50,
    kind="pct",
    name=inputs[7],
)
slider9 = Slider(
    "Correlation of asset 2 with asset 3",
    mn=-100,
    mx=100,
    step=1,
    value=35,
    tick=50,
    kind="pct",
    name=inputs[8],
)

graph = dcc.Graph(id=name + "fig")
graph = dcc.Loading(id=name + "loading", children=[graph], type="circle")

left   = dbc.Col([slider1, slider2, slider3], xs=12, sm=12, md=4, lg=4, xl=4)
middle = dbc.Col([slider4, slider5, slider6], xs=12, sm=12, md=4, lg=4, xl=4)
right  = dbc.Col([slider7, slider8, slider9], xs=12, sm=12, md=4, lg=4, xl=4)
row = dbc.Row([left, middle, right], align="center", className="g-3")

col1 = dbc.Col(html.Div('Positive-definite Covariance Matrix?'), xs=12, sm=12, md=6, lg=6, xl=6, width={'offset': 2})
col2 = dbc.Col(html.Div(id=name+'PDCov', style={'color': blue}), xs=12, sm=12, md=4, lg=4, xl=4)
row2 = dbc.Row([col1, col2], className="g-3")

body = dbc.Container(html.Div([row, html.Br(),row2, html.Br(), graph]))

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + "fig", "figure"), Output(name + "PDCov", "children")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(*args)
