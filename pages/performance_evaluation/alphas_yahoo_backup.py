import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.formatting import Layout, style_data, css_no_header, style_data_conditional
from pages.performance_evaluation.alphas_yahoo_figtbl import figtbl
from datetime import date
today = date.today().year - 1

title = 'Mutual Fund Alphas'
runtitle = 'Mutual Fund Alphas'
chapter = "Topics"
chapter_url = chapter.lower()
urls={'Python notebook':'https://github.com/bbcx-investments/notebooks/blob/main/performance-evaluation/alphas_yahoo.ipynb'}

text =    ''' Monthly market returns and the monthly risk-free rate are downloaded from 
              [Ken French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  Monthly
              stock returns for the ticker you input below are computed from data provided by Yahoo Finance.  The monthly excess
              mutual fund returns (return minus risk-free rate) are regressed on the monthly excess market returns for the sample 
              months (controlled with slider below). The alpha is the intercept from the regression and is expressed as an annual
              percent.
              '''

name = 'alphas_yahoo'


# Input for date range
slider = dcc.RangeSlider(
    id=name + "slider",
    min=1970,
    max=today,
    step=1,
    value=[1980, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Select date range", html_for=name + "slider"), slider])
slider = dbc.Row(dbc.Col(slider, width={"size": 6, "offset": 3}))


# Input ticker
inpt = dbc.Input(id=name+'ticker', type='text', placeholder='Enter a ticker')
inpt = html.Div(inpt)

# Output plot
graph = dcc.Graph(id=name+'fig')

# Ouput table with no column names
tbl = DataTable(id=name+'tbl', css=css_no_header, style_data=style_data,
                style_as_list_view=True, style_data_conditional=style_data_conditional)
tbl = dcc.Loading(id=name+'loading', children=tbl, type='circle')


# Page display set-up
left1 = dbc.Col(inpt,md=4)
right1= dbc.Col(slider,md=8)
row1  = dbc.Row([left1,right1], align='top')


left2 = dbc.Col(tbl,md=4)
right2= dbc.Col(graph,md=8)
row2  = dbc.Row([left2,right2], align='top')

body = html.Div([row1,html.Br(),row2])

layout = Layout(title=title, runtitle=runtitle, chapter=chapter, chapter_url=chapter_url, urls=urls, text=text,body=body)
lst = [Output(name+'fig','figure'), Output(name+'tbl','data'), Input(name+'ticker','value'),Input(name+'slider','value')]


@callback(*lst, prevent_initial_call=True)
def call(ticker, dates) :
    return figtbl(ticker,dates)

