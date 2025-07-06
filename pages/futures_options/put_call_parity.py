import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.futures_options.put_call_parity_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Put-call parity"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None

text = """
        The value at maturity of 'call plus cash' is the same as the value at maturity of 'put plus underlying,' 
        when the two options have the same strike price $K$ and the same time to maturity and where
        'cash' means the present value of the strike price.  The 'call plus cash' portfolio is worth $K$ if the
        call finishes out of the money (keep the cash) and worth $S$ if the option price $S$ ends above $K$ (use
        the cash to exercise
        the call).  Likewise, the 'put plus underlying' portfolio is worth $K$ if $S<K$ (exercise the put) and worth
        $S$ if $S>K$ (keep the underlying).  So, for European options, the two portfolios should have the same values
        prior to maturity also.  This means that $C + e^{-rT}K = P + e^{-qT}S$, where $C=$ call premium, $r=$ risk-free
        rate, $T=$ years to maturity, $P=$ put premium, and $q=$ constant dividend yield.  Notice that $e^{-qT}S$ is
        the cost of a fractional share of the underlying asset - just enough to accumulate to a single share by the
        option maturity through the reinvestment of dividends.  This relation between European call and put premia is
        called put-call parity.  We can re-express it as a formula for the difference between the call and put premia:
        $C-P = e^{-qT}S - e^{-rT}K$.  This difference is plotted below as a function of the underlying price $S$.
        """

name = "put-call-parity"

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
    "Dividend yield", mn=0, mx=5, step=0.1, value=4, tick=1, name=inputs[3], kind="pct"
)
slider5 = Slider(
    "Years to maturity", mn=0, mx=5, step=0.1, value=2, tick=1, name=inputs[4]
)

graph1 = dcc.Graph(id=name + "fig1")

col1 = dbc.Col(slider1, md=4)
col2 = dbc.Col(slider5, md=4)
row1 = dbc.Row([col1, col2, dbc.Col(md=4)])

col1 = dbc.Col(slider2, md=4)
col2 = dbc.Col(slider4, md=4)
col3 = dbc.Col(slider3, md=4)
row2 = dbc.Row([col1, col2, col3])

col0 = dbc.Col(md=2)
col1 = dbc.Col(graph1, md=8)
row3 = dbc.Row([col0, col1, col0], align="center")

body = html.Div([row1, row2, html.Br(), row3])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + "fig1", "figure")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(*args)
