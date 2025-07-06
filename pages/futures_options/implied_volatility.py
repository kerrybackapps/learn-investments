import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    style_data,
    css_no_header,
    style_data_conditional,
    Slider,
    text_style
)
from pages.futures_options.implied_volatility_figtbl import figtbl

title = "Implied volatilities"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None

text = """
    Implied volatilites are computed from the Black-Scholes formulas.  An implied volatility is the volatility that,
    when input into the formula, produces a valuation equal to the market option premium (price).  The tables 
    below verify that the put and call formulas produce the premia that are input (which represent
    hypothetical market prices) when the implied volatilities
    are input to the formulas.  The figure shows that the formulas produce prices below the market prices for
    volatilities less than the implied volatilities and produce prices above the market prices for volatilities 
    greater than the implied volatilities.  The implied volatilities are at the intersections of the price curves
    with the dashed lines at the market prices.  When the put and call premia satisfy put-call parity, then they
    will generate the same implied volatilities (the dots in the figure will align vertically).
    
    The Black-Scholes formula for the value of a European call option shown in the table
    below is $e^{-qT}SN(d_1) - e^{-rT}KN(d_2)$, where
    $q$ is the dividend yield, $T$ is the time to maturity of the option,
    $S$ is the price of the underlying asset, $r$ is the risk-free rate, and $K$ is the
    strike price.  Also, $N$ denotes the standard normal cumulative distribution function, 
    $d_1 = (\log(S/K) + (r-q+0.5\sigma^2)T)/\sqrt{\sigma^2T}$, and $d_2=d_1-\sigma\sqrt{T}$, where
    $\sigma$ denotes the volatility of the underlying asset.  The Black-Scholes
    formula for the value of a European put option is $e^{-rT}KN(-d_2) - e^{-qT}SN(-d_1)$.
    """

name = "implied-volatility"

inputs = [name + "input" + str(i) for i in range(7)]

slider1 = Slider(
    "Strike price", mn=0, mx=200, step=5, value=100, tick=50, name=inputs[0], kind="dol"
)
slider2 = Slider(
    "Call premium", mn=0, mx=40, step=0.1, value=10.2, tick=10, name=inputs[1], kind="dol"
)
slider3 = Slider(
    "Risk-free rate", mn=0, mx=5, step=0.1, value=2, tick=1, name=inputs[2], kind="pct"
)
slider4 = Slider(
    "Dividend yield", mn=0, mx=5, step=0.1, value=4, tick=1, name=inputs[3], kind="pct"
)
slider5 = Slider(
    "Years to maturity", mn=0, mx=2, step=0.05, value=1, tick=0.5, name=inputs[4]
)
slider6 = Slider(
    "Underlying price",
    mn=0,
    mx=200,
    step=1,
    value=100,
    tick=50,
    name=inputs[5],
    kind="dol",
)
slider7 = Slider(
    "Put premium", mn=0, mx=40, step=0.1, value=12.2, tick=10, name=inputs[6], kind="dol"
)

title1 = dbc.Label("European Call")
title2 = dbc.Label("European Put")

tbl1 = DataTable(
    id=name + "tbl1",
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)
tbl2 = DataTable(
    id=name + "tbl2",
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)

out1 = html.Div(id=name + "out1", style=text_style)
label1 = dbc.Label("Call implied volatility", html_for=name + "out1")
out2 = html.Div(id=name + "out2", style=text_style)
label2 = dbc.Label("Put implied volatility", html_for=name + "out2")

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider4], md=4)
middle = dbc.Col([slider5, slider3], md=4)
right = dbc.Col(slider6, md=4)
row1 = dbc.Row([left, middle, right], align="top")

left = dbc.Col([slider2, html.Br(), label1, out1, html.Br(), tbl1], md=3)
right = dbc.Col([slider7, html.Br(), label2, out2, html.Br(), tbl2], md=3)

graph = dbc.Col(graph, md=6)
row2 = dbc.Row([left, right, graph], align="end")

body = html.Div([row1, html.Br(), row2])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = (
    [Output(name + "tbl1", "data"), Output(name + "tbl2", "data")]
    + [Output(name + "fig", "figure")]
    + [Output(name + o, "children") for o in ["out1", "out2"]]
    + [Input(i, "value") for i in inputs]
)


@callback(*lst)
def call(*args):
    return figtbl(*args)
