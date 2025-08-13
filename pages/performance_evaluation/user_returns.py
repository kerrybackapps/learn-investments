# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback, State
import dash_bootstrap_components as dbc
from pages.performance_evaluation.user_returns_figtbl import figtbl
from pages.formatting import Layout

title = "Evaluation of user-supplied returns"
runtitle = None
chapter = "Topics"
chapter_url = "performance-evaluation"

urls = None

text = """ 
    Choose a benchmark from the dropdown menu and upload either an Excel workbook or 
    a csv file that contains a column of dates and a column
    of monthly returns, with the dates on the left and the returns in decimal form.  The returns
    are compared to the benchmark on a raw basis and on a beta-adjusted basis and also in the
    presence of other factors: Size, Value, Profitability, Investment, Momentum, Short-Term Reversal,
    and Long-Term Reversal.
    
    The analysis downloads as an html file with four tabs.  The file can be opened in any browser.  One of
    the tabs presents the data (returns, benchmark, and factors).  The other three tabs analyze different
    types of active returns: (i) excess return over the benchmark, (ii) excess return over the beta-adjusted
    benchmark, namely, """ + r'$\\beta r_b + (1-\\beta)r_f$' + """, where $$r_b$$ denotes the benchmark return 
    and $$r_f$$ denotes
    the risk free rate, and (iii) excess return over a beta-weighted combination of the benchmark and the
    factors.  In each case, the mean active return is called an alpha, the standard deviation of the active
    return can be called a tracking error, and the ratio of the alpha to the tracking error is called 
    an information ratio.  When the benchmark is the market index, the alpha in case (ii) is the CAPM alpha.
    
    The market index benchmark is the monthly market return 
    from [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html). The
    benchmark ETF
    returns are calculated on a monthly basis from the adjusted closing prices provided by Yahoo Finance.  The factors come from 
    French's Data Library.
    
    """

name = "user-returns"

etfs = [
    'Market Index',
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

drop = dcc.Dropdown(etfs, placeholder="Select a benchmark", id=name+'drop')

upload = dcc.Upload(
    id=name+"upload-data",
    children=html.Div("Drag and Drop or Select the Return File"),
    style={
        "width": "100%",
        "height": "60px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "margin": "10px",
    },
    # Allow multiple files to be uploaded
    multiple=False,
)


drop = dbc.Col([dbc.Label('Benchmark'), drop], md=6)
upload = dbc.Col(upload, md=6)

row = dbc.Row([drop, upload])

download = html.Div([dcc.Download(id=name + "download")])
download = dcc.Loading(download,id=name+'loading', type='circle')

body = html.Div([row, download])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [
    Output(name + "download", "data"),
    Input(name+'drop', 'value'),
    Input(name+"upload-data", "contents"),
    State(name+"upload-data", "filename"),
    State(name+"upload-data", "last_modified"),
]


@callback(*lst, prevent_initial_call=True)
def call(*args):
    filename = figtbl(*args)
    return dcc.send_file('./tmp/' + filename)

