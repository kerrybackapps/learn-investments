import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate
from pages.formatting import (
    Slider,
    Layout,
)
from pages.bonds.clean_dirty_paths_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(1)

title = "Hypothetical clean and dirty price paths"
runtitle = "Clean and Dirty Prices"
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = {"Python notebook": None}
text = """
             The figure shows what the clean and dirty bond price paths would be if the bond yield
             remained constant over time. The clean price would be "pulled to par" smoothly.
          """

name = "clean_dirty-paths"

inputs = [name + "input" + str(i) for i in range(4)]
slider1 = Slider(
    "Coupon Rate", mn=0, mx=10, step=0.1, value=4, tick=2, kind="pct", name=inputs[0]
)
slider2 = Slider(
    "Remaining Coupons",
    mn=0,
    mx=60,
    step=1,
    value=20,
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
    "Yield", mn=0, mx=10, step=0.1, value=6, tick=2, kind="pct", name=inputs[3]
)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider2, slider3, slider4], md=4)
right = dbc.Col(graph, md=8)
body = dbc.Row([left, right], align="top")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name + "fig", "figure")]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)
