import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, dash_table
from dash.dash_table import DataTable
from pages.risk.correlations_figtbl import figtbl
from datetime import date
from pages.formatting import Layout, style_header, style_data, style_data_conditional, css_no_header

title = "Inflation and returns"
runtitle = None
chapter = "Risk and Return"
chapter_url = "risk"

urls = None

text = """ Correlations and scatter plots are shown for the U.S. inflation rate (% change in CPI-All Urban) 
           and nominal returns of the S&P 500, corporate
           bonds, Treasury bonds, Treasury bills, and gold.  The correlations are computed from annual data
           over the range of dates specified.  The CPI data is from [Federal Reserve
           Economic Data](https://fred.stlouisfed.org/series/CPIAUCSL).  The gold return is the percent change in the
           London fixing, which is obtained 
           from [Nasdaq Data Link](https://data.nasdaq.com/data/LBMA/GOLD-gold-price-london-fixing). The other
           return data is provided by [Aswath Damodaran](https://pages.stern.nyu.edu/~adamodar/).
"""

name = "inflation-corr"
today = date.today().year - 1

slider = dcc.RangeSlider(
    id=name + "dates",
    min=1968,
    max=today,
    step=1,
    value=[1968, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = dbc.Col(
    [dbc.Label("Select date range"), slider],
    width={"size": 6, "offset": 3},
)
slider = dbc.Row(slider)

tbl = DataTable(
    id=name + "tbl",
    columns=[
        {"name": "col1", "id": name + "col1"},
        {"name": "col2", "id": name + "col2"}
    ],
    css=css_no_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)

figs = [dcc.Graph(id=name+'fig'+str(i)) for i in range(1,6)]
cols = [dbc.Col(fig, md=5) for fig in figs[:2]] + [dbc.Col(fig, md=4) for fig in figs[2:]]

tbl = dbc.Col([dbc.Label('Correlation with inflation'), tbl], md=2)

row1 = dbc.Row([tbl] + cols[:2], align='top')
row2 = dbc.Row(cols[2:], align='top')

body = html.Div([slider, html.Br(), html.Hr(), row1, html.Br(), row2])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name+'fig'+str(i), 'figure') for i in range(1,6)] + [Output(name + "tbl", "data")]
lst = outputs + [Input(name + "dates", "value")]
@callback(*lst)
def call(dates):
    return figtbl(name, dates)


