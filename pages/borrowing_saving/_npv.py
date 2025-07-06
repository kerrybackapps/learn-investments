from dash import callback, Dash, html, dcc
from dash.dependencies import Input, Output, State
from pages.formatting import Layout, style_header, style_editable, style_data_conditional, text_style, myinput
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from pages.borrowing_saving.npv_figtbl import figtbl

name = "_npv"

Num = myinput(id=name+"num", value=5)
Rate = myinput(id=name + "rate", value=10)
NPV = html.Div(id=name + "npv", style=text_style)

tbl1 = DataTable(
    id=name + "tbl1",
    columns=[{"name": "Date", "id": name + "date"}],
    data=[{name+'date': i+1} for i in range(6)],
    style_header=style_header,
    style_data_conditional=style_data_conditional,
)

tbl2 = DataTable(
    id=name + "tbl2",
    columns=[{"name": "Cash Flow", "id": name + "cashflow", "editable": True}],
    data=[{name+'cashflow': -100}] + [{name+'cashflow': 30} for i in range(5)],
    style_header=style_header,
    style_data=style_editable,
)

tbl3 = DataTable(
    id=name + "tbl3",
    columns=[{
            "name": "PV Factor",
            "id": name + "pv-factor",
    },  {"name": "PV of Cash Flow",
             "id": name + "pv",
    }],
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)

tbl1 = dbc.Col(tbl1, xs=1)
tbl2 = dbc.Col(tbl2, xs=2)
tbl3 = dbc.Col(tbl3, xs=4)
left = [dbc.Label("Enter integer number of periods <= 10"),
    Num,
    html.Br(),
    dbc.Label("Enter discount rate in %"),
    Rate]
left = dbc.Col(left, xs=3)
right = [dbc.Label("Net present value", html_for=name + "npv"), NPV]
right = dbc.Col(right, xs=2)

row = dbc.Row([left, tbl1, tbl2, tbl3, right], align="top")
layout = dbc.Container([html.Br(), html.Br(), row], fluid=True)

@callback(
    Output(name + "tbl1", "data"),
    Output(name + "tbl2", "data"),
    Output(name + "tbl3", "data"),
    Output(name + "npv", "children"),
    Input(name + "num", "value"),
    Input(name + "rate", "value"),
    Input(name + "tbl2", "data_timestamp"),
    State(name + "tbl2", "data"),
)
def call(N, r, timestamp, rows):
    return figtbl(name, N, r, rows)


