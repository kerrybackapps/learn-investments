import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.futures_options.american_call_figtbl import figtbl
from pages.formatting import Layout, Slider

title = "American call with a single cash dividend"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None
text = """
        If the underlying asset pays a single dividend prior to the maturity of a call option, then it can be optimal to
        exercise the call just before the asset goes ex-dividend in order to capture
        the dividend.  Exercise at other times is not optimal.  The left
        plot shows the critical price $$S^*$$ such that it is optimal to exercise if and only if $$S_t \\ge S^*$$, where
        $$S_t$$ denotes the underlying price just before it goes ex-dividend.  When the dividend is lower, it is less
        likely that it will be optimal to exercise (the critical price $$S^*$$ is larger).  The right plot shows
        how the American call value compares to the corresponding European call value prior to the ex-dividend date 
        $$t$$.  When the dividend is low, the two values are close together, because it is unlikely that it will be
        optimal to exercise the American call before maturity.  The assumptions that underlie the plots are that the 
        forward price of the asset (for a forward contract maturing at the option maturity date) has a constant volatility
        and the price of the underlying drops by the dividend at the ex-dividend date.  Pricing of the European call
        is by Black-Scholes.  Pricing of the American call is by 
        Black-Scholes after the ex-dividend date and by a variation of Black-Scholes prior to the ex-dividend date.
        """

name = "american-options"

inputs = [name + "input" + str(i) for i in range(6)]

slider1 = Slider(
    "Strike price", mn=0, mx=100, step=5, value=50, tick=25, name=inputs[0], kind="dol"
)
slider2 = Slider(
    "Volatility of forward price of underlying",
    mn=0,
    mx=80,
    step=1,
    value=40,
    tick=20,
    name=inputs[1],
    kind="pct",
)
slider3 = Slider(
    "Risk-free rate", mn=0, mx=5, step=0.1, value=1, tick=1, name=inputs[2], kind="pct"
)
slider4 = Slider(
    "Years to ex-dividend date", mn=0, mx=5, step=0.25, value=1, tick=1, name=inputs[3]
)
slider5 = Slider(
    "Years from ex-dividend date to maturity",
    mn=0,
    mx=5,
    step=0.25,
    value=1,
    tick=1,
    name=inputs[4],
)
slider6 = Slider(
    "Underlying price",
    mn=0,
    mx=100,
    step=0.1,
    value=50,
    tick=25,
    name=inputs[5],
    kind="dol",
)


graph1 = dcc.Graph(id=name + "fig1")
graph2 = dcc.Graph(id=name + "fig2")

col1 = dbc.Col(slider1, xs=12, sm=6, md=4, lg=4, className="mb-2")
col2 = dbc.Col(slider5, xs=12, sm=6, md=4, lg=4, className="mb-2")
col3 = dbc.Col(slider6, xs=12, sm=6, md=4, lg=4, className="mb-2")  # Underlying price
row1 = dbc.Row([col1, col2, col3, dbc.Col(xs=0, sm=0, md=4, lg=4)], className="gx-1")

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
