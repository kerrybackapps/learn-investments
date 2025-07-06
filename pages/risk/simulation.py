# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:31:00 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from pages.risk.simulation_figtbl import figtbl
from pages.formatting import Slider, Layout, text_style


title = "Simulating returns"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "simulation"

text = """ 
    Returns are randomly generated from a normal distribution with the specified mean and standard deviation, for the 
    specified number of periods. The arithmetic and geometric averages of the simulated returns 
    are reported in the left panel along with the standard deviation.   The
    left figure shows the simulated returns, and the right figure shows the accumulation
    $(1+r_1)\cdots(1+r_i)$ through period $i$ for each $i\le n$, as well as what the accumulation would have been
    had either the arithmetic average or the geometric average been earned each period.
    """



btn = dbc.Button(
    "Click to Simulate",
    id=name + "button",
    n_clicks=0,
    color="primary",
    className="me-1",
)
btn = dbc.Row(btn)

inputs = [name + "input" + str(i) for i in range(3)]
slider1 = Slider(
    "Expected return",
    mn=0,
    mx=12,
    step=0.1,
    value=6,
    tick=3,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Standard deviation",
    mn=0,
    mx=20,
    step=0.1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[1],
)

slider3 = Slider(
    "Time periods",
    mn=1,
    mx=40,
    step=1,
    value=20,
    tick=None,
    kind="tip",
    name=inputs[2],
)

fig1 = dcc.Graph(id=name + "fig1")
fig2 = dcc.Graph(id=name + "fig2")

label0 = html.Div("Realized std dev")
label1 = html.Div("Arithmetic average")
label2 = html.Div("Geometric average")
string0 = html.Div(id=name+"string0", style=text_style)
string1 = html.Div(id=name+"string1", style=text_style)
string2 = html.Div(id=name+"string2", style=text_style)

col1 = dbc.Col([label2, label1, label0], width=dict(size=6, offset=2))
col2 = dbc.Col([string2, string1, string0], md=4)
row = dbc.Row([col1, col2])
btn = dbc.Row(
    dbc.Col(btn, width={"size": 6, "offset": 3})
)
left = dbc.Col([btn, html.Br(), slider1, slider2, slider3, html.Br(), row], md=4)
middle = dbc.Col(dcc.Graph(id=name+"fig1"), md=4)
right = dbc.Col(dcc.Graph(id=name+"fig2"), md=4)

body = dbc.Row([left, middle, right], align="top")

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
    Output(name+"fig1", "figure"),
    Output(name+"fig2", "figure"),
    Output(name+"string0", "children"),
    Output(name+"string1", "children"),
    Output(name+"string2", "children"),
    Input(name+"button", "n_clicks"),
    *[State(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(*args)
