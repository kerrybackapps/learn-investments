import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.formatting import Slider, Layout
from pages.bonds.tips_figtbl import figtbl


title = "Treasury inflation protected securities"
runtitle = None
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = None
text = """
             The face value of a TIPS (Treasury Inflation Protected Security) rises with inflation, and the 
             coupons are a fixed percentage of the face value, so
             the coupons also rise with inflation.  The result is that real cash flows (i.e., cash flows in
             constant dollars) are constant.  In contrast, for a non-inflation-protected Treasury bond, cash flows
             are fixed in nominal terms, so real cash flows fall when there is inflation.  This page provides
             an illustration of the nominal and real cash flows, assuming for simplicity that inflation is constant
             over time.  The cash flows are presented on a log scale so that variation in the coupons is easier to 
             see.
          """

name = "tips"

inputs = [name + "input" + str(i) for i in range(4)]
slider1 = Slider(
    "Maturity", mn=0, mx=30, step=0.5, value=10, tick=5, name=inputs[0], kind=None
)
slider2 = Slider(
    "Inflation", mn=0, mx=10, step=0.1, value=4, tick=2, kind="pct", name=inputs[1]
)
slider3 = Slider(
    "Coupon Rate for Regular Treasury",
    mn=0,
    mx=10,
    step=0.1,
    value=6,
    tick=2,
    kind="pct",
    name=inputs[2],
)
slider4 = Slider(
    "Coupon Rate for TIPS",
    mn=0,
    mx=10,
    step=0.1,
    value=6,
    tick=2,
    kind="pct",
    name=inputs[3],
)

left = dbc.Col([slider1, slider2], md=6)
right = dbc.Col([slider3, slider4], md=6)
row1 = dbc.Row([left, right], align="top")

graph1 = dbc.Col(dcc.Graph(id=name + "fig1"), md=6)
graph2 = dbc.Col(dcc.Graph(id=name + "fig2"), md=6)
row2 = dbc.Row([graph1, graph2], align="center")

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

outputs = [Output(name + "fig1", "figure"), Output(name + "fig2", "figure")]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)
