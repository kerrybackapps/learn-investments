from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.preferences_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Preferences"
chapter = "Portfolios"
chapter_url = "portfolios"
name = "preferences"

urls = None
runtitle = None

text = """ 
    Define the utility of a risky investment to be the expected return minus a penalty for variance equal 
    to  $(1/2) \\times A \\times \\text{variance}$ for a constant $A$.  Higher values of $A$ mean higher penalties
    for variance, hence higher aversion to risk.  For example, an expected return of 10%, a standard deviation of 20%,
    and $A=4$ implies a utility of $0.1 - (1/2)\\times 4 \\times 0.04 = 0.02$.  Likewise a risk-free return of 2% implies
    a utility of 0.02, so an investor with $A=4$ is indifferent between a risk-free return of 2% and a return with 
    a mean of 10% and a standard deviation of 20%.  The curves in the figure below are sets of 
    (std dev, mean) combinations among which an investor is indifferent, for the specified values of risk 
    aversion.  The direction of increasing preference is up and to the left (higher expected return and/or 
    lower risk).  Risk aversion is usually assumed to be between 2 and 10.
    """



########## INPUTS
inputs = [name + "input" + str(i) for i in range(2)]
slider1 = Slider(
    "Risk Aversion 1",
    mn=2,
    mx=10,
    step=0.1,
    value=4,
    tick=2,
    kind=None,
    name=inputs[0],
)
slider2 = Slider(
    "Risk Aversion 2",
    mn=2,
    mx=10,
    step=0.1,
    value=8,
    tick=2,
    kind=None,
    name=inputs[1],
)


########## OUTPUTS
fig = dcc.Graph(id=name + "fig")

########## PAGE LAYOUT
# Top row - inputs
left  = dbc.Col(slider1, md=6)
right = dbc.Col(slider2, md=6)
row = dbc.Row([left, right], align='center')

body = html.Div([row, html.Br(), fig])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

@callback(
    Output(name + "fig", "figure"),
    *[Input(i, "value") for i in inputs]
)

def call(*args):
    return figtbl(*args)
