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

# topmatter
title = "Retirement planning simulation"
runtitle = None
chapter = "Borrowing and Saving"
chapter_url = "borrowing-saving"
urls = None
text = """ 
    A retirement account is tracked assuming annual deposits and withdrawals as described on the "Retirement
    Planning" page, except that here the annual returns are randomly
    generated from a normal distribution with the specified mean and standard deviation. 1,000
    possible lifetimes are simulated, and the distribution of the 1,000 ending balances is described in
    the table.  The figure on the left in the second row is a box plot of the ending balances, and the 
    figure on the right displays the percentiles of the ending balance distribution, supplementing the
    information in the table.
    """

name = "retirement_planning_sim"

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
    "Initial annual savings",
    mn=0,
    mx=100000,
    step=1000,
    value=10000,
    tick=20000,
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
    "Annual withdrawal",
    mn=0,
    mx=500000,
    step=1000,
    value=100000,
    tick=100000,
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
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

left = dbc.Col([slider1, slider2, slider3, slider7], xs=12, sm=6, md=6, lg=6, className="mb-2")
right = dbc.Col([slider4, slider5, slider6, slider8], xs=12, sm=6, md=6, lg=6, className="mb-2")
row = dbc.Row([left, right], align="center", className="gx-1")

btn = dbc.Row(
    dbc.Col(
        btn, width={"size": 3}, className="offset-md-5"
    )
)
left = dbc.Col([btn, html.Br(), row], xs=12, sm=12, md=8, lg=8, className="mb-2")
right = dbc.Col(tbl, xs=12, sm=12, md=4, lg=4, className="mb-2")
row1 = dbc.Row([left, right], align="center", className="gx-1")

fig1 = dbc.Col(dcc.Graph(name + "fig1"), xs=12, sm=12, md=6, lg=6, className="mb-2")
fig2 = dbc.Col(dcc.Graph(name + "fig2"), xs=12, sm=12, md=6, lg=6, className="mb-2")
row2 = dbc.Row([fig1, fig2], className="gx-1")


body = dbc.Container([row1, html.Br(), row2], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body
)


@callback(
    Output(name + "fig1", "figure"),
    Output(name + "fig2", "figure"),
    Output(name + "tbl", "data"),
    Input(name + "button", "n_clicks"),
    *[State(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(name, *args)
