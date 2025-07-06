import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State, callback
from pages.formatting import Layout, tab_style, tab_selected_style, myinput, lightblue
from pages.performance_evaluation.funds_figtbl import figtbl

title = 'Evaluation of mutual funds'
runtitle = None
chapter = "Topics"
chapter_url = 'topics'
urls = None

from datetime import date
today = date.today().year

text = """
    Enter a mutual fund or other ticker, select a benchmark against which to compare the fund, and
    select a date range for the analysis.  The fund returns are compared to the benchmark returns
    over the date range specified (or the largest subset of the range in which both the fund and the 
    benchmark existed).  The returns
    are compared on a raw basis and on a beta-adjusted basis and also in the
    presence of other factors: Size, Value, Profitability, Investment, Momentum, Short-Term Reversal, 
    and Long-Term Reversal.
    
    The three tabs analyze three different
    types of active returns: (i) excess return over the benchmark, (ii) excess return over the beta-adjusted
    benchmark, namely, """ + r'$\beta r_b + (1-\beta)r_f$' + """, where $$r_b$$ denotes the benchmark return 
    and $$r_f$$ denotes
    the risk free rate, and (iii) excess return over a beta-weighted combination of the benchmark and the
    factors.  In each case, the mean active return is called an alpha, the standard deviation of the active
    return can be called a tracking error, and the ratio of the alpha to the tracking error is called 
    an information ratio.  When the benchmark is the market index, the alpha in case (ii) is the CAPM alpha.
    
    The market index benchmark is the monthly
    market return from  [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html). The
    mutual fund and benchmark ETF
    returns are calculated on a monthly basis from the adjusted closing prices provided by Yahoo Finance.  The factors come from 
    French's Data Library.  
    """

name = 'funds'

#
# Input  for date range
slider = dcc.RangeSlider(
    id=name + "dates",
    min=1970,
    max=today,
    step=1,
    value=[1980, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Select date range", html_for=name + "slider"), slider])

# Input ticker
inpt = dcc.Input(id=name+'ticker', type='text', placeholder='Enter a ticker', debounce=True)

# benchmark

etfs = [
    'SPY = S&P 500 ETF',
    'IVE = S&P 500 Value ETF',
    'IVW = S&P 500 Growth ETF',
    'IWB = Russell 1000 ETF',
    'IWD = Russell 1000 Value ETF',
    'IWF = Russell 1000 Growth ETF',
    'IWM = Russell 2000 ETF',
    'IWN = Russell 2000 Value ETF',
    'IWO = Russell 2000 Growth ETF',
    'IWV = Russell 3000 ETF',
    ]

drop = dcc.Dropdown(
    ['Market Index'] + etfs,
    'Market Index',
    placeholder="Select a benchmark",
    id=name+'benchmark',
    style={"backgroundColor": lightblue}
)

left = dbc.Col([html.Label('Ticker to Analyze'), inpt], md=4)
mid = dbc.Col([html.Label('Benchmark'), drop], md=4)
right = dbc.Col(slider, md=4)
row = dbc.Row([left, mid, right], align='center')

body = html.Div([row, html.Br(),
    dcc.Tabs(
        id=name+'tab',
        value=name+'simple',
        children=
        [
            dcc.Tab(label='Simple benchmark', value=name+'simple', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Beta-adjusted benchmark', value=name+'beta', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Multi-factor analysis', value=name+'multi', style=tab_style, selected_style=tab_selected_style)
        ]
    ),
    html.Br(),
    html.Hr(),
    dcc.Loading(html.Div(id=name+'content'), id=name+'loading', type='circle')
])

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
    ticker=None,
    benchmark=None,
    dates=None,
    simple=None,
    beta=None,
    multi=None
)

@callback(
    Output(name+'content', 'children'),
    Input(name+'ticker', 'n_submit'),
    State(name+'ticker', 'value'),
    Input(name+'benchmark', 'value'),
    Input(name+'dates', 'value'),
    Input(name+'tab', 'value'),
    prevent_initial_call=True
)
def render_content(n_submit, ticker, benchmark, dates, tab):
    global CONTENT
    if n_submit is None:
        return dash.no_update
    if (ticker!=CONTENT['ticker']) or (benchmark!=CONTENT['benchmark']) or (dates!=CONTENT['dates']):
        CONTENT = figtbl(ticker, benchmark, dates)
    kind = 'simple' if tab == name+'simple' else ('beta' if tab == name+'beta' else 'multi')
    return CONTENT[kind]


