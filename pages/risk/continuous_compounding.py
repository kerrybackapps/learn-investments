# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback, State, callback_context # Added State, callback_context
import dash_bootstrap_components as dbc
from pages.risk.continuous_compounding_figtbl import figtbl
from pages.formatting import Layout, style_header, style_data_conditional, myinput
from datetime import date
from dash.dash_table import DataTable, FormatTemplate
from dash.exceptions import PreventUpdate # Added PreventUpdate
import plotly.graph_objects as go # Added go

today = date.today().year - 1
percentage = FormatTemplate.percentage(1)

title = "Continuously compounded returns"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "continuous-compounding"

text = """ 
    Given a rate of return $r$, the continuously compounded return is defined as $r_c = \\log(1+r)$, where $\\log$ is
    the natural logarithm function.  The left figure shows a scatter plot of returns and continuously compounded returns
    for either the aggregate U.S. stock market or an individual ticker, over the date range specified.  The points
    trace out the function $y=\\log(1+x)$.  The right figure and the table show the distributions of returns 
    and continuously compounded returns (CC Returns). 
    
    The name "continuously compounded return" stems from the fact that, given a return $x$ compounded $m$ times per
    period as $(1+x/m)^m$, the accumulation $(1+x/m)^m$ converges to $e^x$ as $m \\rightarrow \\infty$, where $e$ is
    the natural exponential.  Thus, compounding an infinite number of times (continuously) produces an accumulation
    of $e^x$.  Given a return $r$ compounded only once per period, the definition of the continuously compounded return
    $r_c$ as $r_c = \\log(1+r)$ implies that $e^{r_c} = 1+r$.  Thus, $r_c$ is the rate that, if compounded 
    continuously, would produce the same accumulation as $r$.
    
    The usefulness of the continuously compounded return stems from the fact that, given returns $r_1, \\ldots, r_n$ and
    corresponding continuously compounded returns $r_{ci} = \\log(1+r_i)$, the accumulation $(1+r_1) \\cdots (1+r_n)$
    equals $e^{r_{c1} + \\cdots r_{cn}}$.  Thus, continuously compounded returns are added (and then exponentiated)
    rather than multiplied as are ordinary returns.  In particular,  one plus the geometric average return equals the 
    exponential of the *arithmetic* average continuously compounded return.  It is frequently assumed that continuously
    compounded returns are normally distributed, for example, in the Black-Scholes option pricing model.
    """

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


columns = [
    dict(name=c, id=name + c, type="numeric", format=percentage)
    for c in ["", "Return", "CC Return"]
]
tbl = DataTable(
    id=name + "tbl",
    columns=columns,
    style_header = style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl_col = dbc.Col(dcc.Loading(tbl, type="circle"), xs=12, sm=12, md=4, lg=4, className="mb-2")

fig1_col = dbc.Col(dcc.Loading(dcc.Graph(id=name + "fig1"), type="circle"), xs=12, sm=12, md=4, lg=4, className="mb-2")
fig2_col = dbc.Col(dcc.Loading(dcc.Graph(id=name + "fig2"), type="circle"), xs=12, sm=12, md=4, lg=4, className="mb-2")

row1 = dbc.Row([slider_col, inpt_col], align="center", className="gx-1")
row2 = dbc.Row([tbl_col, fig1_col, fig2_col], align="center", className="gx-1")

body = dbc.Container([row1, html.Hr(), row2, ticker_interval], fluid=True, className="px-1")

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
    Output(name + "tbl", "data")
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
    # Structure for empty table data based on columns: ["", "Return", "CC Return"]
    empty_data_table = [{"": "", "Return": "", "CC Return": ""}] 
    empty_outputs_tuple = (empty_fig, empty_fig, empty_data_table)

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
        # continuous_compounding_figtbl.figtbl expects (name, dates, radio, ticker)
        # We need to pass (name, date_range, mode_for_figtbl, ticker_for_figtbl)
        return figtbl(name, date_range, mode_for_figtbl, ticker_for_figtbl)
    except Exception as e:
        print(f"Error in figtbl call (file: continuous_compounding.py, mode: {mode_for_figtbl}, ticker: {ticker_for_figtbl}): {e}")
        return empty_outputs_tuple
