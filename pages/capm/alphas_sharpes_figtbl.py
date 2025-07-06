# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:41:30 2022

@author: kerry
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, orange, blue, green, red, yellow


def data(rf, mmn, msd, ssd, corr, alpha):
    rf = rf / 100
    mmn = mmn / 100
    msd = msd / 100
    ssd = ssd / 100
    corr = corr / 100
    alpha = alpha / 100
    mprem = mmn - rf
    mvar = msd ** 2
    beta = corr * ssd / msd
    sprem = alpha + beta * mprem
    svar = ssd ** 2
    c = msd * ssd * corr
    names = ["market", "stock"]
    rprem = pd.Series([mprem, sprem], index=names)
    cov = pd.DataFrame([[mvar, c], [c, svar]], index=names, columns=names)
    tang = np.linalg.solve(cov, rprem)
    tang = pd.Series(tang / np.sum(tang), index=names)
    stock = tang["stock"]
    tang_mn = rf + stock * sprem + (1 - stock) * mprem
    tang_sd = np.sqrt(
        stock ** 2 * svar + (1 - stock) ** 2 * mvar + 2 * stock * (1 - stock) * c
    )
    sharpe = (tang_mn - rf) / tang_sd
    if (tang > 0).sum() == 2:
        wts = np.linspace(0, 1, 201)
    elif tang["market"] < 0:
        wts = np.array(
            list(np.linspace(0, 1, 101))
            + list(np.linspace(1.01, max(2, 1 - 2 * tang["market"]), 100))
        )
    else:
        wts = np.array(
            list(np.linspace(min(-1, 2 * tang["stock"]), 0, 101))
            + list(np.linspace(0.01, 1, 100))
        )
    df = pd.DataFrame(
        dtype=float,
        index=range(201),
        columns=["stock", "market", "mean", "std", "msize"],
    )
    df["stock"] = 100 * wts
    df["market"] = 100 * (1 - wts)
    df["mean"] = [rf + w * sprem + (1 - w) * mprem for w in wts]
    df["std"] = np.sqrt(
        [w ** 2 * svar + (1 - w) ** 2 * mvar + 2 * w * (1 - w) * c for w in wts]
    )
    df.loc[200] = [stock, 1 - stock, tang_mn, tang_sd, 15]
    df = df.sort_values(by="mean")

    df2 = pd.DataFrame(dtype=float, index=range(101), columns=["mean", "std"])
    grid = np.linspace(0, 1.1 * df["std"].max(), 101)
    df2["std"] = grid
    df2["mean"] = rf + sharpe * grid
    df2["market"] = 100 * (df2["std"] / tang_sd) * tang["market"]
    df2["stock"] = 100 * (df2["std"] / tang_sd) * stock

    df3 = pd.DataFrame(
        dtype=float,
        index=["stock", "tangency", "market"],
        columns=["mean", "std", "stock", "market"],
    )
    df3.loc["stock"] = [rf + alpha + beta * mprem, ssd, 100, 0]
    df3.loc["market"] = [rf + mprem, msd, 0, 100]
    df3.loc["tangency"] = [tang_mn, tang_sd, tang["stock"], tang["market"]]

    df4 = pd.DataFrame(dtype=float, index=range(101), columns=["mean", "std"])
    df4["std"] = grid
    df4["mean"] = rf + (corr * mprem / msd) * grid

    return df, df2, df3, df4


def figtbl(rf, mmn, msd, ssd, corr, alpha):
    df, df2, df3, df4 = data(rf, mmn, msd, ssd, corr, alpha)
    trace1 = go.Scatter(
        x=df["std"],
        y=df["mean"],
        mode="lines",
        line=dict(color=green),
        text=df["market"],
        customdata=df["stock"],
        hovertemplate="benchmark: %{text:.1f}%<br>asset: %{customdata:.1f}%<extra></extra>",
        showlegend=False
    )
    trace2 = go.Scatter(
        x=df2["std"],
        y=df2["mean"],
        mode="lines",
        line=dict(color=blue),
        text=df2["market"],
        customdata=df2["stock"],
        hovertemplate="benchmark: %{text:.1f}%<br>asset: %{customdata:.1f}%<extra></extra>",
        showlegend=False
    )
    trace3a = go.Scatter(
        x=[df3["std"].loc["stock"]],
        y=[df3["mean"].loc["stock"]],
        mode="markers",
        hovertemplate="asset<extra></extra>",
        marker=dict(size=15, color=red),
        name="Asset"
    )
    trace3b = go.Scatter(
        x=[df3["std"].loc["market"]],
        y=[df3["mean"].loc["market"]],
        mode="markers",
        hovertemplate="benchmark<extra></extra>",
        marker=dict(size=15, color=yellow),
        name="Benchmark"
    )
    trace3c = go.Scatter(
        x=[df3["std"].loc["tangency"]],
        y=[df3["mean"].loc["tangency"]],
        mode="markers",
        text=[df3["stock"].loc["tangency"]],
        customdata=[df3["market"].loc["tangency"]],
        hovertemplate="Tangency<br>benchmark=%{customdata:.1%}<br>asset=%{text:.1%}<extra></extra>",
        marker=dict(size=15, color=green),
        name="Tangency"
    )
    trace4 = go.Scatter(
        x=df4["std"],
        y=df4["mean"],
        mode="lines",
        line_color=orange,
        hovertemplate="slope = correlation x benchmark Sharpe ratio<extra></extra>",
        line_dash="dash",
        showlegend=False
    )  # ,text=['sope='+str(round(corr*(mmn-rf)/msd,2))]*df4.shape[0]),\
    # hovertemplate=text)
    fig = go.Figure()
    for trace in [trace2, trace1, trace3a, trace3b, trace3c, trace4]:
        fig.add_trace(trace)
    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    xmax = 1.25 * np.max([df["std"].max(), df2["std"].max()])
    ymax = 1.25 * np.max([df["mean"].max(), df2["mean"].max()])
    ymin = np.min([0, 1.25 * df["mean"].min()])
    fig.update_xaxes(range=[0, xmax])
    fig.update_yaxes(range=[ymin, ymax])
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return largefig(fig, showlegend=True)
