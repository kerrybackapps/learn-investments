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

from pages.taxes.tax_location_compare_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Comparison of asset locations with taxes"
runtitle = "Comparison of asset locations with taxes"
chapter = "Topics"
chapter_url = "topics"
urls = {"Python notebook": None}
text = """ 
        Investment in a dividend-paying stock and/or a taxable coupon bond is made in a brokerage account, a 401(k) account, or a Roth IRA account. The future after-tax value of an initial after-tax dollar of investment is calculated for multiple asset location allocations. The omitted weight is Roth:Bonds. To compare only two portfolios, set all of portfolio #3 weights to zero. Withdrawal from the account occurs at time T.  The initial tax rate for ordinary income is assumed to prevail until time T-1, at which point it changes to the ending tax rate. The rates of return (dividend-yield, stock capital gain, and bond rate) denote the pre-tax per period rate of return.  Dividends and interest payments are assumed to be reinvested at the same rate.
      """

name = "tax_location_compare"

inputs = [name + "input" + str(i) for i in range(23)]
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
    "Bond rate of returns",
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
    value=20,
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
    "Portfolio #1 weight: Brokerage-Stock",
    mn=0,
    mx=100,
    step=5,
    value=50,
    tick=10,
    name=inputs[8],
    kind="tip",
)
slider10 = Slider(
    "Portfolio #1 weight: Brokerage-Bond",
    mn=0,
    mx=100,
    step=5,
    value=50,
    tick=10,
    name=inputs[9],
    kind="tip",
)
slider11 = Slider(
    "Portfolio #1 weight: 401k-Stock",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[10],
    kind="tip",
)
slider12 = Slider(
    "Portfolio #1 weight: 401k-Bond",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[11],
    kind="tip",
)
slider13 = Slider(
    "Portfolio #1 weight: Roth-Stock",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[12],
    kind="tip",
)


slider14 = Slider(
    "Portfolio #2 weight: Brokerage-Stock",
    mn=0,
    mx=100,
    step=5,
    value=50,
    tick=10,
    name=inputs[13],
    kind="tip",
)
slider15 = Slider(
    "Portfolio #2 weight: Brokerage-Bond",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[14],
    kind="tip",
)
slider16 = Slider(
    "Portfolio #2 weight: 401k-Stock",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[15],
    kind="tip",
)
slider17 = Slider(
    "Portfolio #2 weight: 401k-Bond",
    mn=0,
    mx=100,
    step=5,
    value=50,
    tick=10,
    name=inputs[16],
    kind="tip",
)
slider18 = Slider(
    "Portfolio #2 weight: Roth-Stock",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[17],
    kind="tip",
)

slider19 = Slider(
    "Portfolio #3 weight: Brokerage-Stock",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[18],
    kind="tip",
)
slider20 = Slider(
    "Portfolio #3 weight: Brokerage-Bond",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[19],
    kind="tip",
)
slider21 = Slider(
    "Portfolio #3 weight: 401k-Stock",
    mn=0,
    mx=100,
    step=5,
    value=50,
    tick=10,
    name=inputs[20],
    kind="tip",
)
slider22 = Slider(
    "Portfolio #3 weight: 401k-Bond",
    mn=0,
    mx=100,
    step=5,
    value=50,
    tick=10,
    name=inputs[21],
    kind="tip",
)
slider23 = Slider(
    "Portfolio #3 weight: Roth-Stock",
    mn=0,
    mx=100,
    step=5,
    value=0,
    tick=10,
    name=inputs[22],
    kind="tip",
)


graph = dcc.Graph(id=name + "fig")


# Option 2
# left1 = dbc.Col([slider1,slider2,slider3,slider8], md=6)
# right1= dbc.Col([slider4,slider5,slider6,slider7], md=6)
# row1  = dbc.Row([left1, right1])

left2 = dbc.Col([slider9, slider10, slider11, slider12, slider13], md=4)
mid2 = dbc.Col([slider14, slider15, slider16, slider17, slider18], md=4)
right2 = dbc.Col([slider19, slider20, slider21, slider22, slider23], md=4)
row2 = dbc.Row([left2, mid2, right2])


col = dbc.Col(
    [slider1, slider2, slider3, slider4, slider5, slider6, slider7, slider8], md=4
)
row3 = dbc.Row([col, dbc.Col(graph, md=8)], align="center")

body = html.Div([row2, html.Br(), row3, html.Br()])  # , row1,html.Br()])


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
