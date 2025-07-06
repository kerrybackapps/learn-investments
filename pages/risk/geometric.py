# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:31:00 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State, callback_context
from pages.risk.geometric_figtbl import figtbl
from pages.formatting import Layout, text_style, myinput
from datetime import date
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

today = date.today().year - 1

title = "Geometric average returns"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "geometric"

text = """
    Given
    returns $r_1,\\ldots, r_n$ over $n$ periods, the geometric average return is defined as
    $r_{\\text{geom}} = [(1+r_1) \\cdots (1+r_n)]^{1/n}-1$.  Equivalently, $(1+r_{\\text{geom}})^n = (1+r_1) \\cdots (1+r_n)$.  Thus,
    $r_{\\text{geom}}$
    is the return such that, if it were earned each period, the
    total return over the $n$ periods would be the same as with the actual returns $r_1, \\ldots, r_n$.  The
    geometric average is always smaller than the arithmetic average $(1/n)\\sum_{i=1}^n r_i$, and the difference is
    greater when volatility is higher.  In the context of annual returns, the geometric average return is also known
    as the compound annual growth rate (CAGR).

    Annual returns are presented for either the aggregate U.S. stock market or for individual tickers, over the date range
    specified.  The arithmetic and geometric average returns
    are reported on the right along with the standard deviation.  The
    left figure shows the returns, and the right figure shows the accumulation
    $(1+r_1)\\cdots(1+r_i)$ through year $i$ for each $i\\le n$, where $n$ is the number of years in the specified
    date range.  The figure also shows what the accumulation would have been
    had either the arithmetic average or the geometric average been earned each period.

    The market return data is from
    [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
    and begins in 1927.  Returns
    for individual tickers are computed from the dividend and split-adjusted
    closing prices
    provided by Yahoo Finance.  That data begins in 1970.
    """

inpt = myinput(
    id=name + "ticker", placeholder="Enter MARKET for U.S. market or a ticker"
)
slider = dcc.RangeSlider(
    id=name + "slider",
    min=1927,
    max=today,
    step=1,
    value=[1970, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)

ticker_interval = dcc.Interval(
    id=name + "-ticker-input-interval",
    interval=1500,
    n_intervals=0,
    max_intervals=1
)

inpt_col = dbc.Col(inpt, md=6)
slider_col = dbc.Col([dbc.Label("Date Range", html_for=name + "slider"), slider], md=6)

label0 = html.Div("Standard deviation")
label1 = html.Div("Arithmetic average")
label2 = html.Div("Geometric average")
string0 = html.Div(id=name+"string0", style=text_style)
string1 = html.Div(id=name+"string1", style=text_style)
string2 = html.Div(id=name+"string2", style=text_style)

stats_col1 = dbc.Col([label2, label1, label0], md=8)
stats_col2 = dbc.Col([string2, string1, string0], md=4)
stats_display_row = dbc.Row([stats_col1, stats_col2])
stats_display_col = dbc.Col(stats_display_row, width=dict(size=3, offset=1))

input_slider_row = dbc.Row([slider_col, inpt_col], align="center")
input_area_col = dbc.Col(input_slider_row, md=8)

row1 = dbc.Row([input_area_col, stats_display_col], align="center")

graph_col_left = dbc.Col(dcc.Loading(dcc.Graph(id=name+"fig1"), type="circle"), md=6)
graph_col_right = dbc.Col(dcc.Loading(dcc.Graph(id=name+"fig2"), type="circle"), md=6)

row2 = dbc.Row([graph_col_left, graph_col_right], align="top")

body = html.Div([row1, html.Br(), row2, ticker_interval])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [
    Output(name+"fig1", "figure"),
    Output(name+"fig2", "figure"),
    Output(name+"string0", "children"),
    Output(name+"string1", "children"),
    Output(name+"string2", "children")
]

main_callback_inputs = [
    Input(name + "slider", "value"),
    Input(name + "-ticker-input-interval", "n_intervals"),
    State(name + "ticker", "value"),
]

@callback(
    Output(name + "-ticker-input-interval", "n_intervals"),
    Input(name + "ticker", "value"),
    prevent_initial_call=True
)
def reset_ticker_interval(_ticker_value):
    return 0

@callback(
    outputs,
    main_callback_inputs
)
def call(date_range, n_intervals, ticker_value_state):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'No trigger'

    empty_fig = go.Figure()
    empty_str = ""
    empty_outputs_tuple = (empty_fig, empty_fig, empty_str, empty_str, empty_str)

    if not ctx.triggered and n_intervals == 0:
        raise PreventUpdate

    processed_ticker_input = ticker_value_state.strip() if ticker_value_state else ""

    mode_for_figtbl = ""
    ticker_for_figtbl = None

    if not processed_ticker_input:
        if triggered_id == (name + "-ticker-input-interval") or triggered_id == (name + "slider"):
            return empty_outputs_tuple
        raise PreventUpdate

    if processed_ticker_input.lower() == "market":
        mode_for_figtbl = "Market"
        ticker_for_figtbl = None
    else:
        mode_for_figtbl = "Ticker"
        ticker_for_figtbl = processed_ticker_input

    should_call_figtbl = False
    if triggered_id == (name + "slider"):
        should_call_figtbl = True
    elif triggered_id == (name + "-ticker-input-interval") and n_intervals > 0 :
        should_call_figtbl = True

    if not should_call_figtbl:
        raise PreventUpdate

    try:
        return figtbl(date_range, mode_for_figtbl, ticker_for_figtbl)
    except Exception as e:
        print(f"Error in figtbl call (file: geometric.py, mode: {mode_for_figtbl}, ticker: {ticker_for_figtbl}): {e}")
        return empty_outputs_tuple
