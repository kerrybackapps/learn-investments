# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback, State, callback_context
import dash_bootstrap_components as dbc
from pages.risk.returns_figtbl import figtbl 
from pages.formatting import Layout, style_data, css_no_header, style_data_conditional, myinput
from datetime import date
from dash.dash_table import DataTable, FormatTemplate
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

today = date.today().year - 1

percentage = FormatTemplate.percentage(1)

title = "Stock market returns"
runtitle = "Stock Returns"
chapter = "Risk and Return"
chapter_url = "risk"

urls = {
    "Python notebook": "https://github.com/bbcx-investments/notebooks/blob/dd47811d4b5f3153721553e5b9263d1ed2c1b8ff/risk/returns.ipynb"
}

text = """ The distribution of annual returns is presented over the date range specified for the aggregate U.S. stock 
             market or for individual tickers.  The market return data is from 
             [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
             and begins in 1927.  Returns
             for individual tickers are computed from the dividend and split-adjusted 
             closing prices
             provided by Yahoo Finance.  That data begins in 1970.  The date range for a ticker will be less
             than that specified if it was not traded at all dates in the range. """

name = "returns"

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
    interval=1000, 
    n_intervals=0,
    max_intervals=1 
)

inpt_col = dbc.Col(inpt, xs=12, sm=12, md=5, lg=5, className="mb-2") 
slider_col = dbc.Col([dbc.Label("Date Range", html_for=name + "slider"), slider], xs=12, sm=12, md=7, lg=7, className="mb-2")

graph_std = dcc.Loading(
    id=name + "loading1", children=[dcc.Graph(id=name + "fig1")], type="circle"
)
graph_log = dcc.Loading(
    id=name + "loading2", children=[dcc.Graph(id=name + "fig2")], type="circle"
)
graph_box = dcc.Loading(
    id=name + "loading3", children=[dcc.Graph(id=name + "fig3")], type="circle"
)
graph_hist = dcc.Loading(
    id=name + "loading4", children=[dcc.Graph(id=name + "fig4")], type="circle"
)
graph_rets = dcc.Loading(
    id=name + "loading5", children=[dcc.Graph(id=name + "fig5")], type="circle"
)

graph_std = dbc.Col(graph_std, xs=12, sm=12, md=4, lg=4, className="mb-2")
graph_log = dbc.Col(graph_log, xs=12, sm=12, md=4, lg=4, className="mb-2")
graph_box = dbc.Col(graph_box, xs=12, sm=6, md=3, lg=3, className="mb-2")
graph_hist = dbc.Col(graph_hist, xs=12, sm=12, md=4, lg=4, className="mb-2")
graph_rets = dbc.Col(graph_rets, xs=12, sm=12, md=6, lg=6, className="mb-2")

columns = [
    dict(name=c, id=name + c, type="numeric", format=percentage)
    for c in ["Statistic", "Return"]
]
tbl = DataTable(
    id=name + "tbl",
    columns=columns,
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl = dcc.Loading(id=name + "loading6", children=[tbl], type="circle")
tbl = dbc.Col(tbl, xs=12, sm=6, md=3, lg=3, className="mb-2")

row1 = dbc.Row([slider_col, inpt_col], align="center", className="gx-1") 
row2 = dbc.Row([tbl, graph_rets, graph_box], align="center", className="gx-1")
row3 = dbc.Row([graph_hist, graph_std, graph_log], align="center", className="gx-1")
body = dbc.Container([row1, html.Hr(), row2, row3, ticker_interval], fluid=True, className="px-1") 

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
    Output(name + f, "figure") for f in ["fig1", "fig2", "fig3", "fig4", "fig5"]
] + [Output(name + "tbl", "data")]

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
    empty_data = []

    if not ctx.triggered and n_intervals == 0: 
        raise PreventUpdate

    processed_ticker_input = ticker_value_state.strip() if ticker_value_state else ""

    mode_for_figtbl = ""
    ticker_for_figtbl = None

    if not processed_ticker_input: 
        if triggered_id == (name + "-ticker-input-interval") or triggered_id == (name + "slider"):
            return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_data
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
        fig1, fig2, fig3, fig4, fig5, tbl_data = figtbl(date_range, mode_for_figtbl, ticker_for_figtbl)
        tbl_data.columns = [name + c for c in tbl_data.columns]
        return fig1, fig2, fig3, fig4, fig5, tbl_data.to_dict("records")
    except Exception as e:
        print(f"Error in figtbl call (mode: {mode_for_figtbl}, ticker: {ticker_for_figtbl}): {e}")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_data
