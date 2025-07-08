# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 16:46:49 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.formatting import Layout, style_data, css_no_header, style_data_conditional, myinput
from pages.capm.capm_costequity_figtbl import figtbl

title = "CAPM cost of equity calculator"
runtitle = None
chapter = "Capital Asset Pricing Model"
chapter_url = "capm"
urls = None

text = """ 
    Input a ticker.  Monthly returns for the ticker are computed from the adjusted closing prices provided by
    Yahoo Finance.  Monthly market returns and the monthly risk-free rate are downloaded from 
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  The 
    monthly excess stock returns
    (return minus risk-free rate) are regressed on the monthly excess market returns for the most recent 60
    months.  Hover over the line to see the regression coefficients in the form ret = beta*market + intercept. The 
    beta is used in conjunction with the market risk premium and the risk-free rate to compute the cost of
    equity capital.  The market risk premium is the average market excess return from 1926 to the present from 
    French's data library.  The 
    risk-free rate is the current 3-month Treasury bill yield obtained from 
    [Federal Reserve Economic Data](https://fred.stlouisfed.org/series/DGS3MO).
    """

name = "capm_costequity"

graph = dcc.Loading(dcc.Graph(id=name + "fig"), type="circle")

# table with no column names
tbl = DataTable(
    id=name + "tbl",
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
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
