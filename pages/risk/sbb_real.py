# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.risk.sbb_real_figtbl import figtbl
from pages.formatting import Layout, style_data, style_header, style_data_conditional
from datetime import date

today = date.today().year - 1
from dash.dash_table import DataTable, FormatTemplate

percentage = FormatTemplate.percentage(1)

title = "Real stock, bond, and gold returns"
runtitle = None
chapter = "Risk and Return"
chapter_url = "risk"

urls = None

text = """ 
        Annual inflation-adjusted (real) returns of the S&P 500, corporate
           bonds, Treasury bonds, Treasury bills, and gold are presented.  The nominal gold return is the 
        percent change in the London fixing, which is obtained 
        from [Nasdaq Data Link](https://data.nasdaq.com/data/LBMA/GOLD-gold-price-london-fixing). The other
        nominal return data is provided by 
        [Aswath Damodaran](https://pages.stern.nyu.edu/~adamodar/).  The returns are adjusted for inflation
        based on the percent change in the
        U.S. All-Urban CPI.  The CPI data is from [Federal Reserve
        Economic Data](https://fred.stlouisfed.org/series/CPIAUCSL).
"""

name = "sbbi-real"

slider = dcc.RangeSlider(
    id=name + "slider",
    min=1968,
    max=today,
    step=1,
    value=[1968, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = dbc.Col(
    [dbc.Label("Date Range", html_for=name + "slider"), slider],
    xs=12, sm=12, md=6, lg=6, offset=3, className="mb-2"
)

graph_std = dbc.Col(dcc.Graph(id=name + "fig1"), xs=12, sm=12, md=6, lg=6, className="mb-2")
graph_log = dbc.Col(dcc.Graph(id=name + "fig2"), xs=12, sm=12, md=6, lg=6, className="mb-2")
graph_box = dbc.Col(dcc.Graph(id=name + "fig3"), xs=12, sm=12, md=6, lg=6, className="mb-2")

columns = ["", "S&P 500", "Gold", "Corporates", "Treasuries", "TBills"]
columns = [
    dict(name=c, id=name + c, type="numeric", format=percentage) for c in columns
]
tbl = DataTable(
    id=name + "tbl",
    columns=columns,
    style_data=style_data,
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl = dbc.Col(tbl, xs=12, sm=12, md=6, lg=6, className="mb-2")

row1 = dbc.Row([slider])
row2 = dbc.Row([tbl, graph_box], align="top", className="gx-1")
row3 = dbc.Row([graph_std, graph_log], align="center", className="gx-1")
body = dbc.Container([row1, html.Br(), html.Hr(), row2, html.Br(), row3], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
outputs = [Output(name + f, "figure") for f in ["fig1", "fig2", "fig3"]] + [
    Output(name + "tbl", "data")
]
inputs = [Input(name + "slider", "value")]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(name, *args)

