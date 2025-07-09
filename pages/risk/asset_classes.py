# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from pages.risk.asset_classes_figtbl import figtbl
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    style_header,
    style_data_conditional,
    css_no_header,
    text_style,
    mybadge,
    style_data,
    lightblue
)
from datetime import date

today = date.today().year

title = "Correlations of stocks or funds"
runtitle = None
chapter = "Risk and Return"
chapter_url = "risk"

urls = None

text = """ 
    Monthly returns are computed for the specified tickers over the specified date range from the adjusted closing
    prices provided by Yahoo Finance.  The correlation matrix of the returns is presented.  The default tickers are
    
    * SPY = SPDR S&P 500 ETF
    * IWM = iShares Russell 2000 ETF
    * VWO = Vanguard FTSE Emerging Markets ETF
    * IEF = iShares 7-10 Year Treasury Bond ETF
    * LQD = iShares iBoxx Investment Grade Corporate Bond ETF
    * IYR = iShares US Real Estate ETF
    * GLD = SPDR Gold Trust ETF
    * UUP = Invesco U.S. Dollar Bullish ETF   
    
    The actual date range used is the largest within the specified range for which all tickers were traded.  It is
    stated below the date range slider.
"""

name = "asset-classes"


slider= dcc.RangeSlider(
    id=name+"dates",
    min=1970,
    max=today,
    step=1,
    value=[1990, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Select date range"), slider])


Drop = dcc.Dropdown(
    [i for i in range(2, 13)],
    placeholder="Number of assets",
    value=8,
    id=name + "Num",
    style={"backgroundColor": lightblue}
)

Tickers = DataTable(
    id=name + "tickers",
    columns=[{"name": "Tickers", "id": name + "t", "editable": True}],
    css=css_no_header,
    style_data=style_data,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
    data=[
        {name + "t": "spy"},
        {name + "t": "iwm"},
        {name + "t": "vwo"},
        {name + "t": "lqd"},
        {name + "t": "ief"},
        {name + "t": "iyr"},
        {name + "t": "gld"},
        {name + "t": "uup"},
    ]
)
Tickers = dcc.Loading(Tickers, type="circle")

text1 = """
    Run
    """
Btn = dbc.Button(
    text1,
    id=name + 'btn',
    n_clicks=0,
    color="primary",
    className="me-1",
)



text2 = html.Div(
    """ 
    Specify how many tickers you wish to use, and edit the list of tickers.   
    """
)


left = dbc.Col(
    [
        text2,
        html.Br(),
        dbc.Label("Number of Tickers"),
        Drop,
        html.Br(),
        dbc.Label("Enter Tickers"),
        Tickers
    ],
    xs=12, sm=12, md=5, lg=5, className="mb-2 offset-md-1"
)


mindate_label = html.Div("Actual date range:")
mindate = dcc.Loading(html.Div(id=name+"mindate", style=text_style), type="circle")
mindate_label = dbc.Col(mindate_label, xs=12, sm=6, md=6, lg=6, className="mb-2")
mindate = dbc.Col(mindate, xs=12, sm=6, md=6, lg=6, className="mb-2")
daterow = dbc.Row([mindate_label, mindate], className="gx-1")


right = dbc.Col(
    [
        slider,
        html.Br(),
        daterow,
        html.Br(),
        html.Br(),
        Btn
    ],
    xs=12, sm=12, md=4, lg=4, className="mb-2 offset-md-1"
)

row = dbc.Row([left, right], align="top", className="gx-1")

badge = html.H5(dbc.Badge("Correlation Matrix", className="ms-1"))
badge = mybadge("Correlation Matrix")
badge = dbc.Col(badge, width={"size": 4, "offset": 5})
badge2 = dbc.Row(badge)
badge2 = dbc.Row(dbc.Col(badge2, width=dict(size=6, offset=3)))

Corr = DataTable(
    id=name + "corr",
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
Corr = dcc.Loading(id=name + "loading3", children=[Corr], type="circle")

body = dbc.Container([
    row,
    html.Hr(),
    badge2,
    html.Br(),
    Corr
], fluid=True, className="px-1")

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
    Output(name + "corr", "data"),
    Output(name + "tickers", "data"),
    Output(name + "mindate", "children"),
    Input(name + "dates", "value"),
    Input(name + "Num", "value"),
    Input(name + "tickers", "data_timestamp"),
    State(name + "tickers", "data"),
    Input(name + 'btn', 'n_clicks')
)
def call(dates, N, time_stamp, trows, n_clicks):
    M = len(trows)
    if N > M:
        trows += [{name + "t": None} for i in range(N - M)]
        return None, trows, None
    else:
        trows = trows[:N]
        tickers = [list(d.values())[0] for d in trows]
        if tickers == [t for t in tickers if t]:
            tbl, mindate = figtbl(dates, tickers)
            return tbl, trows, mindate
        else:
            return None, trows, None


