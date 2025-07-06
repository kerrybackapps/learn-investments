import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.performance_evaluation.market_timing_figtbl import figtbl
from pages.formatting import (
    Layout,
    Slider,
    myinput,
    text_style
)

title       = "Market timing"
runtitle    = None
chapter     = "Topics"
chapter_url = "topics"
urls        = None
text = """
        A random sample of 120 monthly fund excess returns are generated 
        assuming $r_{t} - r_{ft} = a + b (r_{mt} - r_{ft}) + c (r_{mt} - r_{ft})^+ + \\varepsilon_{t}.$  The 
        market excess return $r_{mt} - r_{ft}$ is normally distributed with (annual) mean of 5% and standard 
        deviation of 20%.  The error term $\\varepsilon_{t}$ is also normally distributed with mean zero and 
        annual standard deviation of 5%.  This data-generating process is the Henriksson-Merton market-timing 
        model.  Positive values of $c$ correspond to market-timing ability, while negative values 
        indicate perverse market timing.  Fund performance is evaluated by running a market model 
        regression and a Henriksson-Merton market timing regression on the simulated data.  The estimates 
        are reported above the figure and are reflected in the plotted lines in the figure.  Observe that 
        higher market timing ability results in higher CAPM alpha estimates, all else equal.  Click the button 
        above the output to simulate a new sample.
        """
name = "market_timing"


##### INPUTS
inputs = [name + "input" + str(i) for i in range(3)]

slider1 = Slider(
    "a",
    mn=-5,
    mx=5,
    step=0.5,
    value=0,
    tick=1,
    name=inputs[0],
    kind="pct",
)
slider2 = Slider(
    "b",
    mn=0,
    mx=3,
    step=0.5,
    value=0,
    tick=1,
    name=inputs[1],
    kind=None,
)
slider3 = Slider(
    "c",
    mn=-1,
    mx=1,
    step=0.25,
    value=1,
    tick=0.5,
    name=inputs[2],
    kind=None,
)

btn = dbc.Button(
    "Click to Simulate",
    id=name + "btn",
    n_clicks=0,
    color="primary",
    className="me-1",
)

graph = dcc.Graph(id=name + "fig")


##### PAGE SETUP
col1 = dbc.Col(slider1, md=4)
col2 = dbc.Col(slider2, md=4)
col3 = dbc.Col(slider3, md=4)
row1 = dbc.Row([col1, col2, col3])
row2 = dbc.Row(dbc.Col(btn, width=dict(size=2, offset=5)))

# CAPM alpha
capm_alpha = html.Div(id=name + "a_mm", style=text_style)
capm_alphaLabel = dbc.Col(dbc.Label("CAPM alpha (annualized)", html_for=name + "a_mm"), xs=6)
capm_alpha = dbc.Row([capm_alphaLabel, dbc.Col(capm_alpha, xs=6)])

# CAPM beta
capm_beta = html.Div(id=name + "b_mm", style=text_style)
capm_betaLabel = dbc.Col(dbc.Label("CAPM beta", html_for=name + "b_mm"), xs=6)
capm_beta = dbc.Row([capm_betaLabel, dbc.Col(capm_beta, xs=6)])
"""

capm_labels = dbc.Col(
    [
        dbc.Label("CAPM alpha (annualized)", html_for=name + "a_mm"), 
        dbc.Label("CAPM beta", html_for=name + "b_mm"), 
    ]
)
capm_estimates = dbc.Col(
    [
        html.Div(id=name + "a_mm", style=text_style),
        html.Div(id=name + "b_mm", style=text_style)
    ]
)

capm = dbc.Row(
    [capm_labels, capm_estimates]
)
"""
# HM alpha
hm_alpha = html.Div(id=name + "a_hm", style=text_style)
hm_alphaLabel = dbc.Col(dbc.Label("Henriksson-Merton intercept (annualized)", html_for=name + "a_hm"), xs=6)
hm_alpha = dbc.Row([hm_alphaLabel, dbc.Col(hm_alpha, xs=6)])

# HM beta
hm_beta = html.Div(id=name + "b_hm", style=text_style)
hm_betaLabel = dbc.Col(dbc.Label("Henriksson-Merton market loading", html_for=name + "b_hm"), xs=6)
hm_beta = dbc.Row([hm_betaLabel, dbc.Col(hm_beta, xs=6)])

# HM gamma
hm_gamma = html.Div(id=name + "g_hm", style=text_style)
hm_gammaLabel = dbc.Col(dbc.Label("Henriksson-Merton market timing coefficient", html_for=name + "g_hm"), xs=6)
hm_gamma = dbc.Row([hm_gammaLabel, dbc.Col(hm_gamma, xs=6)])

col1 = dbc.Col([capm_alpha, capm_beta], xs=6)
col2 = dbc.Col([hm_alpha, hm_beta, hm_gamma], xs=6)
row3 = dbc.Row([col1, col2])



row4 = dbc.Row(dbc.Col(graph, md=12), align="center")


body = html.Div([row1, html.Br(), row2, html.Hr(), row3, html.Hr(), row4])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

# outputs = [
#     Output(name + "fig", "figure")
# ]
# inputs = [Input(i, "value") for i in inputs]
# lst = outputs + inputs
# @callback(*lst)

@callback(
    Output(name+"fig", "figure"),
    Output(name + "a_mm", "children"),
    Output(name + "b_mm", "children"),
    Output(name + "a_hm", "children"),
    Output(name + "b_hm", "children"),    
    Output(name + "g_hm", "children"),    
    Input(name + "btn", "n_clicks"),
    *[Input(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(*args)
