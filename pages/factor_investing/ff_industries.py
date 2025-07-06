# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.factor_investing.ff_industries_figtbl import figtbl
from pages.formatting import Layout
from datetime import date

today = date.today().year

title = "Fama-French model for industries"
runtitle = None
chapter = "Factors"
chapter_url = "factor-investing"
urls = None

text = """ The Fama-French five-factor model is estimated for monthly value-weighted industry returns using the 
             Fama-French 48 industry classification.  Theoretical expected excess returns (risk premia) are sums 
             of factor betas multiplied by factor risk premia and are calculated from the estimated betas and mean 
             factor returns over the specified time period.  Empirical mean excess returns 
             are plotted against theoretical risk
             premia in blue. The blue line is the regression line showing the best fit between the 
             theoretical and empirical 
             means.  If the theory were perfectly true, then the regression line should be the 45 degree line, which 
             is indicated by the green points.  The data is from 
             [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  Hover
             over the points to see the industry names.
             
         """

name = "ff-industries"

slider = dcc.RangeSlider(
    id=name + "slider",
    min=1963,
    max=today,
    step=1,
    value=[1963, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = dbc.Col(
    [dbc.Label("Select date range", html_for=name + "slider"), slider],
    width={"size": 6, "offset": 3},
)
slider = dbc.Row(slider)

graph = dcc.Graph(id=name + "fig")

body = html.Div([slider, graph])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)


@callback(Output(name + "fig", "figure"), Input(name + "slider", "value"))
def call(dates):
    return figtbl(dates)
