from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.optimal_two_rates_figtbl import figtbl
from pages.formatting import Slider, Layout, text_style

title = "Optimal capital allocation with different rates"
chapter = "Portfolios"
chapter_url = chapter.lower()
name = "preferences_risky"
#

urls = None
runtitle = None

text = """ 

    Assume that the rate at which we can borrow is higher than the rate at which we can save, and assume short
    sales are unconstrained.  The green curve in the figure on the left shows the portfolio mean/risk combinations that
    are can be obtained from portfolios of the risky assets without borrowing or saving.  
    
    Assume the savings rate is below the expected return of the GMV portfolio (which is the height of the green curve
    at its leftmost point).  If the
    borrowing rate is also below the expected return of the GMV portfolio, then there are two tangency portfolios,
    one at the savings rate and one at the borrowing rate, and the efficient frontier consists of three
    regions: (1) a savings region in which the risky asset portfolio is the savings-rate tangency portfolio, (2) a 
    fully invested region in which there is no borrowing or saving and the risky asset portfolio is a combination of the
    two tangency portfolios, and (3) a borrowing region in which the risky asset portfolio is the borrowing-rate
    tangency portfolio.  The first and third regions are indicated by the two blue line segments in the figure on the
    left, and the second region is the segment of the green curve that connects them.  The two tangency portfolios are
    indicated by green dots.  At high levels of risk aversion, the optimal portfolio is in the first region; at 
    intermediate levels, it is in the second region; and at low levels, it is in the third region.  The total
    allocation to risky assets is higher for lower risk aversion.
    
    If the borrowing rate is above the expected return of the GMV portfolio, then the third region does not exist,
    because it is not efficient to borrow at such a high rate.  Instead, for low levels of risk aversion, an investor
    should maintain a 100% investment in the risky assets, possibly  shorting low
    expected return assets to generate high expected portfolio returns.
    
    To identify optimal portfolios, we assume that 
    an investor evaluates a risky investment based on its expected return minus a penalty for variance equal 
    to  $(1/2) \\times A \\times \\text{variance}$, where $A$ represents the investor's risk 
    aversion.  Risk aversion is usually assumed to be 
    between 2 and 10.  The optimal portfolio in the figure on the left 
    is indicated by the star.  The dotted curve is the set of 
    mean/risk combinations 
    that are equally good for the investor (an indifference curve). 
    
    The figure on the right shows the three (or two) regions of efficient portfolios.  For high levels of risk aversion,
    the allocation to risky assets is less than 100%, the remainder being saved at the savings rate (region 1).  For
    intermediate levels of risk aversion, the allocation is 100% (region 2).  For low levels of risk aversion, the 
    allocation is greater than 100% (region 3) and the excess is borrowed if the borrowing rate is below the expected 
    return of the GMV portfolio, and the allocation stays at 100% if the borrowing rate is higher. 
    """




########## INPUTS
inputs = [name + "input" + str(i) for i in range(12)]
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
    "Savings rate",
    mn=0,
    mx=5,
    step=0.1,
    value=2,
    tick=1,
    kind="pct",
    name=inputs[9],
)

slider11 = Slider(
    "Excess of borrowing over savings rate",
    mn=1,
    mx=5,
    step=0.1,
    value=3,
    tick=1,
    kind="pct",
    name=inputs[10],
)

slider12 = Slider(
    "Risk aversion",
    mn=2,
    mx=10,
    step=0.1,
    value=6,
    tick=2,
    kind=None,
    name=inputs[11],
)



########## OUTPUTS
fig1 = dcc.Graph(id=name + "fig1")
fig2 = dcc.Graph(id=name + "fig2")

########## PAGE LAYOUT
# Top row - inputs
left   = dbc.Col([slider1, slider2, slider3, slider10], xs=12, sm=12, md=4, lg=4, className="mb-2")
middle = dbc.Col([slider4, slider5, slider6, slider11], xs=12, sm=12, md=4, lg=4, className="mb-2")
right  = dbc.Col([slider7, slider8, slider9, slider12], xs=12, sm=12, md=4, lg=4, className="mb-2")
row1 = dbc.Row([left, middle, right], align="center", className="gx-1")

col1 = dbc.Col(
    html.Div('Correlations are physically possible and assets are not linearly related?'),
    xs=12, sm=12, md=7, lg=7, className="mb-2"
)
col2 = dbc.Col(
    html.Div(id=name+'PDCov', style=text_style),
    xs=12, sm=6, md=1, lg=1, className="mb-2"
)
row2 = dbc.Row([col1, col2], className="gx-1")

label = html.Div("Optimal allocation to risky assets:")
label = dbc.Col(label, xs=12, sm=12, md=4, lg=4, className="mb-2")
alloc = html.Div(id=name + "alloc", style=text_style)
alloc = dbc.Col(alloc, xs=12, sm=12, md=5, lg=5, className="mb-2")
alloc = dbc.Row([label, alloc], className="gx-1")

fig1 = dbc.Col([alloc, fig1], xs=12, sm=12, md=8, lg=8, className="mb-2")
fig2 = dbc.Col(fig2, xs=12, sm=12, md=4, lg=4, className="mb-2")
row3 = dbc.Row([fig1, fig2], align="top", className="gx-1")
# Combine rows
body = dbc.Container([row1, html.Hr(), row2, html.Hr(), row3], fluid=True, className="px-1")

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
    Output(name + "fig1", "figure"),
    Output(name + "fig2", "figure"),
    Output(name + "PDCov", "children"),
    Output(name + "alloc", "children"),
    *[Input(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(*args)