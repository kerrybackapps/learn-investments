# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 20:20:33 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.futures_options.option_portfolios_figtbl import figtbl
from pages.formatting import Layout, lightblue

title = "Option portfolios"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None

text = """ The value at maturity of a portfolio of options is plotted, assuming all of the options have
              the same maturity.  Enter positive quantities for long positions in options and negative quantities for
              short positions.  Long or short positions in the underlying asset can also be included. Also, long or 
              short cash positions can be included: cash means a position in a risk-free asset sufficient to deliver
              the specified amount of cash at the option maturity, for example, a long or short position in a zero-coupon
              bond that matures at the option maturity."""
name = "option-portfolios"

numoptions = 4
inputs = [name + "input" + str(i) for i in range(3 * numoptions + 4)]

dropc = dcc.Dropdown(["None", "Long", "Short"], value="None", id=inputs[0], style={"backgroundColor": lightblue})
dropx = dcc.Dropdown([i for i in range(5, 105, 5)], placeholder="Amount", id=inputs[1], style={"backgroundColor": lightblue})
dropc = dbc.Col([dbc.Label("Position in cash", html_for=inputs[0]), dropc], xs=12, sm=8, md=8, lg=8, className="mb-2")
dropx = dbc.Col(dropx, xs=12, sm=4, md=4, lg=4, className="mb-2")
row0 = dbc.Row([dropc, dropx], align="end", className="gx-1")

dropu = dcc.Dropdown(["None", "Long", "Short"], value="None", id=inputs[2], style={"backgroundColor": lightblue})
dropq = dcc.Dropdown([i for i in range(1, 4)], placeholder="Quantity", id=inputs[3], style={"backgroundColor": lightblue})
dropu = dbc.Col([dbc.Label("Position in underlying", html_for=inputs[2]), dropu], xs=12, sm=8, md=8, lg=8, className="mb-2")
dropq = dbc.Col(dropq, xs=12, sm=4, md=4, lg=4, className="mb-2")
row1 = dbc.Row([dropu, dropq], align="end", className="gx-1")


inpts = [
    row0,
    html.Br(),
    row1,
    html.Br(),
    dbc.Label("Options", html_for=inputs[4]),
]

for i in range(numoptions):
    inpts.append(html.Br())
    drop1 = dcc.Dropdown(
        ["Call", "Put", "None"], placeholder="Security", id=inputs[3 * i + 4], style={"backgroundColor": lightblue}
    )
    drop2 = dcc.Dropdown(
        [i for i in range(5, 205, 5)], placeholder="Strike", id=inputs[3 * i + 5], style={"backgroundColor": lightblue}
    )
    drop3 = dcc.Dropdown(
        [i for i in range(3, -4, -1) if i != 0],
        placeholder="Quantity",
        id=inputs[3 * i + 6],
        style={"backgroundColor": lightblue}
    )
    drop1 = dbc.Col(drop1, xs=12, sm=6, md=4, lg=4, className="mb-2")
    drop2 = dbc.Col(drop2, xs=12, sm=6, md=4, lg=4, className="mb-2")
    drop3 = dbc.Col(drop3, xs=12, sm=6, md=4, lg=4, className="mb-2")
    row = dbc.Row([drop1, drop2, drop3], className="gx-1")
    inpts.append(row)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col(inpts, xs=12, sm=12, md=6, lg=6, className="mb-2")
right = dbc.Col(graph, xs=12, sm=12, md=6, lg=6, className="mb-2")
body = dbc.Container([dbc.Row([left, right], align="center", className="gx-1")], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + "fig", "figure")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(*args)
