# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:40:58 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.borrowing_saving.retirement_solution_figtbl import figtbl
from pages.formatting import Slider, Layout, text_style, lightblue

title = "Retirement planning solution"
runtitle = "Retirement Planning"
chapter = "Borrowing and Saving"
chapter_url = "borrowing-saving"
urls = None

text = """    
    A retirement plan is analyzed as described on the "Retirement Planning" page.              
    Select one of the inputs using the dropdown menu.  The input will be
    calculated to make the retirement plan exactly feasible, with the other inputs determined by the 
    sliders.  The figure shows the projected account balance by year, based on the calculated input. 
    """

name = "retirement-solution"

inputs = [name + "input" + str(i) for i in range(7)]
slider1 = Slider(
    "Initial balance",
    mn=0,
    mx=1000000,
    step=1000,
    value=100000,
    tick=200000,
    name=inputs[0],
    kind="kdol",
)
slider2 = Slider("Years saving", mn=0, mx=50, step=1, value=30, tick=10, name=inputs[1])
slider3 = Slider(
    "Years withdrawing", mn=0, mx=50, step=1, value=30, tick=10, name=inputs[2]
)
slider4 = Slider(
    "Initial monthly savings",
    mn=0,
    mx=10000,
    step=100,
    value=1000,
    tick=2000,
    name=inputs[3],
    kind="kdol",
)
slider5 = Slider(
    "Annual savings growth rate",
    mn=0,
    mx=10,
    step=0.1,
    value=2,
    tick=2,
    name=inputs[4],
    kind="pct",
)
slider6 = Slider(
    "Monthly withdrawal",
    mn=0,
    mx=50000,
    step=100,
    value=10000,
    tick=10000,
    name=inputs[5],
    kind="kdol",
)
slider7 = Slider(
    "Annual rate of return",
    mn=0,
    mx=15,
    step=0.1,
    value=6,
    tick=3,
    name=inputs[6],
    kind="pct",
)

items = ['Initial balance', 'Initial monthly savings', 'Annual savings growth rate', 'Monthly withdrawal',
         'Annual rate of return']

drop = dcc.Dropdown(items, placeholder="Input", id=name + "drop", value='Initial balance', style={"backgroundColor": lightblue})
drop = html.Div([dbc.Label("Select an input to solve for:", html_for=name + "drop"), drop])

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider2, slider3, slider4, slider5, slider6, slider7], md=4)
col1 = dbc.Col(drop, md=4)
col2 = dbc.Col(html.Div(id=name+'string1'), width={"size": 5, "offset": 1})
col3 = dbc.Col(html.Div(id=name+'string2', style=text_style), md=2)
row = dbc.Row([col1, col2, col3], align='center')

right = dbc.Col([row, html.Br(), graph], md=8)
body = dbc.Row([left, right], align="center")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name + "fig", "figure")] + [Output(name+s, "children") for s in ["string1", "string2"]]
inputs = [Input(i, "value") for i in inputs] + [Input(name + "drop", "value")]
lst = outputs + inputs

@callback(*lst)
def call(*args):
    return figtbl(*args)
