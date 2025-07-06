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

    fig_call = go.Figure()
    fig_put = go.Figure()

    S = [val for val in np.arange(0.1, 100.1, 0.1)]

    for fig in [fig_call, fig_put]:
        if fig == fig_call:
            bs_values = callBS(S, K, T, sigma, r, q)
            intrinsic = call(S, K)
        else:
            bs_values = putBS(S, K, T, sigma, r, q)
            intrinsic = put(S, K)

        fig.add_trace(go.Scatter(x=S, y=bs_values, mode="lines", name="BS Value"))
        fig.add_trace(
            go.Scatter(
                x=S,
                y=intrinsic,
                mode="lines",
                line=dict(dash="dot"),
                name="Intrinsic Value",
            )
        )

        fig.update_layout(hovermode="x unified")
        fig.update_yaxes(title="Option Value")
        fig.update_layout(yaxis_tickformat=",.2f", xaxis_tickformat=",.2f")
        fig.update_xaxes(title="Underlying Price")

    # figure titles
    fig_call.update_layout(
        title={
            "text": "European Call",
            "y": 0.94,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )

    fig_put.update_layout(
        title={
            "text": "European Put",
            "y": 0.94,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )
    fig_call.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig_put.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

    return largefig(fig_call, showlegend=True), largefig(fig_put, showlegend=True)
