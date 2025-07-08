import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.bonds.creditspreads_figtbl import figtbl
from pages.formatting import Layout

title = "Credit spreads"
runtitle = None
chapter = "Fixed Income"
chapter_url = "fixed-income"
urls = None
text = """This page presents option-adjusted spreads of the ICE BofA U.S. corporate
             bond indices relative to Treasury rates.  The data is provided by 
             [Federal Reserve Economic Data](https://fred.stlouisfed.org/).
          """

name = "creditspreads"

body = dbc.Container([
    dcc.Loading(dcc.Graph(id=name + "fig"), type="circle"),
    dbc.Button(id=name+'invisible btn', style={'display':'none'})
    ], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)


@callback(Output(name + "fig", "figure"), Input(name + "invisible btn", "n_clicks"))
def call(nclicks):
    return figtbl(nclicks)
