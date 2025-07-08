# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:40:58 2022

@author: kerry
"""

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.capm.alphas_sharpes_figtbl import figtbl
from pages.formatting import Slider, Layout

# topmatter
title = "Alphas and Sharpe ratios"
runtitle = None
chapter = "Capital Asset Pricing Model"
chapter_url = "capm"
urls = None

text = """ 
    Consider a regression of the excess return of an asset on the excess return of a benchmark:
    $r - r_f = \\alpha +\\beta (r_m-r_f) + \\varepsilon$, where $r=$ asset return, $r_f=$ risk-free return, 
    $r_b=$ benchmark return, and $\\varepsilon$ is a zero-mean risk that is uncorrelated with $r_b$. The alpha is 
    positive if and only if the Sharpe ratio of the asset is higher than the Sharpe ratio of the benchmark multiplied
    by the correlation between the asset return and the benchmark return.  Likewise, the alpha is negative if and only
    if the Sharpe ratio of the asset is lower than the Sharpe ratio of the benchmark multiplied by the correlation.  This
    can be seen from the figure.  
    
    The dashed line has slope equal to the Sharpe ratio of the benchmark multiplied
    by the correlation.  When the Sharpe ratio of the asset is higher than the Sharpe ratio of the benchmark multiplied
    by the correlation, then the asset plots above the dashed line.  That
    occurs when
    the alpha is positive, and in that case adding some of the asset to the benchmark (or increasing its weight)
    can improve the mean-variance efficiency
    of the benchmark.  When the Sharpe ratio of the asset is less than the Sharpe ratio of the benchmark multiplied
    by the correlation, then the asset plots below the dashed line.  In that case, the alpha is negative, 
    and shorting some of the asset 
    (or reducing its weight) can improve the mean-variance efficiency of the benchmark.  The asset 
    plots on the dashed
    line when the alpha is zero, and in that case the benchmark is the tangency portfolio.
    """
name = "alphas_sharpes"

inputs = [name + "input" + str(i) for i in range(6)]

slider1 = Slider(
    "Risk free rate", mn=0, mx=5, step=0.1, value=2, tick=1, name=inputs[0], kind="pct"
)
slider2 = Slider(
    "Expected benchmark return",
    mn=5,
    mx=15,
    step=1,
    value=10,
    tick=5,
    name=inputs[1],
    kind="pct",
)
slider3 = Slider(
    "Standard deviation of benchmark return",
    mn=5,
    mx=20,
    step=1,
    value=15,
    tick=5,
    name=inputs[2],
    kind="pct",
)
slider4 = Slider(
    "Standard deviation of asset return",
    mn=5,
    mx=40,
    step=1,
    value=30,
    tick=5,
    name=inputs[3],
    kind="pct",
)
slider5 = Slider(
    "Correlation of asset with benchmark",
    mn=-90,
    mx=90,
    step=5,
    value=60,
    tick=30,
    name=inputs[4],
    kind="pct",
)
slider6 = Slider(
    "Asset alpha", mn=-10, mx=10, step=0.5, value=5, tick=5, name=inputs[5], kind="pct"
)

graph = dcc.Graph(id=name + "fig")

left = dbc.Col([slider1, slider2, slider3, slider4, slider5, slider6], xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col(graph, xs=12, sm=12, md=8, lg=8, className="mb-2")
body = dbc.Container(dbc.Row([left, right], align="center", className="gx-1"), fluid=True, className="px-1")

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
