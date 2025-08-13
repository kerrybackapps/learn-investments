import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.futures_options.delta_hedge_portfolios_figtbl import figtbl
from pages.formatting import Layout, Slider, blue, text_style, myinput, lightblue

title = "Delta hedges of option portfolios"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None
text = """
    This page illustrates how to hedge a portfolio of options, including possibly a position in the underlying asset.
    The delta of a portfolio is the sum of the deltas of the individual securities.  The delta of a long position 
    in the underlying is $+1$, and the delta of a short position in 
    the underlying is $-1$.  The page assumes that the options
    are European, and option deltas and option values are computed from the Black-Scholes model.  The blue curve is the 
    Black-Scholes
    value of the portfolio.  The red line shows the value of a portfolio that holds delta shares (with delta
    possibly negative) and a position in the risk-free asset such that the investment in the portfolio equals the
    value of the option portfolio.  For small changes in the value of
    the underlying, the change in the value of a delta hedge is approximately the same as the change in the 
    portfolio value.  Thus, the delta hedge is a hedge for someone who has sold the option portfolio.
    """

name = "delta-hedges-portfolios"

numoptions = 5
inputs = [name + "input" + str(i) for i in range(4 * numoptions + 6)]

slider1 = Slider(
    "Underlying price",
    mn=0,
    mx=100,
    step=1,
    value=50,
    tick=25,
    name=inputs[0],
    kind="dol",
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

dropu = dcc.Dropdown(["None", "Long", "Short"], value="None", id=inputs[4], style={"backgroundColor": lightblue})
dropq = dcc.Dropdown([i for i in range(1, 4)], placeholder="Quantity", id=inputs[5], style={"backgroundColor": lightblue})
dropu = dbc.Col([dbc.Label("Position in underlying", html_for=inputs[0]), dropu], xs=12, sm=9, md=9, lg=9, className="mb-2")
dropq = dbc.Col(dropq, xs=12, sm=3, md=3, lg=3, className="mb-2")
row = dbc.Row([dropu, dropq], align="end", className="gx-1")

inpts = [
    row,
    html.Br(),
    dbc.Label("Options", html_for=inputs[6]),
]

for i in range(numoptions):
    inpts.append(html.Br())
    drop1 = dcc.Dropdown(
        ["Call", "Put", "None"], placeholder="Security", id=inputs[4 * i + 6], style={"backgroundColor": lightblue}
    )
    drop2 = dcc.Dropdown(
        [i for i in range(5, 105, 5)], placeholder="Strike", id=inputs[4 * i + 7], style={"backgroundColor": lightblue}
    )
    drop3 = dcc.Dropdown(
        [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
        placeholder="Maturity",
        id=inputs[4 * i + 8],
        style = {"backgroundColor": lightblue}
    )
    drop4 = dcc.Dropdown(
        [i for i in range(3, -4, -1) if i != 0],
        placeholder="Quantity",
        id=inputs[4 * i + 9],
        style={"backgroundColor": lightblue}
    )
    drop1 = dbc.Col(drop1, xs=12, sm=6, md=3, lg=3, className="mb-2")
    drop2 = dbc.Col(drop2, xs=12, sm=6, md=3, lg=3, className="mb-2")
    drop3 = dbc.Col(drop3, xs=12, sm=6, md=3, lg=3, className="mb-2")
    drop4 = dbc.Col(drop4, xs=12, sm=6, md=3, lg=3, className="mb-2")
    row = dbc.Row([drop1, drop2, drop3, drop4], className="gx-1")
    inpts.append(row)

string1 = html.Div(id=name + "string1")
string1a = html.Div("Cash in delta hedge:")
string2 = html.Div(id=name + "string2", style=text_style)
string2a = html.Div(id=name+"string3", style=text_style)

graph = dcc.Graph(id=name + "fig")

col1 = dbc.Col([slider1, slider2], xs=12, sm=12, md=6, lg=6, className="mb-2")
col2 = dbc.Col([slider3, slider4], xs=12, sm=12, md=6, lg=6, className="mb-2")
row1 = dbc.Row([col1, col2], className="gx-1")

left = dbc.Col(inpts, xs=12, sm=12, md=6, lg=6, className="mb-2")
col1 = dbc.Col([string1, string1a], xs=12, sm=12, md=6, lg=6, className="mb-2")
col2 = dbc.Col([string2, string2a], xs=12, sm=12, md=6, lg=6, className="mb-2")
row = dbc.Row([col1, col2], className="gx-1")
strings_col = dbc.Col(row, xs=12, sm=12, md=12, lg=12, className="mb-2")
graph_col = dbc.Col(graph, xs=12, sm=12, md=12, lg=12, className="mb-2")
right = dbc.Col([strings_col, graph_col], xs=12, sm=12, md=6, lg=6, className="mb-2")
row2 = dbc.Row([left, html.Br(), right], align="top", className="gx-1")

body = dbc.Container([row1, html.Br(), row2], fluid=True, className="px-1")
layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
outputs = [Output(name + "fig", "figure")] + [Output(name + s, "children") for s in ["string1", "string2", "string3"]]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs

@callback(*lst)
def call(*args):
    return figtbl(*args)
