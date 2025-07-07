import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    style_data,
    css_no_header,
    style_data_conditional,
    Slider,
    myinput
)
from pages.futures_options.black_scholes_formula_figtbl import figtbl

title = "Black-Scholes formula"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None
text = """
        The Black-Scholes formula for the value of a European call option is $e^{-qT}SN(d_1) - e^{-rT}KN(d_2)$, where
        $q$ is the dividend yield, $T$ is the time to maturity of the option,
        $S$ is the price of the underlying asset, $r$ is the risk-free rate, and $K$ is the
        strike price.  Also, $N$ denotes the standard normal cumulative distribution function, 
        $d_1 = (\log(S/K) + (r-q+0.5*\sigma^2)T)/\sqrt{\sigma^2T}$, and $d_2=d_1-\sigma\sqrt{T}$, where
        $\sigma$ denotes the volatility of the underlying asset.  The Black-Scholes
        formula for the value of a European put option is $e^{-rT}KN(-d_2) - e^{-qT}SN(-d_1)$.
        """

name = "black-scholes-formula"

inputs = [name + "input" + str(i) for i in range(6)]


inpt1 = myinput(id=inputs[0], placeholder="Enter strike price", value=50)
inpt2 = myinput(id=inputs[1], placeholder="Enter volatility as percent", value=30)
inpt3 = myinput(id=inputs[2], placeholder="Enter risk-free rate as percent", value=2)
inpt4 = myinput(id=inputs[3], placeholder="Enter dividend yield as percent", value=3)
inpt5 = myinput(id=inputs[4], placeholder="Enter maturity in years", value=1)
inpt6 = myinput(id=inputs[5], placeholder="Enter price of underlying", value=50)

label1 = 'Enter strike price'
label2 = 'Enter volatility > 0 as percent'
label3 = 'Enter risk-free rate as percent'
label4 = 'Enter dividend yield as percent'
label5 = 'Enter maturity > 0 in years'
label6 = 'Enter price of underlying'

title1 = dbc.Label("European Call")
title2 = dbc.Label("European Put")

tbl1 = DataTable(
    id=name + "tbl1",
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
)

tbl2 = DataTable(
    id=name + "tbl2",
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
)


col1 = dbc.Col([label6, inpt6, html.Br(), label1, inpt1], xs=12, sm=6, md=4, lg=4, className="mb-2")
col2 = dbc.Col([label5, inpt5, html.Br(), label2, inpt2], xs=12, sm=6, md=4, lg=4, className="mb-2")
col3 = dbc.Col([label3, inpt3, html.Br(), label4, inpt4], xs=12, sm=12, md=4, lg=4, className="mb-2")
row1 = dbc.Row([col1, col2, col3], className="gx-1")

col0 = dbc.Col(xs=0, sm=0, md=1, lg=1)
col1 = dbc.Col(title1, xs=12, sm=6, md=4, lg=4, className="text-center mb-2")
col2 = dbc.Col(title2, xs=12, sm=6, md=4, lg=4, className="text-center mb-2")
row2 = dbc.Row([col0, col1, col0, col0, col2, col0], align="center", className="gx-1")

col0 = dbc.Col(xs=0, sm=0, md=1, lg=1)
col1 = dbc.Col(tbl1, xs=12, sm=6, md=4, lg=4, className="mb-2")
col2 = dbc.Col(tbl2, xs=12, sm=6, md=4, lg=4, className="mb-2")
row3 = dbc.Row([col0, col1, col0, col0, col2, col0], align="center", className="gx-1")

body = dbc.Container([row1, html.Hr(), row2, row3], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + f, "data") for f in ["tbl1", "tbl2"]] + [
    Input(i, "value") for i in inputs
]


@callback(*lst)
def call(*args):
    return figtbl(*args)
