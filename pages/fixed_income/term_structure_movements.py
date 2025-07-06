import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate
from pages.formatting import (
    Layout,
    style_header,
    style_data_conditional,
)
from pages.fixed_income.term_structure_movements_figtbl import figtbl
from datetime import date

title = "Term structure movements"
runtitle = None
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = None
text = """
    Yields of U.S. Treasuries are obtained from [Federal Reserve Economic Data](https://fred.stlouisfed.org/), 
    and monthly changes in yields are computed.  The tables provide statistics about the monthly changes over
    the date range specified.  The means and standard deviations are in basis points (a basis point is 
    one one-hundredth of a percent).  The mean changes reflect whether yields were rising or falling on average
    over the date range specified.  The standard deviations show that yields are more volatile at shorter
    maturities.  The correlations are generally high but are lower when the maturities are further apart.
    """
name = "term_structure_movements"

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
    width={"size": 6, "offset": 3},
)
slider = dbc.Row(slider)

lbl1 = dbc.Label("Means and Standard Deviations")
tbl1 = DataTable(
    id=name + "tbl1",
    columns=[
        {"name": "", "id": name + "statistic"},
        {"name": "1-Year", "id": name + "1-Year"},
        {"name": "2-Year", "id": name + "2-Year"},
        {"name": "3-Year", "id": name + "3-Year"},
        {"name": "5-Year", "id": name + "5-Year"},
        {"name": "10-Year", "id": name + "10-Year"},
        {"name": "30-Year", "id": name + "30-Year"},
    ],
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_as_list_view=True,
)

columns = ["", "1-Year", "2-Year", "3-Year", "5-Year", "10-Year", "30-Year"]
columns = [dict(name=c, id=name + 'corr' + c, type="numeric") for c in columns]

lbl2 = dbc.Label("Correlation Matrix")
tbl2 = DataTable(
    id=name + "tbl2",
    columns=columns,
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_as_list_view=True,
)


body = dbc.Row(
    dbc.Col(
        [lbl1, tbl1, html.Br(), lbl2, tbl2],
        width={'size': 10, 'offset': 1}
    )
)

body = html.Div([slider, html.Br(), html.Hr(), body])
layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name + "tbl1", "data"), Output(name + "tbl2", "data")]
inputs = [Input(name + "slider", "value")]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    tbl1, tbl2 = figtbl(*args)
    tbl1.columns = [name + c for c in tbl1.columns]
    tbl2.columns = [name + 'corr' + c for c in tbl2.columns]
    return tbl1.to_dict("Records"), tbl2.to_dict("Records")
