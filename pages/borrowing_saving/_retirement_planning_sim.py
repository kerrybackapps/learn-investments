# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:31:00 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.borrowing_saving.retirement_planning_sim_figtbl import figtbl
from pages.formatting import (
    Slider,
    Layout,
    style_data,
    css_no_header,
    style_data_conditional,
    white,
    primary
)

name = "_retirement_planning_sim"

btn = dbc.Button(
    "Click to Simulate",
    id=name + "button",
    n_clicks=0,
    color="primary",
    className="me-1",
)

inputs = [name + "input" + str(i) for i in range(8)]

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
    "Annual expected return", mn=0, mx=12, step=1, value=6, tick=4, kind="pct", name=inputs[6]
)
slider8 = Slider(
    "Annual standard deviation",
    mn=5,
    mx=20,
    step=1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[7],
)


tbl = DataTable(
    id=name + "tbl",
    columns = [{'name':c, 'id': name+c} for c in ['col1', 'col2']],
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)

left = dbc.Col([slider1, slider2, slider3, slider7])
right = dbc.Col([slider4, slider5, slider6, slider8])
row = dbc.Row([left, right], align="center")

btn = dbc.Row(
    dbc.Col(
        btn, width={"size": 3, "offset": 5}
    )
)
left = dbc.Col([btn, html.Br(), row], xs=8)
right = dbc.Col(tbl, xs=4)
row1 = dbc.Row([left, right], align="center")

fig1 = dbc.Col(dcc.Graph(name + "fig1"), xs=6)
fig2 = dbc.Col(dcc.Graph(name + "fig2"), xs=6)
row2 = dbc.Row([fig1, fig2])


layout = dbc.Container([html.Br(), html.Br(), row1, html.Br(), row2], fluid=True)

@callback(
    Output(name + "fig1", "figure"),
    Output(name + "fig2", "figure"),
    Output(name + "tbl", "data"),
    Input(name + "button", "n_clicks"),
    *[State(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(name, *args)
