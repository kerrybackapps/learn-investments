# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 09:23:46 2022

@author: kerry
"""

from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.portfolios.riskfree_figtbl import figtbl
from pages.formatting import Slider, Layout

title = "Risk-free asset"
runtitle = None
chapter = "Portfolios"
chapter_url = "portfolios"
name = "riskfree"
urls = None

text = """ 
    Expected returns and risks are shown for combinations of a risky asset or portfolio
    with risk-free saving and borrowing.  Because both risk premium and risk scale with the risky asset allocation,
    the set of (std dev, mean) pairs forms a line, namely the locus of points with a constant risk premium to risk (Sharpe)
    ratio.  The portfolios with less than 100% in the risky asset plot on a
    line segment from the saving rate to the risky asset (std dev, mean).  The portfolios with more than 100% in the
    risky asset plot on a line extending beyond the risky asset (std dev, mean) with slope equal to the Sharpe ratio defined by
    the borrowing rate.  The dotted lines indicate infeasible (std dev, mean) combinations, because they involve
    saving at the borrowing rate or borrowing at the saving rate.
    """



inputs = [name + "input" + str(i) for i in range(4)]
slider1 = Slider(
    "Expected return of risky asset",
    mn=0,
    mx=20,
    step=1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Standard deviation of risky asset",
    mn=0,
    mx=50,
    step=1,
    value=30,
    tick=10,
    kind="pct",
    name=inputs[1],
)
slider3 = Slider(
    "Savings rate", mn=0, mx=10, step=1, value=2, tick=2, kind="pct", name=inputs[2]
)
slider4= Slider(
    "Excess of borrowing over savings rate",
    mn=0,
    mx=5,
    step=1,
    value=3,
    tick=1,
    kind="pct",
    name=inputs[3],
)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider2, slider3, slider4], md=4)
right = dbc.Col(graph, md=8)
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
lst = [Output(name + "fig", "figure")] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(*args)
