# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.factor_investing.ff_characteristics_figtbl import figtbl, chars
from datetime import date
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    style_data_conditional,
    style_header,
    lightblue
)

today = date.today().year

title = "Fama-French model for two-way sorts"
runtitle = None
chapter = "Factors"
chapter_url = "factor-investing"
urls = None

text = """ 
    Monthly returns are computed for 25 value-weighted portfolios formed by intersecting quintile sorts 
    on market equity and another
    characteristic.  The Fama-French five-factor model is estimated for each of the 25 portfolios.  All data is from
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  Definitions
    of the characteristics and 
    details of the portfolio constructions can be found there.  The alphas in the left table are the intercepts in 
    the regression of excess returns 
    on the five factors, and the $t$ statistics in the right table are the $t$ statistics of the alphas.  If the model were perfectly
    valid, then alphas should be zero, so large $t$ statistics of either sign reject the model. 
    """

name = "ff-characteristics"

drop = dcc.Dropdown(chars, placeholder="Select a characteristic", id=name + "char", style={"backgroundColor": lightblue})
drop = html.Div([dbc.Label("Characteristic"), drop])

slider = dcc.RangeSlider(
    id=name + "dates",
    min=1963,
    max=today,
    step=1,
    value=[1963, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Date Range"), slider])

alpha_tbl = dcc.Graph(id=name + 'alpha-tbl')

tstat_tbl = dcc.Graph(id=name + 'tstat-tbl')

alpha_tbl = dcc.Loading(alpha_tbl, type="circle")
tstat_tbl = dcc.Loading(tstat_tbl, type="circle")

left = dbc.Col(drop, md=6)
right = dbc.Col(slider, md=6)
row1 = dbc.Row([left, right], align="center")

left = dbc.Col(
    [
        dbc.Label('Alphas (annualized)'),
        alpha_tbl,
    ],
    md=6
)

right = dbc.Col(
    [
        dbc.Label('t statistics'),
        tstat_tbl,
    ],
    md=6
)
row2 = dbc.Row([left, right], align="top")

body = html.Div([row1, html.Hr(), row2])
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
    Output(name + 'alpha-tbl', 'figure'),
    Output(name + 'tstat-tbl', 'figure'),
    Input(name + "char", "value"),
    Input(name + "dates", "value"),
    prevent_initial_call=True
)
def call(char, dates):
    return figtbl(char, dates)
