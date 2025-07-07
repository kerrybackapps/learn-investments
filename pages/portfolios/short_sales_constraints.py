from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.short_sales_constraints_figtbl import figtbl
from pages.formatting import Slider, Layout, text_style, ricegrey

title = "Effect of short sales constraints"
runtitle = None
chapter = "Portfolios"
chapter_url = "portfolios"

urls = {"Python notebook": None}

text = """ 
    It may sometimes be possible to improve mean-variance efficiency by selling some assets short. In practice, 
    there are limitations on short selling: it may not be possible to use the proceeds from
    a short sale to buy other risky assets, less than full interest may be earned on the proceeds, and 
    a fee must be paid to borrow the asset being shorted.  On this page, we ignore those issues.   We assume there is
    no borrowing or lending, and we assume that proceeds
    from short sales are invested in the other risky assets.  Portfolio expected returns and risks are calculated
    based on the inputs below.  
    
    The figure
    shows the mean-variance improvement possible by shorting. The 
    blue curve
    shows the minimum variance possible for a given expected return when short sales are possible 
    under ideal conditions as described above and  there is no borrowing or lending.  The blue
    dot shows the global minimum variance (GMV) portfolio, which is the lowest-risk portfolio that is fully 
    invested
    in the risky assets.  The green curve and green dot show the same things when short sales are not allowed, again
    with no borrowing or lending.  The distance between the blue and green curves (the benefit of short selling) is larger
    when there are assets or portfolios that are highly correlated and have different expected returns (short the low
    expected return portfolio and go long the high expected return portfolio).
    
    If is possible to enter a group of correlations that is physically 
    impossible.  Correlations $c_{12}$, $c_{13}$, and $c_{23}$ between any three 
    assets must satisfy the 
    inequalities $c_{23} \\ge c_{12}c_{13} - \sqrt{(1-c_{12}^2)(1-c_{13}^2)}$ 
    and $c_{23} \\le c_{12}c_{13} + \sqrt{(1-c_{12}^2)(1-c_{13}^2)}$.  Correlations
    that violate these inequalities are physically impossible.  If either of the inequalities holds as an 
    equality, then the assets are linearly related, meaning that one asset is perfectly correlated with a portfolio
    of the other two.  
    
    
    """
name = "frontiers"
inputs = [name + "input" + str(i) for i in range(9)]

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

graph = dcc.Graph(id=name + "fig")

badge = html.H5(dbc.Badge("Results", className="ms-1"))
badge = dbc.Col(badge, xs=12, sm=12, md=4, lg=4, xl=4, width={"offset": 5})
badge = dbc.Row(badge, gutter=3)

left   = dbc.Col([slider1, slider2, slider3], xs=12, sm=12, md=4, lg=4, xl=4)
middle = dbc.Col([slider4, slider5, slider6], xs=12, sm=12, md=4, lg=4, xl=4)
right  = dbc.Col([slider7, slider8, slider9], xs=12, sm=12, md=4, lg=4, xl=4)
row = dbc.Row([left, middle, right], align="center", gutter=3)

col1 = dbc.Col(
    html.Div('Correlations are physically possible and assets are not linearly related?'),
    xs=12, sm=12, md=8, lg=8, xl=8, width={'offset': 2}
)
col2 = dbc.Col(
    html.Div(id=name+'PDCov', style=text_style),
    xs=12, sm=12, md=2, lg=2, xl=2
)
row2 = dbc.Row([col1, col2], gutter=3)

body = dbc.Container(html.Div([row, html.Hr(),
                 row2, html.Hr(),
                 graph]))

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + "fig", "figure"), Output(name + "PDCov", "children")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(*args)
