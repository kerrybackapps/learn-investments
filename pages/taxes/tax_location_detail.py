# -*- coding: utf-8 -*-
"""
Created on Tue May 10 09:31:30 2022

@author: Kevin
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

from pages.taxes.tax_location_detail_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Asset location with taxes"
runtitle = "Asset location with taxes"
chapter = "Topics"
chapter_url = "topics"
urls = {"Python notebook": None}
text = """ Investment in a dividend-paying stock and/or a taxable coupon bond is made in a brokerage account, a 401(k) account, or a Roth IRA account.  The future after-tax value of an initial after-tax dollar of investment is calculated, and each sub-account value is displayed.  The omitted weight is Roth:Bonds.   Withdrawal from the account occurs at time T.  The initial tax rate for ordinary income is assumed to prevail until time T-1, at which point it changes to the ending tax rate.  The rates of return (dividend-yield, stock capital gain, and bond rate) denote the pre-tax per period rate of return.  Dividends and interest payments are assumed to be reinvested at the same rate."""

name = "tax_location_detail"

inputs = [name + "input" + str(i) for i in range(13)]
slider1 = Slider(
    "Stock dividend yield",
    mn=0,
    mx=15,
    step=0.1,
    value=2,
    tick=3,
    name=inputs[0],
    kind="pct",
)
slider2 = Slider(
    "Stock capital gain",
    mn=0,
    mx=15,
    step=0.1,
    value=4,
    tick=3,
    name=inputs[1],
    kind="pct",
)
slider3 = Slider(
    "Bond rate of return",
    mn=0,
    mx=15,
    step=0.1,
    value=3,
    tick=3,
    name=inputs[2],
    kind="pct",
)
slider4 = Slider(
    "Initial tax rate on ordinary income",
    mn=0,
    mx=40,
    step=1,
    value=35,
    tick=10,
    name=inputs[3],
    kind="tip",
)
slider5 = Slider(
    "Ending tax rate on ordinary income",
    mn=0,
    mx=40,
    step=1,
    value=35,
    tick=10,
    name=inputs[4],
    kind="tip",
)
slider6 = Slider(
    "Tax rate on dividends",
    mn=0,
    mx=40,
    step=1,
    value=15,
    tick=10,
    name=inputs[5],
    kind="tip",
)
slider7 = Slider(
    "Tax rate on capital gains",
    mn=0,
    mx=40,
    step=1,
    value=15,
    tick=10,
    name=inputs[6],
    kind="tip",
)
slider8 = Slider(
    "Years saving", mn=1, mx=50, step=1, value=30, tick=None, name=inputs[7], kind="tip"
)

slider9 = Slider(
    "Portfolio weight: Brokerage-Stock",
    mn=0,
    mx=100,
    step=5,
    value=25,
    tick=10,
    name=inputs[8],
    kind="tip",
)
slider10 = Slider(
    "Portfolio weight: Brokerage-Bond",
    mn=0,
    mx=100,
    step=5,
    value=25,
    tick=10,
    name=inputs[9],
    kind="tip",
)
slider11 = Slider(
    "Portfolio weight: 401k-Stock",
    mn=0,
    mx=100,
    step=5,
    value=25,
    tick=10,
    name=inputs[10],
    kind="tip",
)
slider12 = Slider(
    "Portfolio weight: 401k-Bond",
    mn=0,
    mx=100,
    step=5,
    value=25,
    tick=10,
    name=inputs[11],
    kind="tip",
)
slider13 = Slider(
    "Portfolio weight: Roth-Stock",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[12],
    kind="tip",
)

graph = dcc.Graph(id=name + "fig")

# Option 1
# left = dbc.Col([slider1,slider2,slider3,slider4,slider5,slider6,slider7,slider8,slider9,slider10,slider11,slider12,slider13], md=4)
# right = dbc.Col([graph], md=8)
# body = dbc.Row([left,right], align="center")


# Option 2
left = dbc.Col([slider1, slider2, slider3,], xs=12, sm=12, md=4, lg=4, className="mb-2")
mid = dbc.Col([slider4, slider5, slider6], xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col([slider7, slider8], xs=12, sm=12, md=4, lg=4, className="mb-2")
row1 = dbc.Row([left, mid, right], align="top", className="gx-1")

left = dbc.Col(
    [
        slider9,
        html.Br(),
        slider10,
        html.Br(),
        slider11,
        html.Br(),
        slider12,
        html.Br(),
        slider13,
    ],
    xs=12, sm=12, md=4, lg=4, className="mb-2",
)
right = dbc.Col([graph], xs=12, sm=12, md=8, lg=8, className="mb-2")
row2 = dbc.Row([left, right], align="center", className="gx-1")
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
lst = [Output(name + "fig", "figure")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    fig = figtbl(*args)
    return fig
