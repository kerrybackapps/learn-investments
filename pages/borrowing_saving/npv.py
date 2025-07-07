from dash import callback, Dash, html, dcc
from dash.dependencies import Input, Output, State
from pages.formatting import Layout, style_header, style_editable, style_data_conditional, text_style, myinput
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from pages.borrowing_saving.npv_figtbl import figtbl

title = "Net present value"
runtitle = None
chapter = "Borrowing and Saving"
chapter_url = "borrowing-saving"

urls = None

text = """ 
    The net present value (NPV) of a sequence of cash flows is the sum of the present values (PV's)
    of the individual cash flows.  The present value of a cash flow is the cash flow multiplied
    by the PV factor (or 'discount factor').  The PV factor is the fractional investment required today
    to accumulate to 100% at the given date, for an investment that earns the discount rate.   PV factors 
    are calculated as $$1/(1+r)^n$$ where $r$ is the discount rate and $n$ is the number
    of periods away.   
    
    Enter the number of periods.  If there are $r$ periods, there are $r+1$ dates.  Date 0 is the beginning of the
    first period, date 1 is the end of the first period, ..., and date $r$ is the end of the $r$th period.  The
    cash flows in the table below are editable. """

name = "net-present-value"

Num = myinput(id=name+"num", value=5)
Rate = myinput(id=name + "rate", value=10)
NPV = html.Div(id=name + "npv", style=text_style)

tbl1 = DataTable(
    id=name + "tbl1",
    columns=[{"name": "Date", "id": name + "date"}],
    data=[{name+'date': i+1} for i in range(6)],
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'minWidth': '100%'},
)

tbl2 = DataTable(
    id=name + "tbl2",
    columns=[{"name": "Cash Flow", "id": name + "cashflow", "editable": True}],
    data=[{name+'cashflow': -100}] + [{name+'cashflow': 30} for i in range(5)],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'minWidth': '100%'},
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
    style_table={'overflowX': 'auto', 'minWidth': '100%'},
)

tbl1 = dbc.Col(tbl1, xs=12, sm=6, md=1, className="mb-2")
tbl2 = dbc.Col(tbl2, xs=12, sm=12, md=2, className="mb-2")
tbl3 = dbc.Col(tbl3, xs=12, sm=12, md=4, className="mb-2")
left = [dbc.Label("Enter integer number of periods"),
    Num,
    html.Br(),
    html.Br(),
    dbc.Label("Enter discount rate in %"),
    Rate]
left = dbc.Col(left, xs=12, sm=6, md=3, className="mb-2")
right = [dbc.Label("NPV", html_for=name + "npv"), NPV]
right = dbc.Col(right, xs=8, sm=4, md=2, className="mb-2")

row = dbc.Row([left, tbl1, tbl2, tbl3, right], align="top", className="g-2")
body = html.Div(row)

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
    Output(name + "npv", "children"),
    Input(name + "num", "value"),
    Input(name + "rate", "value"),
    Input(name + "tbl2", "data_timestamp"),
    State(name + "tbl2", "data"),
)
def call(N, r, timestamp, rows):
    return figtbl(name, N, r, rows)


