# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback, State, callback_context
import dash_bootstrap_components as dbc
from pages.risk.best_worst_figtbl import figtbl
from pages.formatting import Layout, myinput, lightblue
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

title = "Best and worst periods"
runtitle = None
chapter = "Risk and Return"
chapter_url = "risk"
urls = None
name = "compounded-returns" # Name for this page

text = """
    The two figures on the left show the accumulation $(1+r_1) \\cdots (1+r_i)$
    for years $i=1, \\ldots, n$
    in the best $n$-year period and worst $n$-year period for either the aggregate U.S. stock market or an
    individual ticker.  The third figure from the left shows the geometric average
    return $(1+r_1)^{1/n} \\cdots (1+r_n)^{1/n} - 1$ for the trailing $n$-year period for each year.  The last
    figure is a box plot of the geometric average returns for the overlapping $n$-year periods.  Aggregate U.S. stock
    market return data is from
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
    and begins in 1927.  Returns
    for individual stocks are computed from the dividend and split-adjusted closing prices
    provided by Yahoo Finance beginning in 1970.   """

years = [str(i) + " years" for i in [5, 10, 20, 30]]
drop = dcc.Dropdown(years, value="10 years", id=name + "drop", style={"backgroundColor": lightblue})

inpt = myinput(
    id=name + "ticker", placeholder="Enter MARKET for U.S. market or a ticker"
)

ticker_interval = dcc.Interval(
    id=name + "-ticker-input-interval",
    interval=1500,
    n_intervals=0,
    max_intervals=1
)

graph_all = dcc.Loading(
    id=name + "loading1", children=[dcc.Graph(id=name + "fig1")], type="circle"
)
graph_best = dcc.Loading(
    id=name + "loading2", children=[dcc.Graph(id=name + "fig2")], type="circle"
)
graph_worst = dcc.Loading(
    id=name + "loading3", children=[dcc.Graph(id=name + "fig3")], type="circle"
)
graph_box = dcc.Loading(dcc.Graph(id=name + "fig4"), type="circle")

graph_all = dbc.Col(graph_all, md=4)
graph_best = dbc.Col(graph_best, md=3)
graph_worst = dbc.Col(graph_worst, md=3)
graph_box = dbc.Col(graph_box, md=2)

drop_col = dbc.Col([dbc.Label("Number of years", html_for=name + "drop"), drop], md=6)
inpt_col = dbc.Col(inpt, md=6)

row1 = dbc.Row([drop_col, inpt_col], align="center")
row2 = dbc.Row([graph_best, graph_worst, graph_all, graph_box], align="center")
body = html.Div([row1, html.Hr(), row2, ticker_interval])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name + f, "figure") for f in ["fig1", "fig2", "fig3", "fig4"]]

main_callback_inputs = [
    Input(name + "drop", "value"),
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
def call(years_value, n_intervals, ticker_value_state):
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
        if triggered_id == (name + "-ticker-input-interval") or triggered_id == (name + "drop"):
            return empty_figs_tuple
        raise PreventUpdate

    if processed_ticker_input.lower() == "market":
        mode_for_figtbl = "Market"
        ticker_for_figtbl = None
    else:
        mode_for_figtbl = "Ticker"
        ticker_for_figtbl = processed_ticker_input

    should_call_figtbl = False
    if triggered_id == (name + "drop"):
        should_call_figtbl = True
    elif triggered_id == (name + "-ticker-input-interval") and n_intervals > 0 :
        should_call_figtbl = True

    if not should_call_figtbl:
        raise PreventUpdate

    try:
        return figtbl(years_value, mode_for_figtbl, ticker_for_figtbl)
    except Exception as e:
        print(f"Error in figtbl call (file: best_worst.py, mode: {mode_for_figtbl}, ticker: {ticker_for_figtbl}): {e}")
        return empty_figs_tuple
