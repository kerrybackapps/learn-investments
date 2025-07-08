# -*- coding: utf-8 -*-
"""
Created on Tue May 10 09:31:30 2022

@author: Kevin
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

from pages.taxes.tax_vehicles_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Tax-advantaged savings vehicles"
runtitle = "Tax-Advantaged Savings Vehicles"
chapter = "Topics"
chapter_url = "topics"
urls = {"Python notebook": None}
text = """ The future after-tax value of an initial after-tax dollar of investment is calculated.  Withdrawal from the account occurs at time T.  An initial tax rate for ordinary income is assumed to prevail until time T-1, at which point it changes to the ending tax rate.  The rate of return input denotes the pre-tax per period rate of return. **No Advantage** assume no tax benefits and any returns are taxed immediately.  **Non-deductible IRA** contributions are made in after-tax dollars and taxation on gains is deferred until withdrawal at which time they are taxed as ordinary income.  **Roth** contributions are made using after-tax dollars and earnings are tax-exempt.  **401k** contributions are tax deductible and taxation of both initial investment and gains occurs at withdrawal at ordinary income rates.   """

name = "tax_vehicles"

inputs = [name + "input" + str(i) for i in range(4)]
slider1 = Slider(
    "Initial tax rate on ordinary income",
    mn=0,
    mx=40,
    step=1,
    value=35,
    tick=10,
    name=inputs[0],
    kind="tip",
)
# slider2 = Slider(
#     "Initial tax rate on capital gains",
#     mn=0,
#     mx=40,
#     step=1,
#     value=35,
#     tick=10,
#     name=inputs[1],
#     kind="tip",
# )
slider3 = Slider(
    "Ending tax rate on ordinary income",
    mn=0,
    mx=40,
    step=1,
    value=30,
    tick=10,
    name=inputs[1],
    kind="tip",
)
# slider4 = Slider(
#     "Ending tax rate on capital gains",
#     mn=0,
#     mx=40,
#     step=1,
#     value=35,
#     tick=10,
#     name=inputs[3],
#     kind="tip",
# )
slider5 = Slider(
    "Annual rate of return",
    mn=0,
    mx=15,
    step=0.1,
    value=6,
    tick=3,
    name=inputs[2],
    kind="pct",
)
slider6 = Slider(
    "Years saving", 
    mn=0, 
    mx=50, 
    step=1, 
    value=30, 
    tick=None, 
    name=inputs[3], 
    kind="tip"
)

graph = dcc.Graph(id=name + "fig")

# left = dbc.Col([slider5, slider1, slider2, slider3, slider4, slider6], md=4)
left = dbc.Col([slider5, slider1, slider3, slider6], xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col([graph], xs=12, sm=12, md=8, lg=8, className="mb-2")
body = dbc.Container(dbc.Row([left, right], align="center", className="gx-1"), fluid=True, className="px-1")

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
    fig = figtbl(*args)
    return fig
