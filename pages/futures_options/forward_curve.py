# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:19:47 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.futures_options.forward_curve_figtbl import keys, figtbl
from pages.formatting import Layout, lightblue

title = "Forward curves"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"

urls = None

text = """ Historical forward curves are shown for commodities, currencies, and financial futures.  
             """

name = "forward-curve"

drop = dcc.Dropdown(keys, placeholder="Select a contract", id=name + "drop", style={"backgroundColor": lightblue})
drop = dbc.Col(drop, xs=12, sm=8, md=6, lg=6, className="mb-2", width={"size": 6, "offset": 3})
drop = dbc.Row([drop], className="gx-1")

graph = dcc.Graph(id=name + "fig")
loading = dcc.Loading(id=name + "loading", children=[html.Div(graph)], type="circle",)
body = dbc.Container([drop, html.Br(), loading], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
outputs = [Output(name + "fig", "figure")]
inputs = [Input(name + "drop", "value"), Input(name + "loading", "value")]
lst = outputs + inputs

import plotly.graph_objects as go

@callback(
    Output(name + "fig", "figure"),
    Input(name + "drop", "value"),
    prevent_initial_call=True
)
def call(contract):
    return figtbl(contract)
