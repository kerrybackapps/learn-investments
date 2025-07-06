import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable, FormatTemplate
from pages.formatting import (
    Slider,
    Layout,
    text_style,
    style_header,
    style_data,
    style_data_conditional,
)
from pages.bonds.prices_yields_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(1)

runtitle = None
title = "Bond prices and yields"
chapter = "Fixed Income"
chapter_url = "fixed-income"
urls = None
text = """ The yield of a bond that pays semi-annual coupons is defined to be 
              twice the semi-annual discount rate at 
              which the current
              price equals the present value of
              the future coupons and face value.  This page shows the relationship between 
              prices and yields for a bond the first coupon of which
              is six months away.  Cash flows are stated per 100 dollars face value.   The PV factors in the table are
              $(1+y/2)^{-1}$, $(1+y/2)^{-2}$, ..., where $y$ denotes the yield.  The price equals the sum of the
              PVs of the cash flows.  When the yield is below the coupon rate, the price is above
              face value (the bond is trading 'at a premium'), and when the yield is above the coupon rate, 
              the price is below face value (the bond is trading 'at a discount').
              """
name = "prices-yields"

inputs = [name + "input" + str(i) for i in range(5)]
slider1 = Slider(
    "Years to maturity",
    mn=0,
    mx=30,
    step=0.5,
    value=5,
    tick=5,
    name=inputs[0],
    kind=None,
)
slider2 = Slider(
    "Coupon Rate", mn=0, mx=10, step=0.1, value=5, tick=2, kind="pct", name=inputs[1]
)

radio = dcc.RadioItems(
    options={"yld": "Solve for Yield", "price": "Solve for Price"},
    value = "yld", id=inputs[2], labelStyle={"display": "block"}
)

slider3 = Slider(
    "Price (use when solving for yield)", mn=50, mx=150, step=1, value=90, tick=25, kind="dol", name=inputs[3]
)

slider4 = Slider(
    "Yield (use when solving for price)", mn=0, mx=15, step=0.1, value=6, tick=3, kind="pct", name=inputs[4]
)

graph = dcc.Graph(id=name + "fig")

tbl = DataTable(
    id=name + "tbl",
    columns=[
        {"name": "Period", "id": name + "Period"},
        {"name": "Cash Flow", "id": name + "Cash Flow"},
        {
            "name": "PV Factor @ Yield",
            "id": name + "PV Factor @ Yield",
            "type": "numeric",
            "format": percentage,
        },
        {"name": "PV of Cash Flow", "id": name + "PV of Cash Flow"},
    ],
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_as_list_view=True,
)

yld = html.Div(id=name+"yld", style=text_style)
price = html.Div(id=name+"price", style=text_style)

left = dbc.Col([slider1, slider2], md=6)
right = dbc.Col([slider3, slider4], md=6)
sliders = dbc.Row([left, right])
sliders = dbc.Col(sliders, md=8)

radio = dbc.Col(radio, md=6)
output1 = dbc.Row([dbc.Col(html.Div('Yield:'), md=6), dbc.Col(yld, md=6)])
output2 = dbc.Row([dbc.Col(html.Div('Price:'), md=6), dbc.Col(price, md=6)])
outputs = dbc.Col([output1, output2], md=6)
other = dbc.Row([radio, outputs], align='center')
other = dbc.Col(other, md=4)

row1 = dbc.Row([sliders, other], align='center')

left = dbc.Col(graph, md=6)
right = dbc.Col(tbl, md=6)
row2 = dbc.Row([left, right], align="top")

body = html.Div([row1, html.Hr(), row2])

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
    Output(name + "fig", "figure"),
    Output(name + "yld", "children"),
    Output(name + "price", "children"),
   ]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs

@callback(*lst)
def call(*args):
    df, fig, str1, str2 = figtbl(*args)
    df.columns = [name + c for c in df.columns]
    return df.to_dict("records"), fig, str1, str2
