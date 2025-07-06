# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:31:00 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.risk.means_figtbl import figtbl
from pages.formatting import (
    Slider,
    Layout,
    style_header,
    style_data_conditional,
)

title = "Arithmetic and geometric averages as forecasts"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "means"

text = """ 
    $n$ past investment returns are simulated, and the arithmetic and geometric average returns are calculated, 
    where $n$ is the number of years in the specified investment period.  The same 
    number of future investment returns is 
    simulated and the compound return $(1+r_1) \cdots (1+r_n)-1$ and average return $(1/n)\sum_{i=1}^n r_i$ are
    calculated.  This page examines whether the past arithmetic and geometric average returns are good predictors of
    the future compound and average returns.  To predict the future compound return, predictors are formed as
    $(1+ \\bar{r}_{\\text{arithmetic}})^n-1$ and $(1+ \\bar{r}_{\\text{geometric}})^n-1$, where
    $\\bar{r}_{\\text{arithmetic}}$ and $\\bar{r}_{\\text{geometric}}$ are the past arithmetic
    and geometric averages respectively.  The prediction error (prediction
    minus outcome) is calculated for each pairing (past arithmetic average minus future average, 
    past geometric average minus future average,
    past arithmetic predictor minus future compound, past geometric predictor minus future compound).  This simulation is repeated
    5,000 times, and the distributions of the prediction errors are summarized in the box plots and tables.  RMSE is 
    "root mean squared error" and is the square root of the average squared error.  Mean AD is "mean absolute deviation"
    and is the average absolute error.  Med AD is the median absolute error.  By all criteria, the geometric average is
    the better predictor for the compound return, and the arithmetic average is the better predictor for 
    the average return.  The mean and median errors show that the arithmetic average predictor is too high for 
    predicting the compound return, and the geometric average is too low for predicting
    the average return.
    """
#
btn = dbc.Button(
    "Click to Simulate",
    id=name + "button",
    n_clicks=0,
    color="primary",
    className="me-1",
)


inputs = [name + "input" + str(i) for i in range(3)]
slider1 = Slider(
    "Expected return",
    mn=0,
    mx=12,
    step=1,
    value=6,
    tick=3,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Standard deviation",
    mn=0,
    mx=20,
    step=1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[1],
)

slider3 = Slider(
    "Investment period (years)",
    mn=1,
    mx=40,
    step=1,
    value=20,
    tick=None,
    kind="tip",
    name=inputs[2],
)

tbl1 = DataTable(
    id=name + "tbl1",
    columns=[
        {'name': c, 'id': name+c}
        for c in ["", "Arithmetic", "Geometric"]
    ],
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_cell_conditional=[
        {
            'if': {'column_id': name},
            'textAlign': 'left'
        }
    ]
)

tbl2 = DataTable(
    id=name + "tbl2",
    columns=[
        {'name': c, 'id': name+"2"+c}
        for c in ["", "Arithmetic", "Geometric"]
    ],
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_cell_conditional=[
        {
            'if': {'column_id': name+"2"},
            'textAlign': 'left'
        }
    ]
)

col1 = dbc.Col(slider1, md=3)
col2 = dbc.Col(slider2, md=3)
col3 = dbc.Col(slider3, md=3)

btn = dbc.Row(
    dbc.Col(btn, width={"size": 8, "offset": 4})
)
col4 = dbc.Col(btn, md=3)
row1 = dbc.Row([col1, col2, col3, col4], align="top")

a = dbc.Col([dbc.Label('Error for Compound Return'), tbl1], md=3)
b = dbc.Col(dcc.Graph(id=name+"fig1"), md=3)
c = dbc.Col([dbc.Label('Error for Average Return'), tbl2], md=3)
d = dbc.Col(dcc.Graph(id=name+"fig2"), md=3)
row2 = dbc.Row([a, b, c, d], align="top")

body = html.Div([row1, html.Hr(), row2])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

@callback(
    Output(name + "tbl1", "data"),
    Output(name+"fig1", "figure"),
    Output(name + "tbl2", "data"),
    Output(name+"fig2", "figure"),
    Input(name+"button", "n_clicks"),
    *[State(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(name, *args)
