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
from pages.fixed_income.duration_risk_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(1)

title = "Duration and risk"
runtitle = "Duration and Risk"
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = {"Python notebook": None}
text = """
             Modified duration
             determines the risk of a bond in the sense that it determines how much the price will move
             when the yield changes.  The percent change in the price is approximately the negative of the 
             modified duration 
             multiplied by the change in the yield.  Longer duration bonds have more risk in the sense that 
             the absolute value of the return is larger for any given change in the yield.  
          """

name = "duration-risk"

inputs = [name + "input" + str(i) for i in range(3)]
slider1 = Slider(
    "Maturity (years)",
    mn=0,
    mx=30,
    step=0.5,
    value=10,
    tick=10,
    name=inputs[0],
    kind=None,
)
slider2 = Slider(
    "Coupon Rate", mn=0, mx=10, step=0.1, value=5, tick=2, kind="pct", name=inputs[1]
)
slider3 = Slider(
    "Yield", mn=0, mx=10, step=0.1, value=5, tick=2, kind="pct", name=inputs[2]
)

graph = dcc.Graph(id=name + "fig")

duration = html.Div(id=name + "duration", style=text_style)
duration = dbc.Col(duration, md=6)
label = dbc.Label("Modified Duration", html_for=name + "duration")
label = dbc.Col(label, md=6)
row = dbc.Row([label, duration], align="center")

left = dbc.Col([slider1, slider2, slider3, html.Br(), row], md=4)
right = dbc.Col(graph, md=8)
row = dbc.Row([left, right], align="top")
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

outputs = [Output(name + "fig", "figure"), Output(name + "duration", "children")]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)
