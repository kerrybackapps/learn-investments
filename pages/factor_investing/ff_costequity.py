# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 16:46:49 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.formatting import Layout, style_data, style_header, style_data_conditional, myinput
from pages.factor_investing.ff_costequity_figtbl import figtbl

title = "Fama-French cost of equity calculator"
runtitle = None
chapter = "Factors"
chapter_url = "factor-investing"
urls = None

text = """ The Fama-French factors and the monthly risk-free rate are downloaded from 
              [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  Monthly stock returns for the
              ticker input below are computed from data provided by Yahoo Finance.  The monthly excess stock returns
              (return minus risk-free rate) are regressed on the factors for the most recent 60
              months.  The betas are used in conjunction with the factor risk premia and the risk-free rate to compute the cost of
              equity capital.  The market, SMB, and HML risk premia are the averages from 1926 to the present from French's data library.  The 
              RMW and CMA risk premia are the averages from 1964 to the present from French's data library.
              The risk-free rate is the current 3-month Treasury bill yield obtained from 
              [Federal Reserve Economic Data](https://fred.stlouisfed.org/series/DGS3MO).
              """

name = "ff-costequity"

inpt = myinput(id=name + "ticker", placeholder="Enter a ticker")
inpt = dbc.Col(inpt, width={"size": 2}, className="offset-md-5")
inpt = dbc.Row(inpt)

columns = ["Factor", "Factor Risk Premium", "Beta", "Risk Premium"]
tbl = DataTable(
    id=name + "tbl",
    columns=[{"name": c, "id": name + c} for c in columns],
    style_data=style_data,
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl = dbc.Col(tbl, width={"size": 8}, className="offset-md-2")
tbl = dcc.Loading(id=name + "loading", children=[tbl], type="circle")

body = dbc.Container([inpt, html.Br(), html.Br(), tbl], fluid=True, className="px-1")

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
    Output(name + "tbl", "data"),
    Input(name + "ticker", "value"),
    prevent_initial_call=True,
)
def call(ticker):
    return figtbl(ticker)
