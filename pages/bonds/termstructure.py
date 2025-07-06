# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

# this page has no interactive elements
# the fig imported from figtbl includes the animation button

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, dash_table
from pages.bonds.termstructure_figtbl import figtbl
from pages.formatting import Layout

title = "Term structure of interest rates"
runtitle = None
chapter = "Fixed Income"
chapter_url = "fixed-income"
urls = None
text = """ Yields of U.S. Treasury bills, notes, and bonds are shown as a function of the maturity of the instrument 
              on the first trading day of each month.  The data is provided by
              [Federal Reserve Economic Data](https://fred.stlouisfed.org/). """
name = "termstructure"
graph = dcc.Loading(
    id=name + "loading", children=[dcc.Graph(id=name+"fig")], type="circle"
)
body = html.Div([
    graph,
dbc.Button(id=name+'invisible btn', style={'display':'none'})]
)
layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
@callback(Output(name + "fig", "figure"), Input(name + "invisible btn", "n_clicks"))
def call(nclicks):
    return figtbl(nclicks)