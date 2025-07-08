# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 09:23:46 2022

@author: kerry
"""

from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.short_sales_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Short sales"
runtitle = None
chapter = "Portfolios"
chapter_url = chapter.lower()
name = "two-assets-shorts"
urls = None

text = """ 
    The expected returns and risks of portfolios of two assets are shown.  The parts of the curve above the higher 
    mean and below the lower mean involve short sales.  It is assumed that short sales are unconstrained, meaning that
    there is full use of the proceeds (that is, the proceeds from shorting are invested in the other asset), 
    there is no cost to borrow the asset being shorted, and margin constraints are not binding.
    """


inputs = [name + "input" + str(i) for i in range(5)]

slider1 = Slider(
    "Expected return of asset 1",
    mn=0,
    mx=20,
    step=1,
    value=5,
    tick=5,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Expected return of asset 2",
    mn=0,
    mx=20,
    step=1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[1],
)
slider3 = Slider(
    "Standard deviation of asset 1",
    mn=0,
    mx=50,
    step=1,
    value=20,
    tick=10,
    kind="pct",
    name=inputs[2],
)
slider4 = Slider(
    "Standard deviation of asset 2",
    mn=5,
    mx=50,
    step=1,
    value=30,
    tick=10,
    kind="pct",
    name=inputs[3],
)
slider5 = Slider(
    "Correlation of assets",
    mn=-100,
    mx=100,
    step=5,
    value=25,
    tick=50,
    kind="pct",
    name=inputs[4],
)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider2, slider3, slider4, slider5], xs=12, sm=12, md=4, lg=4, xl=4)
right = dbc.Col(graph, xs=12, sm=12, md=8, lg=8, xl=8)
body = dbc.Container(dbc.Row([left, right], align="center", className="g-3"))

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + "fig", "figure")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(*args)
