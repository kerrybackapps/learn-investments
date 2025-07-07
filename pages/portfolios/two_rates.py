from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.two_rates_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Different borrowing and saving rates"
runtitle = None
chapter = "Portfolios"
chapter_url = "portfolios"

urls = None

text = """ 
    The expected returns and risks of long-only portfolios of two assets are shown.  For each asset, portfolios 
    of the asset with the risk-free savings rate are shown.  The Sharpe ratio is a measure of the excess return 
    of an investment per unit of risk.  The Sharpe ratio is the slope of the line connecting the risk-free rate to 
    a risky portfolio.  The highest Sharpe ratio is obtained by combining the risk-free asset with a risky portfolio 
    so that this slope is as high as possible.  This occurs when the line is tangent to the curve of risky-only 
    portfolios.  Hover over each line representing portfolios of a risky portfolio with risk-free savings to see 
    the Sharpe ratio of combining risk-free saving with a given risky portfolio.

    When interest rates are lower than expected returns, the efficient portfolios (meaning portfolios with minimum
    risk for a given expected return) fall into three regions, separated 
    by green dots indicating an efficient low risk portfolio and an efficient high mean portfolio, both comprised 
    solely of risky assets. To the left of the efficient low risk portfolio, the efficient portfolios are scaled-down 
    versions of the efficient low risk portfolio with some savings. To the right of the efficient high mean portfolio, 
    the efficient portfolios are scaled-up versions of the efficient high mean portfolio with some borrowing. Both cases
    are shown as blue lines in the figure.  The third region is the green curve between the efficient low risk and 
    efficient high mean portfolios.  These portfolios do not involve saving or borrowing.  The blue
    dotted lines extend the blue solid lines, but the points on the blue dotted lines are infeasible, 
    because they involve saving at the 
    borrowing rate or borrowing at the savings rate.  If the borrowing rate equals the savings rate, then the 
    efficient low mean and efficient high risk portfolios are the same, which is called the tangency 
    portfolio, and the third region consists of this single portfolio.  If interest rates are set higher than 
    expected returns, then the efficient portfolios may not exist 
    or may be outside the plotted range.
"""

name = "portfolios2rf"
inputs = [name + "input" + str(i) for i in range(7)]

slider1 = Slider(
    "Expected return of asset 1",
    mn=5,
    mx=20,
    step=1,
    value=5,
    tick=5,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Expected return of asset 2",
    mn=5,
    mx=20,
    step=1,
    value=8,
    tick=5,
    kind="pct",
    name=inputs[1],
)
slider3 = Slider(
    "Standard deviation of asset 1",
    mn=0,
    mx=50,
    step=1,
    value=15,
    tick=10,
    kind="pct",
    name=inputs[2],
)
slider4 = Slider(
    "Standard deviation of asset 2",
    mn=5,
    mx=50,
    step=1,
    value=25,
    tick=10,
    kind="pct",
    name=inputs[3],
)
slider5 = Slider(
    "Correlation of assets",
    mn=-100,
    mx=100,
    step=5,
    value=25,
    tick=50,
    kind="pct",
    name=inputs[4],
)
slider6 = Slider(
    "Savings rate", mn=0, mx=5, step=1, value=2, tick=2, kind="pct", name=inputs[5]
)
slider7= Slider(
    "Excess of borrowing over savings rate",
    mn=0,
    mx=5,
    step=1,
    value=2,
    tick=1,
    kind="pct",
    name=inputs[6],
)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider2, slider3, slider4, slider5, slider6, slider7], xs=12, sm=12, md=4, lg=4, xl=4)
right = dbc.Col(graph, xs=12, sm=12, md=8, lg=8, xl=8)
body = dbc.Container(dbc.Row([left, right], align="center", gutter=3))

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
