import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, dash_table
from pages.bonds.real_termstructure_figtbl import figtbl
from pages.formatting import Layout

title = "Term structure of real interest rates"
runtitle = "Term Structure of TIPS"
chapter = "Fixed Income"
chapter_url = "fixed-income"
urls = {"Python notebook": None}
text = """
            Yields on TIPS are shown at various maturities.  Because TIPS have inflation-protected cash flows, these
            are real interest rates.  The data is provided by 
            [Federal Reserve Economic Data](https://fred.stlouisfed.org/).
          """
name = "real-termstructure"
graph = dcc.Loading(
    id=name + "loading", children=[dcc.Graph(id=name+"fig")], type="circle"
)
body = html.Div([
    graph,
    dbc.Button(id=name+'invisible btn', style={'display':'none'})]
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

@callback(Output(name+"fig", "figure"), Input(name + "invisible btn", "n_clicks"))
def call(nclicks):
    return figtbl(nclicks)