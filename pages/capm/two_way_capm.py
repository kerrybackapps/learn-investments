from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.capm.two_way_capm_figtbl import figtbl, chars
from pages.formatting import Layout, tab_style, tab_selected_style, lightblue
from datetime import date

today = date.today().year

title = "CAPM for two-way sorts"
runtitle = None
chapter = "Capital Asset Pricing Model"
chapter_url = "capm"

urls = None
text = """
    Stocks are independently sorted into quintiles on market equity and on another characteristic, and monthly returns
    are calculated for the 25 value-weighted
    portfolios formed from the intersection of the sorts.  The portfolio return data comes from
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  The 
    definitions of the characteristics and the
    details of the portfolio constructions can be found there.  The excess returns are regressed on the market excess 
    return, and alphas and 
    $t$ statistics for the alphas are reported.  The CAPM states that alphas should be zero, so large $t$ 
    statistics of either sign reject the CAPM.  The book-to-market, momentum, and reversal data begins in 1926, and 
    the other 
    characteristic data starts in 1963.  The market equity quintiles are designated ME1, ME2, ME3, ME4, and ME5, 
    from smallest to largest.  The other characteristic quintiles are also designated 1 through 5,
    from smallest values of the characteristic to largest.
    
    In the figure at the bottom of the page, average annualized excess returns (risk premia) are plotted
    against betas in blue. The blue line is the regression line showing the best fit between estimated betas
    and empirical risk premia.  The green points are the theoretical risk premia, based on the CAPM, the
    market risk premium over the date range selected, and the estimated betas.  Hover over the points to see
    the portfolio names.
    """

name = "two-way-capm"

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

left = dbc.Col(drop, xs=12, sm=12, md=6, lg=6, className="mb-2")
right = dbc.Col(slider, xs=12, sm=12, md=6, lg=6, className="mb-2")
row = dbc.Row([left, right], align="center", className="gx-1")

body = dbc.Container(
    [
        row,
        html.Br(),
        dcc.Loading(html.Div(id=name+'content'), id=name+'loading', type='circle')
    ], fluid=True, className="px-1"
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
        CONTENT = figtbl(name, char, dates)

    return CONTENT["alphas"]

