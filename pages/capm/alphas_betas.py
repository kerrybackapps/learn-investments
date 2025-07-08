# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 16:46:49 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.formatting import Layout, style_data, css_no_header, myinput
from pages.capm.alphas_betas_figtbl import figtbl

title = "Alphas and betas"
runtitle = None
chapter = "Capital Asset Pricing Model"
chapter_url = "capm"
urls = None

text = """ 
    Input a ticker.  Monthly returns for the ticker are computed from the adjusted closing prices provided by
    Yahoo Finance.  Monthly U.S. stock market returns and the monthly risk-free rate are downloaded from 
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  The 
    monthly excess stock returns
    (return minus risk-free rate) are regressed on the monthly excess market returns for the most recent 60
    months, that is, the following regression is estimated:
    $r - r_f = \\alpha +\\beta (r_m-r_f) + \\varepsilon$, where $r=$ stock return, $r_f=$ risk-free return, 
    $r_m=$ market return, and $\\varepsilon$ is a zero-mean risk that is uncorrelated with $r_m$.  The 
    alpha is reported in the table in basis points (per month).
    """

name = "alphas-betas"

graph = dcc.Loading(dcc.Graph(id=name + "fig"), type="circle")

# table with no column names
tbl = DataTable(
    id=name + "tbl",
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_cell_conditional=[
        {
            'if': {'column_id': 'index'},
            'textAlign': 'left'
        }
    ],
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl = dcc.Loading(id=name + "loading", children=tbl, type="circle")

inpt = myinput(id=name + "ticker", placeholder="Enter a ticker")
inpt = dbc.Col(inpt, width={"size": 4}, className="offset-md-4")
row1 = html.Div(inpt)

left = dbc.Col(tbl, xs=12, sm=12, md=3, lg=3, className="mb-2")
right = dbc.Col(graph, xs=12, sm=12, md=9, lg=9, className="mb-2")
row2 = dbc.Row([left, right], align="top", className="gx-1")

body = dbc.Container([row1, html.Br(), row2], fluid=True, className="px-1")

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
    Input(name + "ticker", "value"),
]


@callback(*lst, prevent_initial_call=True)
def call(*args):
    return figtbl(*args)
