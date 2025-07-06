from dash import callback, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from pages._outliers_figtbl import figtbl
from pages.formatting import Slider


name = "_outliers"

xslider = Slider(
    "Add to x:",
    mn=-20,
    mx=20,
    step=.1,
    value=0,
    tick=4,
    name=name + "x",
)

yslider = Slider(
    "Add to y:",
    mn=-20,
    mx=20,
    step=.1,
    value=0,
    tick=4,
    name=name + "y",
)

fig = dcc.Graph(id=name + "fig")

xslider = dbc.Col(xslider, xs=6)
yslider = dbc.Col(yslider, xs=6)
fig = dbc.Row(dbc.Col(fig, xs=12))
row = dbc.Row([xslider, yslider], align="top")
layout = dbc.Container([row, html.Br(), fig], fluid=True)

lst = [
    Output(name + "fig", "figure"),
    Input(name + "x", "value"),
    Input(name + "y", "value")
]

@callback(*lst)
def call(*args):
    return figtbl(*args)

