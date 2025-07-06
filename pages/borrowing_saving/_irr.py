from dash import callback, Dash, html, dcc
from dash.dependencies import Input, Output, State
from pages.formatting import Layout, style_header, myinput, style_editable, style_data_conditional, text_style, style_light
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from pages.borrowing_saving.irr_figtbl import figtbl

name = "_irr"

Num = myinput(id=name+"num", value=5)

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
            "name": "PV Factor @ IRR",
            "id": name + "pv-factor",
    },  {"name": "PV of Cash Flow",
             "id": name + "pv",
    }],
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)



tbl1 = dbc.Col(tbl1, xs=2)
tbl2 = dbc.Col(tbl2, xs=4)
tbl3 = dbc.Col(tbl3, xs=6)
row2 = dbc.Row([tbl1, tbl2, tbl3], align="top")

left = dbc.Col(
    [
        html.Div("Enter integer number of periods <= 10"),
        Num,
    ],
    xs=5
)

label = html.Div(['Internal rate of return:'])
label = dbc.Col(label, xs={"size": 3, "offset": 1})
IRR= html.Div(id=name + "irr", style=text_style)
IRR = dbc.Col(IRR, xs=3)
row1 = dbc.Row([left, label, IRR], align="center")


graph = dcc.Graph(name + "fig")

layout = dbc.Container([html.Br(), html.Br(), row1, html.Br(), row2, graph], fluid=True)

@callback(
    Output(name + "tbl1", "data"),
    Output(name + "tbl2", "data"),
    Output(name + "tbl3", "data"),
    Output(name + "irr", "children"),
    Output(name + 'fig', 'figure'),
    Input(name + "num", "value"),
    Input(name + "tbl2", "data_timestamp"),
    State(name + "tbl2", "data"),
)
def call(N,timestamp, rows):
    return figtbl(name, N, rows)


