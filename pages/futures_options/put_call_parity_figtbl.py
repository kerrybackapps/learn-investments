import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import largefig


def call(S, K):
    return np.maximum(np.array(S) - K, 0)


def put(S, K):
    return np.maximum(K - np.array(S), 0)


def callBS(S, K, T, sigma, r, q):
    def f(s):
        s = s if s != 0 else 1.0e-6
        d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return np.exp(-q * T) * s * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def putBS(S, K, T, sigma, r, q):
    def f(s):
        s = s if s != 0 else 1.0e-6
        d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * s * norm.cdf(-d1)

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def figtbl(K, sigma, r, q, T):
    sigma /= 100
    r /= 100
    q /= 100

    fig = go.Figure()

    S = [val for val in np.arange(0.1, 100.1, 0.1)]

    call_put_diff = callBS(S, K, T, sigma, r, q) - putBS(S, K, T, sigma, r, q)

    fig.add_trace(
        go.Scatter(
            x=S,
            y=call_put_diff,
            mode="lines",
            hovertemplate="underlying = %{x:.2f}<br>call minus put = %{y:.2f}<extra></extra>"
        )
    )


    fig.update_yaxes(title="Call Minus Put")
    fig.update_layout(yaxis_tickformat=",.1f", xaxis_tickformat=",.1f")
    fig.update_xaxes(title="Underlying Price")

    return largefig(fig)
