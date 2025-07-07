import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    style_header,
    style_data_conditional,
    Slider,
    blue,
    red,
)
from pages.futures_options.monte_carlo_figtbl import figtbl

title = "Monte Carlo option valuation"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None
text = """
    Black and Scholes assumed that the natural logarithm of the underlying asset price at the option maturity is
    normally distributed with standard deviation equal to $\sigma\sqrt{T}$, where $\sigma$ is called the volatility
    and $T$ is the number of years to maturity of the option.  The Black-Scholes formula
    can be derived by assuming the stock earns the risk-free rate on
    average and discounting the expected option value at maturity at the risk-free rate.  This page estimates the expected
    values at maturity by simulation.  20,000 values of the underlying 
    asset price $S_T$ at the option maturity are simulated as the exponential of
    $\log S_T = \log S_0 + (r-q-0.5\sigma^2)T + \sigma\sqrt{T}\epsilon$, 
    where $\epsilon$ is a simulated standard normal random variable, and $r$ is the interest rate, $q$ is the dividend
    yield, $\sigma$ is the volatility, $T$ is the time to maturity, and $S_0$ is the initial underlying asset 
    price.  The figure on the left shows a histogram of the simulated prices.  In each simulation, the call value 
    $\max(0, S_T-K)$ and put value $\max(0, K-S_T)$ are calculated.  The histograms of in-the-money values of the
    call and put are shown
    in the other two figures.  The discounted average values approximate the Black-Scholes formula, and the approximation
    would be better if a larger number of values were simulated.  
    """

name = "monte-carlo"

inputs = [name + "input" + str(i) for i in range(6)]

slider1 = Slider("Underlying price", mn=0, mx=200, step=5, value=100, tick=50, name=inputs[0], kind="dol"
)

slider2 = Slider(
    "Strike price", mn=0, mx=200, step=1, value=100, tick=50, name=inputs[1], kind="dol",
)


slider3 = Slider(
    "Volatility", mn=0, mx=80, step=1, value=40, tick=20, name=inputs[2], kind="pct"
)

slider4 = Slider(
    "Risk-free rate", mn=0, mx=5, step=0.1, value=2, tick=1, name=inputs[3], kind="pct"
)

slider5 = Slider(
    "Dividend yield", mn=0, mx=5, step=0.1, value=4, tick=1, name=inputs[4], kind="pct"
)

slider6 = Slider(
    "Years to maturity", mn=0, mx=2, step=0.05, value=1, tick=0.5, name=inputs[5]
)


btn = dbc.Button(
    "Click to Simulate",
    id=name + "btn",
    n_clicks=0,
    color="primary",
    className="me-1",
)

col1 = dbc.Col([slider1, slider2], xs=12, sm=6, md=4, lg=4, className="mb-2")
col2 = dbc.Col([slider3, slider4], xs=12, sm=6, md=4, lg=4, className="mb-2")
col3 = dbc.Col([slider5, slider6], xs=12, sm=12, md=4, lg=4, className="mb-2")
row1 = dbc.Row([col1, col2, col3], align='top', className="gx-1")


col1 = dbc.Col(html.Div('Black-Scholes call value:'), xs=12, sm=6, md=3, lg=3, className="mb-2")
call_bs = html.Div(id=name + 'call_bs', style={"color": blue, "font-weight": "bold"})
col2 = dbc.Col(call_bs, xs=12, sm=6, md=3, lg=3, className="mb-2")
col3 = dbc.Col(html.Div('Black-Scholes put value:'), xs=12, sm=6, md=3, lg=3, className="mb-2")
put_bs = html.Div(id=name + 'put_bs', style={"color": red, "font-weight": "bold"})
col4 = dbc.Col(put_bs, xs=12, sm=6, md=3, lg=3, className="mb-2")
row2 = dbc.Row([col3, col4, col1, col2], align='center', className="gx-1")

row3 = dbc.Row(dbc.Col(btn, xs=12, sm=6, md=2, lg=2, className="mx-auto text-center mb-2"), className="gx-1")

col1 = dbc.Col(html.Div("Discounted average call value:"), xs=12, sm=6, md=6, lg=6, className="mb-2")
call_mc = dcc.Loading(html.Div(id=name + 'call_mc', style={'color': blue}), type="circle")
col2 = dbc.Col(call_mc, xs=12, sm=6, md=6, lg=6, className="mb-2")
rowa = dbc.Row([col1, col2], className="gx-1")

col1 = dbc.Col(html.Div("Discounted average put value:"), xs=12, sm=6, md=6, lg=6, className="mb-2")
put_mc = dcc.Loading(html.Div(id=name + 'put_mc', style={'color': red}), type="circle")
col2 = dbc.Col(put_mc, xs=12, sm=6, md=6, lg=6, className="mb-2")
rowb = dbc.Row([col1, col2], className="gx-1")

col1 = dbc.Col([dcc.Loading(dcc.Graph(id=name+"fig"), type="circle")], xs=12, sm=12, md=6, lg=6, className="mb-2")
col2 = dbc.Col([rowb, html.Br(), dcc.Loading(dcc.Graph(id=name+"fig_put"), type="circle")], xs=12, sm=6, md=3, lg=3, className="mb-2")
col3 = dbc.Col([rowa, html.Br(), dcc.Loading(dcc.Graph(id=name+"fig_call"), type="circle")], xs=12, sm=6, md=3, lg=3, className="mb-2")
row4 = dbc.Row([col1, col2, col3], align='end', className="gx-1")

body = dbc.Container([row1, html.Hr(), row2, html.Hr(), row3, html.Br(), row4], fluid=True, className="px-1")

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
    Output(name+"fig", "figure"),
    Output(name+"fig_put", "figure"),
    Output(name+"fig_call", "figure"),
    Output(name+"put_bs", "children"),
    Output(name+"call_bs", "children"),
    Output(name+"put_mc", "children"),
    Output(name+"call_mc", "children"),
    Input(name + "btn", "n_clicks"),
    *[Input(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(*args)
