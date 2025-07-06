import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import FormatTemplate
from pages.formatting import Slider, Layout, text_style
from pages.borrowing_saving.amortization_schedules_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

name = "_amortization-schedules"

inputs = [name + "input" + str(i) for i in range(5)]
slider1 = Slider(
    "Principal",
    mn=0,
    mx=1000000,
    step=1000,
    value=400000,
    tick=200000,
    name=inputs[0],
    kind="kdol",
)
slider2 = Slider(
    "Annual Rate", mn=0, mx=12, step=0.01, value=4.5, tick=3, kind="pct", name=inputs[1]
)
slider3 = Slider(
    "Number of Years", mn=0, mx=30, step=1, value=15, tick=5, name=inputs[2], kind=None
)
slider4 = Slider(
    "Balloon",
    mn=0,
    mx=1000000,
    step=1000,
    value=0,
    tick=200000,
    name=inputs[3],
    kind="kdol",
)

radio = dcc.RadioItems(
    options=[
        {"value": "Monthly", "label": "Monthly"},
        {"value": "Annual", "label": "Annual"},
    ],
    value="Monthly",
    inline=True,
    id=inputs[4],
    labelStyle={"display": "block"},
)

left = dbc.Col(dbc.Label("Payment Frequency", html_for=inputs[4]), md=6)
right = dbc.Col(radio, md=6)
radio = dbc.Row([left, right], align="top")

graph = dcc.Graph(id=name + "fig")
graph2 = dcc.Graph(id=name + "fig2")

payment = html.Div(id=name + "payment", style=text_style)
paymentLabel = dbc.Col(dbc.Label("Payment", html_for=name + "payment"), md=6)
payment = dbc.Row([paymentLabel, dbc.Col(payment, md=6)])

col1 = dbc.Col([slider3, html.Br(), radio], md=4)
col2 = dbc.Col([slider1, slider4], md=4)
col3 = dbc.Col([slider2, html.Br(), payment], md=4)
row1 = dbc.Row([col1, col2, col3], align="top")

left = dbc.Col(graph2, md=6)
right = dbc.Col(graph, md=6)
row2 = dbc.Row([left, right])
layout = dbc.Container([html.Br(), html.Br(), row1, html.Br(), row2], fluid=True)

outputs = [
    Output(name + "fig", "figure"),
    Output(name + "fig2", "figure"),
    Output(name + "payment", "children"),
]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)
