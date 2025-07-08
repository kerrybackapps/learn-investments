# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.borrowing_saving.inflation_figtbl import figtbl
from pages.formatting import Slider, Layout, text_style
from datetime import datetime

today = datetime.today()
today = today.year - 1

title = "Inflation and real returns"
runtitle = "Inflation"
chapter = "Borrowing and Saving"
chapter_url = "borrowing-saving"

urls = {"Python notebook": None}

text = """ The inflation rate shown in the figure on the left is based on the U.S. "Consumer Price Index 
           for All Urban Consumers" and is from [Federal Reserve
           Economic Data](https://fred.stlouisfed.org/series/CPIAUCSL).  Given a nominal rate of 
           return $y$ and the inflation rate $i$, the real rate of return is $r$ defined 
           by $(1+r)(1+i)=1+y$.  In other words, $r = (1+y)/(1+i)-1$.  This is approximately $y-i$.  The figure 
           on the right shows the
           compound U.S. stock market return in nominal terms (from 
           [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html))
           and the compound real U.S. stock market return, which is the return in constant dollars. The
           compound return in constant dollars equals
           the compound nominal return divided by the growth in the CPI.
           """

name = "inflation"

dates = dcc.RangeSlider(
    id=name + "dates",
    min=1950,
    max=today,
    step=1,
    value=[1970, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)

dates = html.Div([dbc.Label("Select date range", html_for=name + "dates"), dates])

nominal = html.Div(id=name + "nominal", style=text_style)
label = dbc.Label("Average nominal return", html_for=name + "nominal")
nominal = dbc.Row([dbc.Col(label, md=6), dbc.Col(nominal, md=6)], align="center")

real = html.Div(id=name + "real", style=text_style)
label = dbc.Label("Average real return", html_for=name + "real")
real = dbc.Row([dbc.Col(label, md=6), dbc.Col(real, md=6)], align="center")

infl = html.Div(id=name + "infl", style=text_style)
label = dbc.Label("Average annual inflation", html_for=name + "infl")
infl = dbc.Row([dbc.Col(label, md=6), dbc.Col(infl, md=6)], align="center")


fig1 = dbc.Col(dcc.Graph(id=name + "fig1"), xs=12, sm=12, md=6, lg=6, className="mb-2")
fig2 = dbc.Col(dcc.Graph(id=name + "fig2"), xs=12, sm=12, md=6, lg=6, className="mb-2")

left = dbc.Col([dates], xs=12, sm=12, md=6, lg=6, className="mb-2")
right = dbc.Col([nominal, infl, real], xs=12, sm=12, md=4, lg=4, className="mb-2 offset-md-2")
row1 = dbc.Row([left, right], align="top", className="gx-1")
row2 = dbc.Row([fig1, fig2], align="top", className="gx-1")

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
outputs = [Output(name + f, "figure") for f in ["fig1", "fig2"]] + [
    Output(name + s, "children") for s in ["nominal", "infl", "real"]
]
inputs = [Input(name + s, "value") for s in ["dates"]]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)
