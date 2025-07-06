from dash.dependencies import Input, Output
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    text_style,
    style_header,
    style_data,
    style_data_conditional,
    myinput,
    lightblue
)
from pages.futures_options.market_data_figtbl import price_maturities, figtbl

title = "Market option data"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None

text = """This page presents market data on call and put options.  The data is provided by Yahoo Finance."""

name = "market-data"

ticker = myinput(id=name + "ticker", placeholder="Enter a ticker")
ticker = dbc.Col([dbc.Label('Ticker'), ticker], md=4)

kind = dcc.Dropdown(
    ["call", "put"],
    placeholder="Select call or put",
    id=name + "security",
    style={"backgroundColor": lightblue}
)
kind = dbc.Col([dbc.Label('Call or Put'), kind], md=4)

maturity = dcc.Dropdown(placeholder="Select a maturity", id=name + "maturity", style={"backgroundColor": lightblue})
maturity = dcc.Loading(id=name + "loading1", children=[maturity], type="circle")
maturity = dbc.Col([dbc.Label('Maturity'), maturity], md=4)

row1 = dbc.Row([ticker, kind, maturity])

price = html.Div(id=name + "price", style=text_style)
price = dbc.Col(price, width={'size': 3, 'offset': 5})
row2 = dbc.Row([price])
row2 = dcc.Loading(id=name + "loading3", children=row2, type="circle")

cols = [
    "Strike",
    "Bid",
    "Ask",
    "Last Price",
    "Change",
    "% Change",
    "Time Since Last Trade",
    "Volume",
    "Open Interest",
    "Implied Volatility",
]
tbl = DataTable(
    id=name + "tbl",
    columns=[{"name": c, "id": name + c} for c in cols],
    style_header=style_header,
    style_data=style_data,
    style_as_list_view=True,
    # fixed_rows={'headers': True}, style_table={'height': 400},
    style_data_conditional=style_data_conditional,
)

tbl = dcc.Loading(id=name + "loading2", children=[tbl], type="circle")

body = html.Div([row1, html.Hr(), row2, html.Br(), tbl])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

# this returns the price and fills the dropdown with available maturities
@callback(
    Output(name + "price", "children"),
    Output(name + "maturity", "options"),
    Input(name + "ticker", "value"),
    prevent_initial_call=True,
)
def call1(ticker):
    return price_maturities(ticker)


# this deletes the selected maturity when the ticker is changed
@callback(
    Output(name + "maturity", "value"),
    Input(name + "ticker", "value"),
    prevent_initial_call=True,
)
def call2(ticker):
    return None


# this updates the data table
@callback(
    Output(name + "tbl", "data"),
    Input(name + "ticker", "value"),
    Input(name + "security", "value"),
    Input(name + "maturity", "value"),
    prevent_initial_call=True,
)
def call3(ticker, kind, maturity):
    if maturity:
        df = figtbl(ticker, kind, maturity)
        df.columns = [name + c for c in df.columns]
        return df.to_dict("records")
    else:
        return None
