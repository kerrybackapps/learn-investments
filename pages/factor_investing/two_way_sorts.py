from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.factor_investing.two_way_sorts_figtbl import figtbl, chars
from pages.formatting import Layout, tab_style, tab_selected_style, lightblue
from datetime import date

today = date.today().year

title = "Two-way sorts"
runtitle = None
chapter = "Factors"
chapter_url = "factor-investing"

urls = None
text = """
    Stocks are independently sorted into quintiles on market equity and on another characteristic, and monthly returns
    are calculated for the 25 value-weighted
    portfolios formed from the intersection of the sorts.  The portfolio return data comes from
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  The 
    definitions of the characteristics and the
    details of the portfolio constructions can be found there.  The book-to-market, momentum, and reversal data begins in 1926, and the other 
    characteristic data starts in 1963.  The market equity quintiles are designated ME1, ME2, ME3, ME4, and ME5, 
    from smallest to largest.  The other characteristic quintiles are also designated 1 through 5,
    from smallest values of the characteristic to largest.
    
    Mean returns in excess of the risk-free rate and Sharpe ratios
    are tabulated.  The figures at the bottom of the page show the compound returns of the corner portfolios: ME1
    (small cap) intersected with the lowest characteristic quintile, ME1 intersected with the highest characteristic 
    quintile, ME5 (large cap) intersected with the lowest characteristic quintile, and ME5 intersected with the highest
    characteristic quintile.
    """

name = "two-way-sorts"

drop = dcc.Dropdown(chars, placeholder="Select a characteristic", id=name + "char", style={"backgroundColor": lightblue})
drop = html.Div([dbc.Label("Characteristic"), drop])

slider = dcc.RangeSlider(
    id=name + "dates",
    min=1926,
    max=today,
    step=1,
    value=[1980, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Date Range"), slider])

left = dbc.Col(drop, md=6)
right = dbc.Col(slider, md=6)
row = dbc.Row([left, right], align="center")

body = html.Div(
    [
        row,
        html.Br(),
        dcc.Loading(html.Div(id=name+'content'), id=name+'loading', type='circle')
    ]
)

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

CONTENT = dict(
    char=None,
    dates=None,
    means=None,
    alphas=None,

)

@callback(
    Output(name+'content', 'children'),
    Input(name+'char', 'value'),
    Input(name+'dates', 'value'),
    prevent_initial_call=True
)
def call(char, dates):
    global CONTENT
    if (char!=CONTENT['char']) or (dates!=CONTENT['dates']):
        CONTENT = figtbl(char, dates)
    return CONTENT["means"]

