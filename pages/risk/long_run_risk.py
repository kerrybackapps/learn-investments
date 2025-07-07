# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:31:00 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable, FormatTemplate

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

from pages.risk.long_run_risk_figtbl import figtbl
from pages.formatting import (
    Slider,
    Layout,
    style_header,
    style_data,
    style_data_conditional,
)

title = "Skewness of long-run returns"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "longrunrisk_sim"

text = """ 
    Suppose $1 is invested in an asset or portfolio and the investment is maintained for the
    specified number of years, with dividends reinvested.  The probability distributions of
    the investment values at the end of the given number of years are calculated for two different sets of parameter values
    by simulating
    5,000 hypothetical investment "lifetimes" for each set of parameter values, 
    assuming the returns each year are independent draws
    from normal distributions with the specified means and standard deviations.  Compounding induces
    positive skewness, which can be seen from the boxplots.  Because of the positive skewness, 
    the mean accumulation exceeds the median.  The distribution is more positively skewed and the difference between 
    mean and median is larger when the volatility is higher.  The figure on the right shows the percentiles of
    the accumulations from two returns.  If the two returns have
    the same mean, then they produce the same mean long-run accumulation, but the lower-risk
    return has the higher median.
    """


btn = dbc.Button(
    "Click to Simulate",
    id=name + "button",
    n_clicks=0,
    color="primary",
    className="me-1",
)


inputs = [name + "input" + str(i) for i in range(5)]
slider1 = Slider(
    "Expected return 1",
    mn=0,
    mx=12,
    step=0.1,
    value=6,
    tick=3,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Standard deviation 1",
    mn=5,
    mx=20,
    step=0.1,
    value=15,
    tick=5,
    kind="pct",
    name=inputs[1],
)
slider3 = Slider(
    "Expected return 2",
    mn=0,
    mx=12,
    step=0.1,
    value=6,
    tick=3,
    kind="pct",
    name=inputs[2],
)
slider4 = Slider(
    "Standard deviation 2",
    mn=5,
    mx=20,
    step=0.1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[3],
)
slider5 = Slider(
    "Years invested",
    mn=1,
    mx=40,
    step=1,
    value=20,
    tick=None,
    kind="tip",
    name=inputs[4],
)

graph1 = dcc.Graph(id=name + "fig1")
graph2 = dcc.Graph(id=name + "fig2")

cols = ["", "Return 1", "Return 2"]
tbl = DataTable(
    id=name + "tbl",
    columns=[dict(name=c, id=name + c, type="numeric", format=money) for c in cols],
    style_data=style_data,
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

btn = dbc.Row(
    dbc.Col(btn, width={"size": 8, "offset": 4})
)
left = dbc.Col([btn, html.Br(), slider5], xs=12, sm=12, md=4, lg=4, className="mb-2")
mid = dbc.Col([slider1, slider2], xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col([slider3, slider4], xs=12, sm=12, md=4, lg=4, className="mb-2")
row1 = dbc.Row([left, mid, right], align="center", className="gx-1")

left = dbc.Col([btn, html.Br(), slider1, slider2, slider3, slider4, slider5], md=3)
left = dbc.Col(tbl, xs=12, sm=12, md=4, lg=4, className="mb-2")
mid = dbc.Col(graph1, xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col(graph2, xs=12, sm=12, md=4, lg=4, className="mb-2")
row2 = dbc.Row([left, mid, right], align="center", className="gx-1")

body = dbc.Container([row1, html.Hr(), html.Br(), row2], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [
    Output(name + "fig", "figure"),
    Output(name + "tbl", "data"),
    Input(name + "button", "n_clicks"),
] + [State(i, "value") for i in inputs]


@callback(
    Output(name+"tbl", "data"),
    Output(name+"fig1", "figure"),
    Output(name+"fig2", "figure"),
    Input(name+"button", "n_clicks"),
    *[State(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(name, *args)

