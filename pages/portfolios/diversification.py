from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.diversification_figtbl import figtbl
from pages.formatting import Slider, Layout, ricegrey

title = "Diversification"
runtitle = "Diversification"
chapter = "Portfolios"
chapter_url = chapter.lower()

urls = {"Python notebook": None}

text = """ The risk of a portfolio is shown, assuming each asset has the same standard deviation and
           the assets all have the same correlation with each other.  The 
           portfolio variance decreases as the number of assets increases, eventually approaching the
           variance of an individual asset multiplied by their common correlation.  The decrease in risk 
           as the number of assets increases illustrates the benefit of diversification. Diversification is
           more beneficial when the correlation of the assets is lower."""

name = "diversification"

graph = dcc.Graph(id=name + "fig")

slider1 = Slider(
    "Standard deviation of assets",
    mn=0,
    mx=50,
    step=1,
    value=40,
    tick=10,
    kind="pct",
    name=name + "std",
)
slider2 = Slider(
    "Correlation between assets",
    mn=0,
    mx=100,
    step=1,
    value=25,
    tick=25,
    kind="pct",
    name=name + "cor",
)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col(slider1, xs=12, sm=12, md=6, lg=6, xl=6)
right = dbc.Col(slider2, xs=12, sm=12, md=6, lg=6, xl=6)
row = dbc.Row([left, right], align="center", gutter=3)

body = dbc.Container(html.Div([row, html.Hr(), graph]))


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
    Output(name + "fig", "figure"),
    Input(name + "std", "value"),
    Input(name + "cor", "value"),
]


@callback(*lst)
def call(*args):
    return figtbl(*args)
