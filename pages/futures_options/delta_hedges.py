import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.futures_options.delta_hedges_figtbl import figtbl
from pages.formatting import Layout, Slider, blue, text_style


title = "Delta hedges"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None
text = """
        This page illustrates how to replicate or hedge an option based on its delta.  The page assumes that the options
        are European and that the correct valuation model is the Black-Scholes model.  The blue curves are the Black-Scholes
        values.  The red lines show the values of portfolios that hold delta shares purchased with leverage (for a call) or
        are short |delta| shares and hold  cash (for a put).  The $$y$$ intercept of the red line is the amount of 
        borrowed money (for a call) or the amount of cash held (for a put).  For small changes in the value of
        the underlying, the change in the value of a delta hedge is approximately the same as the change in 
        the value of the option.  Thus, the delta hedge is a hedge for someone who has sold the option.
        """

name = "delta-hedges"

inputs = [name + "input" + str(i) for i in range(6)]

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
slider6 = Slider(
    "Underlying price",
    mn=0,
    mx=100,
    step=1,
    value=50,
    tick=25,
    name=inputs[5],
    kind="dol",
)

label_call_delta = html.Div(id=name + "out01")
call_delta = html.Div(id=name + "out1", style=text_style)
label_call_cash = html.Div("Cash in delta hedge:")
call_cash = html.Div(id=name+"call-cash", style=text_style)

label_put_delta = html.Div(id=name + "out02")
put_delta = html.Div(id=name + "out2", style=text_style)
label_put_cash = html.Div("Cash in delta hedge:")
put_cash = html.Div(id=name+"put-cash", style=text_style)

graph1 = dcc.Graph(id=name + "fig1")
graph2 = dcc.Graph(id=name + "fig2")


col1 = dbc.Col(slider1, md=4)
col2 = dbc.Col(slider5, md=4)
col3 = dbc.Col(slider6, md=4)  # Underlying price
row1 = dbc.Row([col1, col2, col3])

col1 = dbc.Col(slider2, md=4)
col2 = dbc.Col(slider4, md=4)
col3 = dbc.Col(slider3, md=4)
row2 = dbc.Row([col1, col2, col3])

col1 = dbc.Col([label_call_delta, label_call_cash], md=3)
col2 = dbc.Col([call_delta, call_cash], md=3)
col3 = dbc.Col([label_put_delta, label_put_cash], md=3)
col4 = dbc.Col([put_delta, put_cash], md=3)
row3 = dbc.Row([col1, col2, col3, col4], align="center")


col1 = dbc.Col(graph1, md=6)
col2 = dbc.Col(graph2, md=6)
row4 = dbc.Row([col1, col2], align="center")

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
lst = (
    [Output(name + f, "figure") for f in ["fig1", "fig2"]]
    + [Output(name + o, "children") for o in ["out1", "out2"]]
    + [Output(name + o, "children") for o in ["out01", "out02"]]
    + [Output(name + o, "children") for o in ["call-cash", "put-cash"]]
    + [Input(i, "value") for i in inputs]
)


@callback(*lst)
def call(*args):
    return figtbl(*args)
