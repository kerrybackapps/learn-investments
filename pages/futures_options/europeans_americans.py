import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.futures_options.europeans_americans_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "European and American option values"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None
text = """
        Assuming a constant volatility, a constant dividend yield, and a constant risk-free rate, the Black-Scholes
        formula is used to value European options, and a binomial tree is used to value American options.  The values
        are shown as functions of the underlying asset price.  An American option is always worth at least as
        much as the intrinsic value, and it is optimal to exercise the option when the American and intrinsic
        values are the same.  A European option can sometimes be worth less than the intrinsic value.
        """

name = "europeans-americans"

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
    "Risk-free rate", mn=0, mx=5, step=0.1, value=3, tick=1, name=inputs[2], kind="pct"
)
slider4 = Slider(
    "Dividend yield", mn=0, mx=5, step=0.1, value=4, tick=1, name=inputs[3], kind="pct"
)
slider5 = Slider(
    "Years to maturity", mn=0, mx=5, step=0.25, value=3, tick=1, name=inputs[4]
)

graph1 = dcc.Graph(id=name + "fig1")
graph2 = dcc.Graph(id=name + "fig2")

col1 = dbc.Col(slider1, xs=12, sm=6, md=4, lg=4, className="mb-2")
col2 = dbc.Col(slider5, xs=12, sm=6, md=4, lg=4, className="mb-2")
row1 = dbc.Row([col1, col2, dbc.Col(xs=0, sm=0, md=4, lg=4)], className="gx-1")

col1 = dbc.Col(slider2, xs=12, sm=6, md=4, lg=4, className="mb-2")
col2 = dbc.Col(slider4, xs=12, sm=6, md=4, lg=4, className="mb-2")
col3 = dbc.Col(slider3, xs=12, sm=6, md=4, lg=4, className="mb-2")
row2 = dbc.Row([col1, col2, col3], className="gx-1")

col1 = dbc.Col(graph1, xs=12, sm=12, md=6, lg=6, className="mb-2")
col2 = dbc.Col(graph2, xs=12, sm=12, md=6, lg=6, className="mb-2")
row3 = dbc.Row([col1, col2], align="center", className="gx-1")

body = dbc.Container([row1, row2, html.Br(), row3], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + f, "figure") for f in ["fig1", "fig2"]] + [
    Input(i, "value") for i in inputs
]


@callback(*lst)
def call(*args):
    return figtbl(*args)
