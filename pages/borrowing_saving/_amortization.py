from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.three_assets_figtbl import figtbl
from pages.formatting import Slider, Layout, text_style, mybadge
import numpy_financial as npf

name = "_annuities"

###########
Rate_Slider_Arg = {
    "text": "Annual Rate",
    "mn": 0,
    "mx": 12,
    "step": 0.05,
    "value": 4.5,
    "tick": 3,
    "kind": "pct",
}

Principal_Slider_Arg = {
    "text": "Principal",
    "mn": 0,
    "mx": 1000000,
    "step": 5000,
    "value": 400000,
    "tick": 200000,
    "kind": "kdol",
}

Payment_Slider_Arg = {
    "text": "Payment",
    "mn": 0,
    "mx": 15000,
    "step": 100,
    "value": 3000,
    "tick": 3000,
    "kind": "kdol",
}

Balloon_Slider_Arg = {
    "text": "Balloon",
    "mn": 0,
    "mx": 1000000,
    "step": 5000,
    "value": 0,
    "tick": 200000,
    "kind": "kdol",
}

variables = ["rate", "principal", "payment", "balloon"]
inputs = [name + "input" + str(i) for i in range(12)]
outputs = [name + str(i) for i in variables]

radio0 = dcc.RadioItems(
    options=[
        {"value": "Monthly", "label": "Monthly"},
        {"value": "Annual", "label": "Annual"},
    ],
    value="Monthly",
    inline=True,
    id=name + "termtype",
)
label = html.Div("Payment Frequency")
slider0 = Slider(
    "Number of Years", mn=0, mx=30, step=1, value=15, tick=5, name=name + "term"
)

# Input components
slider11 = Slider(**Rate_Slider_Arg, name=inputs[0])
slider21 = Slider(**Rate_Slider_Arg, name=inputs[1])
slider31 = Slider(**Rate_Slider_Arg, name=inputs[2])
slider41 = Slider(**Principal_Slider_Arg, name=inputs[3])

slider12 = Slider(**Principal_Slider_Arg, name=inputs[4])
slider22 = Slider(**Payment_Slider_Arg, name=inputs[5])
slider32 = Slider(**Principal_Slider_Arg, name=inputs[6])
slider42 = Slider(**Payment_Slider_Arg, name=inputs[7])

slider13 = Slider(**Balloon_Slider_Arg, name=inputs[8])
slider23 = Slider(**Balloon_Slider_Arg, name=inputs[9])
slider33 = Slider(**Payment_Slider_Arg, name=inputs[10])
slider43 = Slider(**Balloon_Slider_Arg, name=inputs[11])

paymentSliders = [slider11, slider12, slider13]
principalSliders = [slider21, slider22, slider23]
balloonSliders = [slider31, slider32, slider33]
rateSliders = [slider41, slider42, slider43]

# Outputs components
payment = html.Div(id=name + "payment", style=text_style)
principal = html.Div(id=name + "principal", style=text_style)
balloon = html.Div(id=name + "balloon", style=text_style)
rate = html.Div(id=name + "rate", style=text_style)

paymentLabel = dbc.Col(dbc.Label("Payment", html_for=name + "payment"), md=6)
principalLabel = dbc.Col(dbc.Label("Principal", html_for=name + "principal"), md=6)
balloonLabel = dbc.Col(dbc.Label("Balloon", html_for=name + "balloon"), md=6)
rateLabel = dbc.Col(dbc.Label("Annual Rate", html_for=name + "rate"), md=6)

payment = dbc.Row([paymentLabel, dbc.Col(payment, md=6)])
principal = dbc.Row([principalLabel, dbc.Col(principal, md=6)])
balloon = dbc.Row([balloonLabel, dbc.Col(balloon, md=6)])
rate = dbc.Row([rateLabel, dbc.Col(rate, md=6)])

left = dbc.Col([slider0], md=5)
middle = dbc.Col(label, width=dict(size=2), className="offset-md-1")
right = dbc.Col([radio0], md=3)

header = dbc.Row([left, middle, right], align="center")

paymentCol = dbc.Col(
    [
        dbc.Row(dbc.Col(mybadge("Payment"), width={"size":4}, className="offset-md-4")),
        html.Br(),
        *paymentSliders,
        html.Br(),
        payment
    ],
    xs=3
)
principalCol = dbc.Col(
    [
        dbc.Row(dbc.Col(mybadge("Principal"), width={"size":4}, className="offset-md-4")),
        html.Br(),
        *principalSliders,
        html.Br(),
        principal
    ],
    xs=3
)

balloonCol = dbc.Col(
    [
        dbc.Row(dbc.Col(mybadge("Balloon"), width={"size":4}, className="offset-md-4")),
        html.Br(),
        *balloonSliders,
        html.Br(),
        balloon
    ],
    xs=3
)

rateCol = dbc.Col(
    [
        dbc.Row(dbc.Col(mybadge("Rate"), width={"size":4}, className="offset-md-4")),
        html.Br(),
        *rateSliders,
        html.Br(),
        rate
    ],
    xs=3
)

row = dbc.Row([paymentCol, principalCol, balloonCol, rateCol], align="top")
layout = html.Div([header, html.Hr(), row])

outputs = [Output(i, "children") for i in outputs]
inputs = [Input(name + "termtype", "value"), Input(name + "term", "value")] + [
    Input(i, "value") for i in inputs
]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)


def figtbl(termtype, term, a11, a21, a31, a41, a12, a22, a32, a42, a13, a23, a33, a43):

    # Change the rate to decimal representation
    a11 /= 100
    a21 /= 100
    a31 /= 100

    # Monthly rate
    if termtype == "Monthly":
        a11 /= 12
        a21 /= 12
        a31 /= 12
        term *= 12

    ########
    # A note on the sign of the numbers
    ########
    # In the website, the POSITIVE values of the following means
    #   For payment, it is the amount a borrower pays
    #   For principal , it is the amount a borrower receives.
    #   For balloon, it is the amount a borrower pays

    payment = -npf.pmt(rate=a11, nper=term, pv=a12, fv=-a13)
    principal = npf.pv(rate=a21, nper=term, pmt=-a22, fv=-a23)
    balloon = -npf.fv(rate=a31, nper=term, pv=a32, pmt=-a33)
    rate = npf.rate(nper=term, pmt=a42, pv=-a41, fv=a43)
    # Monthly rate
    if termtype == "Monthly":
        rate *= 12

    # return should be in the order of variables list
    return (
        "{:.2%}".format(rate),
        "${:,.2f}".format(principal),
        "${:,.2f}".format(payment),
        "${:,.2f}".format(balloon),
    )
