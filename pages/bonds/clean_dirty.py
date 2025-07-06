import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate
from pages.formatting import (
    Slider,
    Layout,
    blue,
    style_header,
    style_data,
    style_data_conditional,
)
from pages.bonds.clean_dirty_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(1)

title = "Clean and dirty bond prices and yields"
runtitle = "Premium and Discount"
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = {"Python notebook": None}
text = """
             The buyer of a bond pays the quoted price plus accrued interest.  The quoted price is called the clean
             price, and the price including accrued interest is called the dirty price.  The dirty price can
             can be computed from the yield $y$ by discounting the cash flows at a semi-annual 
             rate of $y/2$.  Subtracting
             accrued interest then produces the clean price.  Conversely, the yield can be computed from the clean
             price by first adding accrued interest to obtain the dirty price and then computing the yield as
             the rate (more precisely, twice the semi-annual rate) that equates the PV of the cash flows to the
             dirty price.  That approach is taken on this page.  Letting $d$ denote the number of days to the
             next coupon, $\\Delta = d/180$, and $y$ the yield, the PV factors 
             in the table are $(1+y/2)^{-\\Delta}$, $(1+y/2)^{-1-\\Delta}$, 
             $(1+y/2)^{-2-\\Delta}$, ...
             
             This page uses the  30/360 day count 
             convention, which means that accrued interest is calculated as
             ($1 -$ days to next coupon/180) times 
             the coupon, and 30-day months are assumed when computing "days to next coupon." Values 
             are presented per $100 face value.  
          """

name = "clean-dirty"

inputs = [name + "input" + str(i) for i in range(4)]
slider1 = Slider(
    "Coupon Rate", mn=0, mx=10, step=0.1, value=5, tick=2, kind="pct", name=inputs[0]
)
slider2 = Slider(
    "Remaining Coupons",
    mn=0,
    mx=60,
    step=1,
    value=10,
    tick=20,
    name=inputs[1],
    kind=None,
)
slider3 = Slider(
    "Days to Next Coupon",
    mn=0,
    mx=180,
    step=1,
    value=60,
    tick=30,
    name=inputs[2],
    kind=None,
)
slider4 = Slider(
    "Clean Price", mn=60, mx=140, step=1, value=110, tick=20, kind=None, name=inputs[3]
)

graph = dcc.Graph(id=name + "fig")

tbl = DataTable(
    id=name + "tbl",
    columns=[
        {"name": "Time", "id": name + "Time"},
        {"name": "Cash Flow", "id": name + "Cash Flow"},
        {
            "name": "PV Factor @ Yield",
            "id": name + "PV Factor @ Yield",
            "type": "numeric",
            "format": percentage,
        },
        {"name": "PV of Cash Flow", "id": name + "PV of Cash Flow"},
    ],
    style_data=style_data,
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_as_list_view=True,
)

yld = html.Div(id=name + "yield", style={"color": blue})
dirty = html.Div(id=name + "dirty", style={"color": blue})

label1 = dbc.Label("Yield", html_for=name + "yield")
label2 = dbc.Label("Dirty Price", html_for=name + "dirty")
row = dbc.Row(
    [
        dbc.Col(label2, md=3),
        dbc.Col(dirty, md=3),
        dbc.Col(label1, md=3),
        dbc.Col(yld, md=3),
    ]
)

left = dbc.Col([slider1, slider2, slider3], md=6)
right = dbc.Col([slider4, html.Br(), row], md=6)
row1 = dbc.Row([left, right], align="center")

left = dbc.Col(graph, md=6)
right = dbc.Col(tbl, md=6)
row2 = dbc.Row([left, right], align="top")

body = html.Div([row1, html.Br(), row2])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [
    Output(name + "tbl", "data"),
    Output(name + "yield", "children"),
    Output(name + "dirty", "children"),
    Output(name + "fig", "figure"),
]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    df, yld, dirty, fig = figtbl(*args)
    df.columns = [name + c for c in df.columns]
    return df.to_dict("records"), yld, dirty, fig
