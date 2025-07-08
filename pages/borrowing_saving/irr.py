from dash import callback, Dash, html, dcc
from dash.dependencies import Input, Output, State
from pages.formatting import Layout, style_header, myinput, style_editable, style_data_conditional, text_style, style_light
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from pages.borrowing_saving.irr_figtbl import figtbl

title = "Internal rate of return"
runtitle = None
chapter = "Borrowing and Saving"
chapter_url = "borrowing-saving"

urls = None

text = """ 
    The internal rate of return (IRR) is the discount rate at which the net present value (NPV) of the cash
    flows is zero.  If cash flows are negative early and positive late with only one switch-point, and the
    sum of the positive cash flows is larger than the sum of the absolute values of the negative cash flows, then
    there is a unique positive IRR and it is the discount rate at which the NPV switches from positive to
    negative.  For some sequences of cash flows, the IRR is undefined.  

    Enter the number of periods.  If there are $r$ periods, there are $r+1$ dates.  Date 0 is the beginning of the
    first period, date 1 is the end of the first period, ..., and date $r$ is the end of the $r$th period.  The
    cash flows in the table below are editable. """

name = "irr"

Num = myinput(id=name+"num", value=5)

tbl1 = DataTable(
    id=name + "tbl1",
    columns=[{"name": "Date", "id": name + "date"}],
    data=[{name+'date': i+1} for i in range(6)],
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

tbl2 = DataTable(
    id=name + "tbl2",
    columns=[{"name": "Cash Flow", "id": name + "cashflow", "editable": True}],
    data=[{name+'cashflow': -100}] + [{name+'cashflow': 30} for i in range(5)],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
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
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)



tbl1 = dbc.Col(tbl1, xs=12, sm=4, md=2, lg=2, className="mb-2")
tbl2 = dbc.Col(tbl2, xs=12, sm=8, md=4, lg=4, className="mb-2")
tbl3 = dbc.Col(tbl3, xs=12, sm=12, md=6, lg=6, className="mb-2")
tables = dbc.Row([tbl1, tbl2, tbl3], align="top", className="gx-1")

left = dbc.Col(
    [
        html.Div("Enter integer number of periods"),
        Num,
        html.Br(),
        html.Br(),
        tables
    ],
    xs=12, sm=12, md=6, lg=6, className="mb-2"
)

label = html.Div(['Internal rate of return:'])
IRR= html.Div(id=name + "irr", style=text_style)
IRR = dbc.Row([dbc.Col(label, md=6), dbc.Col(IRR, md=6)])

graph = dcc.Graph(name + "fig")

right = dbc.Col([IRR, html.Br(), graph], xs=12, sm=12, md=6, lg=6, className="mb-2")

row = dbc.Row([left, right], align="top", className="gx-1")
body = dbc.Container(row, fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)


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


