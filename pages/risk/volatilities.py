# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback, State, callback_context # Added State, callback_context
import dash_bootstrap_components as dbc
from pages.risk.volatilities_figtbl import figtbl
from pages.formatting import Layout, myinput
from datetime import date
from dash.exceptions import PreventUpdate # Added PreventUpdate
import plotly.graph_objects as go # Added go

today = date.today().year - 1

title = "Time varying volatilities"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "volatilities"

text = """ 
    The standard deviation of daily returns (volatility) is calculated for each month in the specified date 
    range for either the
    U.S. stock market or an individual ticker.  The time series of volatility is plotted in the 
    top left figure.  Typically,
    there is some clustering (persistence) of volatility.  This can be confirmed by the top right figure,
    which shows a regression line of volatility on lagged (previous month's) volatility.  The bottom left figure
    provides an answer to the question of whether lagged volatility predicts returns.  If volatility is higher when
    lagged volatility is higher, but returns are not higher, then an investor may want to reduce exposure
    when lagged volatility is high.  The bottom right figure looks at the correlation of returns with contemporaneous
    (same month's) volatility.  A negative slope of the regression line in that figure is consistent with 
    volatility rising during downturns.  
        
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
inpt_col = dbc.Col(inpt, md=5) # Adjusted width
slider_col = dbc.Col([dbc.Label("Date Range", html_for=name + "slider"), slider], md=7) # Adjusted width

fig1 = dcc.Loading(dcc.Graph(id=name + "fig1"), type="circle")
fig2 = dcc.Loading(dcc.Graph(id=name + "fig2"), type="circle")
fig3 = dcc.Loading(dcc.Graph(id=name + "fig3"), type="circle")
fig4 = dcc.Loading(dcc.Graph(id=name + "fig4"), type="circle")

left = dbc.Col([fig1, fig3], md=6)
right = dbc.Col([fig2, fig4], md=6)

row1 = dbc.Row([slider_col, inpt_col], align="center") # Updated row1 layout
row2 = dbc.Row([left, right], align="top")

body = html.Div([row1, html.Br(), row2, ticker_interval]) # Added ticker_interval

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
    Output(name+"fig1", "figure"),
    Output(name+"fig2", "figure"),
    Output(name+"fig3", "figure"),
    Output(name+"fig4", "figure")
]

# Define inputs for main callback
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
    empty_figs_tuple = (empty_fig, empty_fig, empty_fig, empty_fig)

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
        # volatilities_figtbl.figtbl expects *args: (dates, radio, ticker)
        # We need to pass (date_range, mode_for_figtbl, ticker_for_figtbl)
        return figtbl(date_range, mode_for_figtbl, ticker_for_figtbl)
    except Exception as e:
        print(f"Error in figtbl call (file: volatilities.py, mode: {mode_for_figtbl}, ticker: {ticker_for_figtbl}): {e}")
        return empty_figs_tuple
