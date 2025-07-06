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
from pages.fixed_income.duration_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(1)

title = "Duration"
runtitle = None
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = None
text = """
             The Macaulay duration of a bond is defined as a weighted average of the 'times to cash flows' of its coupons
             and face value.  It equals the sum over cash flows of the 'time to cash flow' multiplied by the percent
             of the bond value that the cash flow contributes, calculating values by discounting at the bond yield.  The 
             table below calculates the percent of the total
             value that each cash flow contributes and multiplies by the 'time to cash flow'.  The sum of those numbers
             is the Macaulay duration.  Modified duration
             is defined as Macaulay duration divided by $1 + \\text{yield}/2$.  Modified duration
             is useful for describing the risk of a bond.  This is shown on the "Duration and Risk" page.
             
             Duration of either type is always less than maturity for a coupon-paying bond, 
             because part of the
             value is contributed by the coupons, which are paid earlier than the maturity.  Both types of 
             duration are also lower, other 
             things equal, when coupons are higher, because more of the bond value is paid earlier when coupons are 
             higher.
             Both types of duration are also lower, other things equal, when the yield is higher, because earlier 
             cash flows constitute
             a larger fraction of the total value when cash flows are discounted at a higher rate.  
          """

name = "duration_tbl"

inputs = [name + "input" + str(i) for i in range(3)]
slider1 = Slider(
    "Maturity", mn=0, mx=30, step=0.5, value=10, tick=10, name=inputs[0], kind=None
)
slider2 = Slider(
    "Coupon Rate", mn=0, mx=10, step=0.1, value=5, tick=2, kind="pct", name=inputs[1]
)
slider3 = Slider(
    "Yield", mn=0, mx=10, step=0.1, value=5, tick=2, kind="pct", name=inputs[2]
)

tbl = DataTable(
    id=name + "tbl",
    columns=[
        {"name": "Year", "id": name + "Year"},
        {"name": "Cash Flow", "id": name + "Cash Flow"},
        {
            "name": "PV Factor @ Yield",
            "id": name + "PV Factor @ Yield",
            "type": "numeric",
            "format": percentage,
        },
        {"name": "PV of Cash Flow", "id": name + "PV of Cash Flow"},
        {
            "name": "Percent of Total",
            "id": name + "Percent of Total",
            "type": "numeric",
            "format": percentage,
        },
        {"name": "Year x Percent", "id": name + "Year x Percent"},
    ],
    style_data=style_data,
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_as_list_view=True,
)

macaulay = html.Div(id=name + "macaulay", style=text_style)
label1 = dbc.Label("Macaulay Duration", html_for=name + "macaulay")
macaulay = dbc.Col([label1, macaulay], md=6)

modified = html.Div(id=name + "modified", style=text_style)
label2 = dbc.Label("Modified Duration", html_for=name + "modified")
modified = dbc.Col([label2, modified], md=6)
row = dbc.Row([macaulay, modified], align="center")

left = dbc.Col([slider1, slider2], md=6)
right = dbc.Col([slider3, html.Br(), row])
row = dbc.Row([left, right], align="top")

body = html.Div([row, html.Br(), tbl])

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
    Output(name + "macaulay", "children"),
    Output(name + "modified", "children"),
]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    df, string1, string2 = figtbl(*args)
    df.columns = [name + c for c in df.columns]
    return df.to_dict("records"), string1, string2
