# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.capm.sml_industries_figtbl import figtbl
from pages.formatting import Layout
from datetime import date

today = date.today().year - 1

title = "Security market line for industry returns"
runtitle = None
chapter = "Capital Asset Pricing Model"
chapter_url = "capm"
urls = None

text = """ 
    Market betas are estimated for value-weighted industry returns using monthly data and the 
    Fama-French 48 industry classification.  Average annual excess returns (risk premia) are plotted
    against betas in blue. The blue line is the regression line showing the best fit between estimated betas
    and empirical risk premia.  The green points are the theoretical risk premia, based on the CAPM, the
    market risk premium over the date range selected, and the estimated betas.  The data is from 
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  
    
    Hover over the points to see the industry names.  The low beta industries are generally noncycical industries
    and the high beta industries are cyclical industries.  The CAPM predicts that cyclical industries should 
    have higher average returns than noncyclical industries, but this is generally not borne out in the data.
    """

name = "capm48"

graph = dcc.Graph(id=name + "fig")

slider = dcc.RangeSlider(
    id=name + "slider",
    min=1970,
    max=today,
    step=1,
    value=[1980, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Select date range", html_for=name + "slider"), slider])
slider = dbc.Row(dbc.Col(slider, width={"size": 6}, className="offset-md-3"))
body = dbc.Container([slider, html.Br(), graph], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + "fig", "figure"), Input(name + "slider", "value")]


@callback(*lst)
def call(*args):
    return figtbl(*args)
