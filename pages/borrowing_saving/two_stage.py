from dash import callback, Dash, html, dcc
from dash.dependencies import Input, Output, State
from pages.formatting import (
    Layout,
    css_no_header,
    style_header,
    style_data_conditional,
    style_dark,
    style_light,
    style_header_dark,
    Slider,
    style_editable,
    myinput,

)
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from pages.borrowing_saving.two_stage_figtbl import figtbl

title = "Two-stage valuation model"
runtitle = None
chapter = "Borrowing and Saving"
chapter_url = "borrowing-saving"

urls = None

text = """ 
    In the first stage of a two-stage valuation model, cash flow forecasts are made period by period.  In the second
    stage, cash flows are assumed to grow at a constant rate.  If there are $n$ periods in the first stage,
    and $C_i$ denotes the 
    cash flow at date $i$, then the second-stage cash flows are $C_{n+1}$, $C_{n+2} = (1+g)C_{n+1}$, $C_{n+3} = (1+g)C_{n+2}$, etc.,
    where $g$ denotes the growth rate.  The value of the second-stage cash flows discounted to date $n$ is
    $TV = C_{n+1}/(r-g)$, where $r>g$ is the discount rate.  The present value as of date 
    0 of the second-stage cash flows is
    $TV/(1+r)^n$.  This is added to the present value of the first-stage cash
    flows to compute the total value.
    
    On this page, it is assumed that the first cash flow occurs at date 1 (1 period away).  The
    cash flows in the table below are editable.  The "first cash flow of the second stage" is $C_{n+1}$ in the notation above.
    """

name = "two-stage"

Num = myinput(id=name+"num", value=5)
Rate = Slider(
    "Discount rate",
    mn=5,
    mx=20,
    step=.1,
    value=10,
    tick=5,
    kind="pct",
    name=name+'rate'
)

Growth = Slider(
    "Second-stage growth rate",
    mn=0,
    mx=10,
    step=.1,
    value=4,
    tick=2,
    kind="pct",
    name=name+'growth'
)

tbl1 = DataTable(
    id=name + "tbl1",
    columns=[{"name": "Year", "id": name + "date"}],
    data=[{name+'date': i} for i in range(1,6)],
    style_header=style_header_dark,
    style_data=style_dark,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

tbl2 = DataTable(
    id=name + "tbl2",
    columns=[{"name": "Cash Flow", "id": name + "cashflow", "editable": True}],
    data=[{name+'cashflow': 100} for i in range(1,6)],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

tbl3 = DataTable(
    id=name + "tbl3",
    columns=[{
            "name": "col1",
            "id": name + "col1",
    },  {"name": "col2",
             "id": name + "col2",
    }],
    css=css_no_header,
    style_as_list_view=True,
    style_data=style_dark,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

tbl1 = dbc.Col(tbl1, xs=12, sm=6, md=6, lg=6, className="mb-2")
tbl2 = dbc.Col([ html.Div("Enter first-stage cash flows."), tbl2], xs=12, sm=6, md=6, lg=6, className="mb-2")
# tbl3 = dbc.Col(tbl3, md=6)

left = [
    html.Div("Enter number of periods in first stage."),
    Num,
    html.Br(),
    dbc.Row([tbl1, tbl2], align="end", className="gx-1"),
]

middle = [
    Growth,
    html.Br(),
    html.Div("Enter first cash flow of second stage."),
    myinput(id=name+"cf", value=100)
]

right = [
    Rate,
    html.Br(),
    html.Br(),
    tbl3
]

left = dbc.Col(left, xs=12, sm=12, md=4, lg=4, className="mb-2")
middle = dbc.Col(middle, xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col(right, xs=12, sm=12, md=4, lg=4, className="mb-2")


row = dbc.Row([left, middle, right], align="top", className="gx-1")
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
    Input(name + "num", "value"),
    Input(name + "rate", "value"),
    Input(name + "growth", "value"),
    Input(name + "cf", "value"),
    Input(name + "tbl2", "data_timestamp"),
    State(name + "tbl2", "data"),
)
def call(N, r, g, cf, timestamp, rows):
    return figtbl(name, N, r, g, cf, rows)


