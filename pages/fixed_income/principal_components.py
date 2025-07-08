import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate
from pages.formatting import (
    Layout,
    style_header,
    style_data_conditional,
)
from pages.fixed_income.principal_components_figtbl import figtbl
from datetime import date

percentage = FormatTemplate.percentage(1)

title = 'Principal components'
runtitle = None
chapter = 'Fixed Income'
chapter_url = 'fixed-income'

urls=None
text = """
    Historical monthly U.S. Treasury yield changes at six maturities (1, 2, 3, 5, 10, and 30 years) are 
    described in terms of 
    six uncorrelated monthly shocks by the method of principal components.  The table on the left below shows the 
    amount of the variation in yields that
    each of the shocks explains, beginning with the most important, then including the next most important,
    etc.  The second table shows how the yields at each of the maturities changes in
    response to a unit shock, for each of the six shocks, with the yield changes expressed in basis points.
    The labeling is 1 for the shock that explains the most variance, 2 for the shock that explains the second 
    most variance, etc.  The figure on the right plots the first three columns of the second table, showing
    how yields change in response to the three most important shocks.
    """

name = "principal-components"

today = date.today().year
slider = dcc.RangeSlider(
    id=name + "slider",
    min=1978,
    max=today,
    step=1,
    value=[1978, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = dbc.Col(
    [dbc.Label("Select date range", html_for=name + "slider"), slider],
    xs=12, sm=8, md=6, lg=6, className="mb-2 offset-md-3",
)
slider = dbc.Row(slider, className="gx-1")

graph = dcc.Graph(id=name + "fig")

values = DataTable(
    id=name + "values",
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_as_list_view=True,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
    columns=[dict(name="", id=name+"col1"),
             dict(name="% of Variance", id=name+"col2", type="numeric", format=percentage)
            ]
)

vectors = DataTable(
    id=name + "vectors",
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_cell_conditional=[
        {
            'if': {'column_id': name+"maturity"},
            'textAlign': 'left'
        }
    ],
    style_as_list_view=True,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
    columns=[dict(name="Maturity/Shock", id=name+"maturity")] + [
             dict(name=str(i), id=name+str(i)) for i in range(1, 7)
            ]
)

values = dbc.Col(values, xs=12, sm=12, md=2, lg=2, className="mb-2")
vectors = dbc.Col(vectors, xs=12, sm=12, md=5, lg=5, className="mb-2")
graph = dbc.Col(graph, xs=12, sm=12, md=5, lg=5, className="mb-2")
row2 = dbc.Row([values, vectors, graph], align="top", className="gx-1")

body = dbc.Container([slider, html.Br(), html.Hr(), row2], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name + "fig", "figure"), Output(name + "v", "data")]
inputs = [Input(name + "slider", "value")]
lst = outputs + inputs


@callback(
    Output(name+"values", "data"),
    Output(name+"vectors", "data"),
    Output(name+"fig", "figure"),
    Input(name+"slider", "value")
)
def call(dates):
    return figtbl(name, dates)
