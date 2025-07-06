import numpy as np
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly import tools
from pages.formatting import largefig


def p(deltay, n, coupon, yld):
    cashFlows = [coupon] * (n - 1) + [100 + coupon]
    y = yld + deltay
    pvs = cashFlows / (1 + y / 2) ** np.arange(1, n + 1)
    return np.sum(pvs)


def figtbl(maturity, coupon_rate, yld):
    # calculate price
    yld /= 100
    n = int(2 * maturity)
    coupon = coupon_rate / 2
    cashFlows = [coupon] * (n - 1) + [100 + coupon]
    pvs = cashFlows / (1 + yld / 2) ** np.arange(1, n + 1)
    price = np.sum(pvs)

    # calculate duration
    pcts = pvs / np.sum(pvs)
    times = np.array([i / 2 for i in range(1, n + 1)])
    duration = np.sum(pcts * times) / (1 + yld / 2)

    string1 = "% change in price = %{y:.01%}<extra></extra>"
    string2 = "-duration x change in yield = %{y:.01%}<extra></extra>"
    grid = np.arange(-0.05, 0.051, 0.001)
    trace1 = go.Scatter(
        x=grid,
        y=[(p(dy, n, coupon, yld) - price) / price for dy in grid],
        mode="lines",
        hovertemplate=string1,
        name="% change in price",
    )
    trace2 = go.Scatter(
        x=grid,
        y=np.array([-dy * duration for dy in grid]),
        mode="lines",
        hovertemplate=string2,
        name="- modified duration x change in yield",
    )
    fig = go.Figure(trace1)
    fig.add_trace(trace2)
    fig.update_layout(xaxis_title="Change in Yield")
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".1%")
    fig.update_layout(hovermode="x unified")
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

    return largefig(fig, showlegend=True), "{:.3f}".format(duration)
