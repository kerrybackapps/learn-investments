from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.optimal_figtbl import figtbl
from pages.formatting import Slider, Layout, text_style

title = "Optimal capital allocation"
chapter = "Portfolios"
chapter_url = chapter.lower()
name = "optimal"
#

urls = None
runtitle = None

text = """ 

    Assume that we can borrow and save at the same risk-free rate and short sales are unconstrained.  If the 
    risk-free rate is below the expected return of the GMV portfolio, then the optimal 
    portfolio is a combination of the tangency portfolio with risk-free borrowing or saving.  The optimal amount
    of borrowing or saving depends on an investor's preferences.  Assume that 
    an investor evaluates a risky investment based on its expected return minus a penalty for variance equal 
    to  $(1/2) \\times A \\times \\text{variance}$, where $A$ represents the investor's risk 
    aversion.  The optimal portfolio is indicated by the star.  The dotted curve is the set of mean/risk combinations 
    that are equally good for the investor (an indifference curve).  When risk aversion is increased, the optimal 
    portfolio shifts to less risky and lower expected return portfolios.  Risk aversion is usually assumed to be 
    between 2 and 10.
    
    It is possible to enter a group of correlations that is physically 
    impossible.  Correlations $c_{12}$, $c_{13}$, and $c_{23}$ between any three 
    assets must satisfy the 
    inequalities $c_{23} \\ge c_{12}c_{13} - \sqrt{(1-c_{12}^2)(1-c_{13}^2)}$ 
    and $c_{23} \\le c_{12}c_{13} + \sqrt{(1-c_{12}^2)(1-c_{13}^2)}$.  Correlations
    that violate these inequalities are physically impossible.  If either of the inequalities holds as an 
    equality, then the assets are linearly related, meaning that one asset is perfectly correlated with a portfolio
    of the other two.  
    """



########## INPUTS
inputs = [name + "input" + str(i) for i in range(11)]
slider1 = Slider(
    "Expected return of asset 1",
    mn=5,
    mx=20,
    step=1,
    value=8,
    tick=5,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Expected return of asset 2",
    mn=5,
    mx=20,
    step=1,
    value=12,
    tick=5,
    kind="pct",
    name=inputs[1],
)
slider3 = Slider(
    "Expected return of asset 3",
    mn=5,
    mx=20,
    step=1,
    value=15,
    tick=5,
    kind="pct",
    name=inputs[2],
)
slider4 = Slider(
    "Standard deviation of asset 1",
    mn=5,
    mx=45,
    step=1,
    value=15,
    tick=10,
    kind="pct",
    name=inputs[3],
)
slider5 = Slider(
    "Standard deviation of asset 2",
    mn=5,
    mx=45,
    step=1,
    value=25,
    tick=10,
    kind="pct",
    name=inputs[4],
)
slider6 = Slider(
    "Standard deviation of asset 3",
    mn=5,
    mx=45,
    step=1,
    value=35,
    tick=10,
    kind="pct",
    name=inputs[5],
)
slider7 = Slider(
    "Correlation of asset 1 with asset 2",
    mn=-100,
    mx=100,
    step=1,
    value=15,
    tick=50,
    kind="pct",
    name=inputs[6],
)
slider8 = Slider(
    "Correlation of asset 1 with asset 3",
    mn=-100,
    mx=100,
    step=1,
    value=60,
    tick=50,
    kind="pct",
    name=inputs[7],
)
slider9 = Slider(
    "Correlation of asset 2 with asset 3",
    mn=-100,
    mx=100,
    step=1,
    value=30,
    tick=50,
    kind="pct",
    name=inputs[8],
)

slider10 = Slider(
    "Risk-free rate",
    mn=0,
    mx=5,
    step=0.1,
    value=2,
    tick=1,
    kind="pct",
    name=inputs[9],
)

slider11 = Slider(
    "Risk aversion",
    mn=2,
    mx=10,
    step=0.1,
    value=6,
    tick=2,
    kind=None,
    name=inputs[10],
)



########## OUTPUTS
graph = dcc.Graph(id=name + "fig")

########## PAGE LAYOUT
# Top row - inputs
left   = dbc.Col([slider1, slider2, slider3], xs=12, sm=12, md=4, lg=4, className="mb-2")
middle = dbc.Col([slider4, slider5, slider6], xs=12, sm=12, md=4, lg=4, className="mb-2")
right  = dbc.Col([slider7, slider8, slider9], xs=12, sm=12, md=4, lg=4, className="mb-2")
row1 = dbc.Row([left, middle, right], align="center", className="gx-1")

left = dbc.Col(slider10, xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col(slider11, xs=12, sm=12, md=4, lg=4, className="mb-2")
row2 = dbc.Row([left, right], align="top", className="gx-1")

col1 = dbc.Col(
    html.Div('Correlations are physically possible and assets are not linearly related?'),
    xs=12, sm=12, md=7, lg=7, className="mb-2"
)
col2 = dbc.Col(
    html.Div(id=name+'PDCov', style=text_style),
    xs=12, sm=6, md=1, lg=1, className="mb-2"
)
row3 = dbc.Row([col1, col2], className="gx-1")

label = html.Div("Optimal allocation to risky assets:")
label = dbc.Col(label, xs=12, sm=12, md=4, lg=4, className="mb-2")
alloc = html.Div(id=name + "alloc", style=text_style)
alloc = dbc.Col(alloc, xs=12, sm=6, md=2, lg=2, className="mb-2")

row4 = dbc.Row([label, alloc], align="center", className="gx-1")

# Combine rows
body = dbc.Container([row1, row2, html.Hr(), row3, html.Hr(), row4, html.Br(), graph], fluid=True, className="px-1")

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
    Output(name + "PDCov", "children"),
    Output(name + "alloc", "children"),
    *[Input(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(*args)
