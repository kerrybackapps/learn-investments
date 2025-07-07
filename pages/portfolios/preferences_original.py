from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.preferences_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Preferences"
chapter = "Portfolios"
chapter_url = chapter.lower()
name = "preferences"
#

urls = None
runtitle = None

text = """ 
    Define the utility of a risky investment to be the expected return minus a penalty for variance equal 
    to  $(1/2) \\times A \\times \\text{variance}$, where $A$ represents an investor's risk aversion.  More risk averse
    investors have higher values for $A$, meaning that they put greater penalties on variance. A utility of, 
    for example, 10% means that the investor would be indifferent between the risky investment and a risk-free 
    investment with a return of 10%.  Setting all risk aversions to be the same and varying utility levels, we 
    see from the figure that higher utility is achieved with either a higher expected return or lower risk or 
    both.  Setting all utility levels to be the same, we see from the figure that a higher expected return is 
    required to reach the utility for a given level of risk when risk aversion is higher, 
    and the extra expected return increases when risk increases.
"""



########## INPUTS
inputs = [name + "input" + str(i) for i in range(6)]
slider1 = Slider(
    "Risk Aversion 1",
    mn=1,
    mx=10,
    step=1,
    value=2,
    tick=1,
    kind="tip",
    name=inputs[0],
)
slider2 = Slider(
    "Risk Aversion 2",
    mn=1,
    mx=10,
    step=1,
    value=2,
    tick=1,
    kind="tip",
    name=inputs[1],
)
slider3 = Slider(
    "Risk Aversion 3",
    mn=1,
    mx=10,
    step=1,
    value=2,
    tick=1,
    kind="tip",
    name=inputs[2],
)
slider4 = Slider(
    "Utility Level 1",
    mn=2,
    mx=20,
    step=2,
    value=8,
    tick=2,
    kind="pct",
    name=inputs[3],
)
slider5 = Slider(
    "Utility Level 2",
    mn=2,
    mx=20,
    step=2,
    value=10,
    tick=2,
    kind="pct",
    name=inputs[4],
)
slider6 = Slider(
    "Utility Level 3",
    mn=2,
    mx=20,
    step=2,
    value=12,
    tick=2,
    kind="pct",
    name=inputs[5],
)


########## OUTPUTS
graph = dcc.Graph(id=name + "fig")


########## PAGE LAYOUT
# Top row - inputs
left0  = dbc.Col([slider1, slider2, slider3], xs=12, sm=12, md=6, lg=6, xl=6)
right0 = dbc.Col([slider4, slider5, slider6], xs=12, sm=12, md=6, lg=6, xl=6)
row0 = dbc.Row([left0, right0], align='center', gutter=3)

# 2nd row - figures
row1 = dbc.Row(graph, align='center', gutter=3)

# Combine rows
body = dbc.Container(html.Div([row0, html.Br(), row1]))

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + "fig", "figure")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(*args)
