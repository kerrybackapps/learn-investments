import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.portfolios.optimal_short_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Optimal portfolios with short sales"
runtitle = "Optimal Short Sales"
chapter = "Portfolios"
chapter_url = "portfolios"
urls = {"Python notebook": None}

text = """
    Optimal portfolios are shown for various levels of risk aversion, assuming short sales are possible under
    the ideal conditions described on the "Frontier with Short Sales" page.  We model risk aversion as a 
    penalty on variance
    in a standard formulation: a portfolio is optimal if the
    portfolio maximizes 'expected return - (1/2) x risk aversion x variance.' Risk aversion is a number that
    is usually 
    assumed to be between 2 and 10.
    
    It is assumed that the investor
    can either save or borrow risk-free, at possibly different rates.  If the borrowing rate exceeds the savings
    rate, two special portfolios are shown in green.  An investor who is highly risk averse will choose to save
    some funds at the risk-free savings rate.  Such an investor should hold a delevered version of the "efficient
    low-risk portfolio," meaning that her relative weights on risky assets should be the same as in that 
    portfolio.  In other words, she just holds a scaled-down version of the portfolio.  An investor who is not
    very risk averse will choose to borrow at the borrowing rate.  Such an investor should hold a levered (scaled
    up) version of the "efficient high-mean portfolio."  The optimal portfolios between the green dots involve
    neither saving nor borrowing.  If the borrowing rate is the same as the savings rate, then there is just one
    special portfolio, and all investors should hold levered or delevered versions of that portfolio, which is
    called the "tangency portfolio."  When the borrowing rate is higher than the savings rate, the figure
    shows two dotted lines, which are infeasible, because they represent borrowing at the savings rate and saving
    at the borrowing rate.
    """
name = "optimal-short"

inputs = [name + "input" + str(i) for i in range(11)]
slider1 = Slider(
    "Expected return of asset 1",
    mn=5,
    mx=20,
    step=1,
    value=6,
    tick=5,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Expected return of asset 2",
    mn=5,
    mx=20,
    step=1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[1],
)
slider3 = Slider(
    "Expected return of asset 3",
    mn=5,
    mx=20,
    step=1,
    value=12,
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
    mn=-50,
    mx=100,
    step=1,
    value=20,
    tick=50,
    kind="pct",
    name=inputs[6],
)
slider8 = Slider(
    "Correlation of asset 1 with asset 3",
    mn=-50,
    mx=100,
    step=1,
    value=40,
    tick=50,
    kind="pct",
    name=inputs[7],
)
slider9 = Slider(
    "Correlation of asset 2 with asset 3",
    mn=-50,
    mx=100,
    step=1,
    value=20,
    tick=50,
    kind="pct",
    name=inputs[8],
)
slider10 = Slider(
    "Savings rate", mn=0, mx=5, step=0.1, value=2, tick=1, kind="pct", name=inputs[9]
)
slider11 = Slider(
    "Excess of borrowing over savings rate",
    mn=0,
    mx=5,
    step=0.1,
    value=3,
    tick=1,
    kind="pct",
    name=inputs[10],
)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider2, slider3, slider10], md=4)
middle = dbc.Col([slider4, slider5, slider6, slider11], md=4)
right = dbc.Col([slider7, slider8, slider9], md=4)
row = dbc.Row([left, middle, right], align="top")
body = html.Div([row, html.Br(), graph])

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
