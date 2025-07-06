from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from pages.formatting import (
    Layout,
    text_style,
    myinput,
    lightblue
)
from pages.futures_options.market_implied_vols_figtbl import price_maturities, figtbl

title = "Market implied volatilities"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None

text = """Implied volatilities calculated from market option prices are plotted against strike prices.  The data comes
          from Yahoo Finance.  The implied volatilities are based on the most recent transaction prices, using
          only transactions within the most recent 24 hour window.
       """

name = "market-implied-vols"

ticker = myinput(id=name + "ticker",  placeholder="Enter a ticker")
ticker = dbc.Col([dbc.Label('Ticker'), ticker], width={"size": 4, "offset": 1})


maturity = dcc.Dropdown(placeholder="Select a maturity", id=name + "maturity", style={"backgroundColor": lightblue})
maturity = dcc.Loading(id=name + "loading1", children=[maturity], type="circle")
maturity = dbc.Col([dbc.Label('Maturity'), maturity], width={"size": 4, "offset": 2})

row1 = dbc.Row([ticker, maturity])

price = html.Div(id=name + "price", style=text_style)
price = dbc.Col(price, width={"size": 3, "offset": 5})
row2 = dbc.Row([price])
row2 = dcc.Loading(id=name + "loading3", children=row2, type="circle")

fig = dcc.Graph(id=name + 'fig')

fig = dcc.Loading(id=name + "loading2", children=[fig], type="circle")

body = html.Div([row1, html.Hr(), row2, fig])

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


# this updates the figure
@callback(
    Output(name + "fig", "figure"),
    Input(name + "ticker", "value"),
    Input(name + "maturity", "value"),
    prevent_initial_call=True,
)
def call3(ticker, maturity):
    return figtbl(ticker, maturity) if maturity else go.Figure()
