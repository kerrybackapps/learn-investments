# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:40:58 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.borrowing_saving.retirement_planning_figtbl import figtbl
from pages.formatting import (
    Slider,
    Layout,
    blue,
    text_style
)

name = "_retirement-planning"

inputs = [name + "input" + str(i) for i in range(7)]
slider1 = Slider(
    "Initial balance",
    mn=0,
    mx=1000000,
    step=1000,
    value=100000,
    tick=200000,
    name=inputs[0],
    kind="kdol",
)
slider2 = Slider("Years saving", mn=0, mx=50, step=1, value=30, tick=10, name=inputs[1])
slider3 = Slider(
    "Years withdrawing", mn=0, mx=50, step=1, value=30, tick=10, name=inputs[2]
)
slider4 = Slider(
    "Initial monthly savings",
    mn=0,
    mx=10000,
    step=100,
    value=1000,
    tick=2000,
    name=inputs[3],
    kind="kdol",
)
slider5 = Slider(
    "Annual savings growth rate",
    mn=0,
    mx=10,
    step=0.1,
    value=2,
    tick=2,
    name=inputs[4],
    kind="pct",
)
slider6 = Slider(
    "Monthly withdrawal",
    mn=0,
    mx=50000,
    step=100,
    value=10000,
    tick=10000,
    name=inputs[5],
    kind="kdol",
)
slider7 = Slider(
    "Annual rate of return",
    mn=0,
    mx=15,
    step=0.1,
    value=6,
    tick=3,
    name=inputs[6],
    kind="pct",
)

graph = dcc.Graph(id=name + "fig")

col1 = dbc.Col(html.Div('Ending balance:'), width={'size': 3, 'offset': 3})
col2 = dbc.Col(html.Div(id=name+'string', style=text_style), width={'size': 2})
row = dbc.Row([col1, col2])

left = dbc.Col([slider1, slider2, slider3, slider4, slider5, slider6, slider7], xs=4)
right = dbc.Col([row, html.Br(), graph], xs=8)
layout = dbc.Container([html.Br(), html.Br(), dbc.Row([left, right], align="center")], fluid=True)

lst = [Output(name + "fig", "figure"), Output(name + "string", "children")] + [
    Input(i, "value") for i in inputs
]


@callback(*lst)
def call(*args):
    return figtbl(*args)

