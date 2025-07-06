# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 17:50:07 2022

@author: kerry
"""

import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, blue, green


def stockTree(S, u, n):
    return [[S * u ** (t - 2 * i) for i in range(t + 1)] for t in range(n + 1)]


def europeanTree(S, K, r, u, n, kind):
    def f(S):
        if kind == "call":
            return np.maximum(np.array(S) - K, 0)
        else:
            return np.maximum(K - np.array(S), 0)

    d = 1 / u
    p = (1 + r - d) / (u - d)
    disc = 1 / (1 + r)
    ST = [S * u ** (n - 2 * i) for i in range(n + 1)]
    x = f(ST)
    lst = [x]
    while len(x) > 1:
        x = disc * (p * x[:-1] + (1 - p) * x[1:])
        lst.insert(0, x)
    return [list(x) for x in lst], p


def americanTree(S, K, r, u, n, kind):
    def f(S):
        if kind == "call":
            return np.maximum(np.array(S) - K, 0)
        else:
            return np.maximum(K - np.array(S), 0)

    d = 1 / u
    p = (1 + r - d) / (u - d)
    disc = 1 / (1 + r)
    ST = [S * u ** (n - 2 * i) for i in range(n + 1)]
    x = f(ST)
    lst = [x]
    while len(x) > 1:
        x0 = disc * (p * x[:-1] + (1 - p) * x[1:])
        t = len(x0) - 1
        St = [S * u ** (t - 2 * i) for i in range(t + 1)]
        x = np.maximum(x0, f(St))
        lst.insert(0, x)
    return [list(x) for x in lst], p


def treePlot(tree, kind):
    color = green if kind == "option" else blue
    string = "$%{y:,.2f}<extra></extra>"
    spliced = []
    for a, b in zip(tree[1:], tree[:-1]):
        x = []
        for i in range(len(a)):
            x.append(a[i])
            try:
                x.append(b[i])
            except:
                pass
        spliced.append(x)
    fig = go.Figure()
    for i in range(len(tree) - 1):
        x = [1, 0, 1]
        for j in range(i):
            x.append(0)
            x.append(1)
        x = np.array(x) + i
        y = spliced[i]
        trace = go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            hovertemplate=string,
            marker=dict(size=12, color=color),
            line=dict(color=color),
        )
        fig.add_trace(trace)
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=1))
    fig.update_xaxes(title="Time")
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    return fig

def figtbl(kind, S, K, r, u, n):
    r /= 100
    u = 1 + u / 100
    tree = stockTree(S, u, n)
    fig_stock = treePlot(tree, kind="stock")
    fig_stock.update_yaxes(title="Underlying Price")
    x = kind.split(" ")
    Tree = europeanTree if x[0] == "European" else americanTree
    tree, prob = Tree(S, K, r, u, n, x[1])
    value = tree[0][0]
    fig_option = treePlot(tree, kind="option")
    if x[1] == "put":
        fig_option.update_yaxes(autorange="reversed")
    fig_option.update_yaxes(title=kind.title() + " Value")
    string1 = x[0].title() + " " + x[1].title() + " value at date 0:"
    string2 = f"${value:.2f}"
    string3 = f"{prob:.1%}"

    return largefig(fig_stock), largefig(fig_option), string1, string2, string3
