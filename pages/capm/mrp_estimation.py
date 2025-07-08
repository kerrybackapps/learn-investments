import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.capm.mrp_estimation_figtbl import figtbl
from pages.formatting import (
    Slider,
    Layout,
    style_header,
    style_data_conditional,
)

title = "Estimating the market risk premium"
chapter = "Capital Asset Pricing Model"
chapter_url = "capm"
runtitle = None
urls = None
name = "mrp_estimation"

text = """ 
    This page examines variability in estimating the market risk premium from 
    historical data.  The left-hand plot shows how the range of possible market risk 
    premium estimates (specifically, the 5th and 95th percentiles) changes as a function 
    of the number of years of historical monthly data used to estimate the market 
    risk premium.  Returns each period are assumed to be normally distributed with 
    mean and standard deviations controlled by the left-hand sliders.  The right-hand 
    plot shows the empirical estimates and the 90 percent confidence interval obtained by estimating
    the market risk premium over a rolling window.  The
    length of the window is controlled by the slider on the right.
    """




########## INPUTS
inputs = [name + "input" + str(i) for i in range(3)]
slider1 = Slider(
    "Expected return",
    mn=0,
    mx=12,
    step=1,
    value=5,
    tick=3,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Standard deviation",
    mn=0,
    mx=20,
    step=1,
    value=15,
    tick=5,
    kind="pct",
    name=inputs[1],
)

slider3 = Slider(
    "Length of Estimation Window (Years)",
    mn=5,
    mx=40,
    step=5,
    value=20,
    tick=None,
    kind="tip",
    name=inputs[2],
)


########## OUTPUTS
sim_graph = dcc.Graph(id=name + "simfig")
data_graph = dcc.Graph(id=name + "datafig")



########## PAGE LAYOUT
# Top row - inputs
left0  = dbc.Col([slider1, slider2], xs=12, sm=12, md=6, lg=6, className="mb-2")
right0 = dbc.Col([slider3], xs=12, sm=12, md=6, lg=6, className="mb-2")
row0 = dbc.Row([left0, right0], align='center', className="gx-1")

# 2nd row - figures
left1  = dbc.Col(sim_graph, xs=12, sm=12, md=6, lg=6, className="mb-2")  
right1 = dbc.Col(data_graph, xs=12, sm=12, md=6, lg=6, className="mb-2")
row1 = dbc.Row([left1,right1],align='center', className="gx-1")

# Combine rows
# body = html.Div([btn, row0, html.Hr(), html.Br(), text1, row1, html.Br(), text2, row2, html.Br(), text3, row3])
body = dbc.Container([row0, html.Br(), row1], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name + f, "figure") for f in ["simfig", "datafig"]]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs

@callback(*lst)
def call(*args):
    return figtbl(*args)
