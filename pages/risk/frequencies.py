# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback, State, callback_context # Added State, callback_context
import dash_bootstrap_components as dbc
from pages.risk.frequencies_figtbl import figtbl
from pages.formatting import Layout, style_data, style_header, style_data_conditional, myinput
from datetime import date
from dash.dash_table import DataTable, FormatTemplate
from dash.exceptions import PreventUpdate # Added PreventUpdate
import plotly.graph_objects as go # Added go

today = date.today().year - 1
percentage = FormatTemplate.percentage(2)

title = "Returns at different frequencies"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "frequencies"

text = """ 
    The distributions of daily, monthly, and annual returns are described over the date range specified for the 
    aggregate U.S. stock 
    market or for individual tickers.  Daily returns are typically highly leptokurtic, meaning that there is a large
    number of extreme outliers, which can be seen in a boxplot.  Monthly returns are typically also 
    somewhat leptokurtic.  Hover over the dots outside the fences in the boxplots to see the dates and magnitudes of
    outlier returns.  
    
    The leptokurtic nature of daily and monthly returns can also be seen from the density plots at 
    the bottom of the page.  The normal curves in those figures are normal distributions with the same means and 
    standard deviations as the actual returns, extending three standard deviations on each side of the mean, which 
    should encompass 99.7% of the data, if the distributions were actually normal.  The wide "tails" and high narrow
    peaks of the daily and monthly distributions reflect the large number of daily and monthly return outliers.
    
    The market return data is from 
    [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
    and begins in 1927.  Returns
    for individual tickers are computed from the dividend and split-adjusted 
    closing prices
    provided by Yahoo Finance.  That data begins in 1970.  The date range for a ticker will be less
    than that specified if it was not traded at all dates in the range. """

# RadioButton removed
inpt = myinput(
    id=name + "ticker", placeholder="Enter MARKET for U.S. market or a ticker" # Updated placeholder
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

# Added Interval component for debounce mechanism
ticker_interval = dcc.Interval(
    id=name + "-ticker-input-interval",
    interval=1500,  # 1.5 second delay
    n_intervals=0,
    max_intervals=1 
)

# Adjusted layout columns
inpt_col = dbc.Col(inpt, xs=12, sm=12, md=5, lg=5, className="mb-2")
slider_col = dbc.Col([dbc.Label("Date Range", html_for=name + "slider"), slider], xs=12, sm=12, md=7, lg=7, className="mb-2")

columns = ["", "Daily", "Monthly", "Annual"]
columns = [
    dict(name=c, id=name + c, type="numeric", format=percentage) for c in columns
]
tbl = DataTable(
    id=name + "tbl",
    columns=columns,
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl = dbc.Col(dcc.Loading(tbl, type="circle"), xs=12, sm=12, md=6, lg=6, className="mb-2")

fig = dbc.Col(dcc.Loading(dcc.Graph(id=name + "fig"), type="circle"), xs=12, sm=12, md=6, lg=6, className="mb-2")

row1 = dbc.Row([slider_col, inpt_col], align="center", className="gx-1")
row2 = dbc.Row([tbl, fig], align="top", className="gx-1")

figd = dbc.Col(dcc.Loading(dcc.Graph(id=name + "figd"), type="circle"), xs=12, sm=12, md=4, lg=4, className="mb-2")
figm = dbc.Col(dcc.Loading(dcc.Graph(id=name + "figm"), type="circle"), xs=12, sm=12, md=4, lg=4, className="mb-2")
figa = dbc.Col(dcc.Loading(dcc.Graph(id=name + "figa"), type="circle"), xs=12, sm=12, md=4, lg=4, className="mb-2")
row3 = dbc.Row([figd, figm, figa], className="gx-1")

body = dbc.Container([row1, html.Hr(), html.Br(), row2, html.Br(), row3, ticker_interval], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

# Define outputs
outputs = [
    Output(name+"tbl", "data"),
    Output(name+"fig", "figure"),
    Output(name+"figd", "figure"),
    Output(name+"figm", "figure"),
    Output(name+"figa", "figure")
]

# Define inputs for main callback (radio input removed, interval input added, ticker input becomes State)
main_callback_inputs = [
    Input(name + "slider", "value"), 
    Input(name + "-ticker-input-interval", "n_intervals"), 
    State(name + "ticker", "value"), 
]

# Callback to reset the interval timer when ticker input changes
@callback(
    Output(name + "-ticker-input-interval", "n_intervals"),
    Input(name + "ticker", "value"), 
    prevent_initial_call=True
)
def reset_ticker_interval(_ticker_value):
    return 0

# Main callback, refactored
@callback(
    outputs,
    main_callback_inputs
)
def call(date_range, n_intervals, ticker_value_state): 
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'No trigger'
    
    empty_fig = go.Figure()
    # Corrected structure for empty data based on defined columns:
    # columns = ["", "Daily", "Monthly", "Annual"]
    # ids = [name + c for c in columns] -> ["frequencies", "frequenciesDaily", "frequenciesMonthly", "frequenciesAnnual"]
    empty_data_table = [{name + c: "" for c in ["", "Daily", "Monthly", "Annual"]}]


    empty_figs_tuple = (empty_data_table, empty_fig, empty_fig, empty_fig, empty_fig)


    if not ctx.triggered and n_intervals == 0: 
        raise PreventUpdate

    processed_ticker_input = ticker_value_state.strip() if ticker_value_state else ""

    mode_for_figtbl = ""
    ticker_for_figtbl = None

    if not processed_ticker_input: 
        if triggered_id == (name + "-ticker-input-interval") or triggered_id == (name + "slider"):
            return empty_figs_tuple
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
        # figtbl in frequencies_figtbl.py needs to be called with (name, dates, mode, ticker)
        # The 'name' argument was implicitly passed by original figtbl(*args) structure.
        # Explicitly pass it now.
        return figtbl(name, date_range, mode_for_figtbl, ticker_for_figtbl)
    except Exception as e:
        print(f"Error in figtbl call (file: frequencies.py, mode: {mode_for_figtbl}, ticker: {ticker_for_figtbl}): {e}")
        return empty_figs_tuple
