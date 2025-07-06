import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.futures_options.greeks_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Option Greeks"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None

text = """
        Call and put Greeks for European options are calculated from the Black-Scholes formulas and plotted as functions 
        of the underlying asset price.  The Greeks are (calculus) derivatives of the values with respect to the formula
        inputs, so they tell us the rate at which the values change when the inputs 
        change.  Let $y=f(s,K,\sigma,r,q,T)$ denote a call or put value as a function of the underlying
        asset price $S$, the strike price $K$, the volatility $\sigma$, the interest rate $r$, the dividend
        yield $q$, and the time to maturity $T$.  The Greeks are delta $= \partial y/\partial S$, 
        vega $= \partial y/\partial \sigma$, gamma $= \partial^2 y/\partial S^2$, theta $= -\partial y/\partial T$,
        and rho $= \partial y/\partial r$.  The vega is the same for a call as for a put, and the same is true for
        the gamma.  Also, a call delta equals a put delta plus $e^{-qT}$.  These facts all follow from put-call 
        parity: call price - put price $$= e^{-qT}S - e^{-rT}K$$.
        """

name = "greeks"

inputs = [name + "input" + str(i) for i in range(5)]

slider1 = Slider(
    "Strike price", mn=0, mx=100, step=5, value=50, tick=25, name=inputs[0], kind="dol"
)
slider2 = Slider(
    "Volatility of underlying",
    mn=0,
    mx=80,
    step=1,
    value=40,
    tick=20,
    name=inputs[1],
    kind="pct",
)
slider3 = Slider(
    "Risk-free rate", mn=0, mx=5, step=0.1, value=2, tick=1, name=inputs[2], kind="pct"
)
slider4 = Slider(
    "Dividend yield", mn=0, mx=5, step=0.1, value=3, tick=1, name=inputs[3], kind="pct"
)
slider5 = Slider(
    "Years to maturity", mn=0, mx=2, step=0.05, value=1, tick=0.5, name=inputs[4]
)

graph1 = dcc.Graph(id=name + "fig1")
graph2 = dcc.Graph(id=name + "fig2")
graph3 = dcc.Graph(id=name + "fig3")
graph4 = dcc.Graph(id=name + "fig4")
graph5 = dcc.Graph(id=name + "fig5")

col1 = dbc.Col(slider1, md=4)
col2 = dbc.Col(slider5, md=4)
row1 = dbc.Row([col1, col2, dbc.Col(md=4)])

col1 = dbc.Col(slider2, md=4)
col2 = dbc.Col(slider4, md=4)
col3 = dbc.Col(slider3, md=4)
row2 = dbc.Row([col1, col2, col3])

blank = dbc.Col(md=2)
col1 = dbc.Col(graph1, md=4)  # delta
col2 = dbc.Col(graph4, md=4)  # vega
row3 = dbc.Row([blank, col1, col2, blank], align="center")

col1 = dbc.Col(graph2, md=4)  # gamma
col2 = dbc.Col(graph3, md=4)  # theta
col3 = dbc.Col(graph5, md=4)  # rho
row4 = dbc.Row([col1, col2, col3], align="center")

body = html.Div([row1, row2, html.Br(), row3, html.Br(), row4])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + f, "figure") for f in ["fig1", "fig2", "fig3", "fig4", "fig5"]] + [
    Input(i, "value") for i in inputs
]


@callback(*lst)
def call(*args):
    return figtbl(*args)
