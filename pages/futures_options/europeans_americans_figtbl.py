import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm
from pages.formatting import largefig, blue, red


def call(S, K):
    return np.maximum(S - K, 0)


def put(S, K):
    return np.maximum(K - S, 0)


def callBS(S, K, T, sigma, r, q):
    if T == 0:
        return np.maximum(S - K, 0)

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
    if T == 0:
        return np.maximum(K - S, 0)

    def f(s):
        s = s if s != 0 else 1.0e-6
        d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * s * norm.cdf(-d1)

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def callAmerican(S, K, T, sigma, r, q, N=40):
    if T == 0:
        return np.maximum(S - K, 0)

    def f(s):
        s = s if s != 0 else 1.0e-6
        dt = T / N
        up = np.exp(sigma * np.sqrt(dt))
        down = 1 / up
        prob = (np.exp((r - q) * dt) - down) / (up - down)
        discount = np.exp(-r * dt)
        v = np.zeros(N + 1)
        x = s * up ** N
        v[0] = np.maximum(x - K, 0)
        for i in range(1, N + 1):
            x *= down * down
            v[i] = np.maximum(x - K, 0)
        for n in range(N - 1, -1, -1):
            x = s * up ** n
            v[0] = np.maximum(x - K, discount * (prob * v[0] + (1 - prob) * v[1]))
            for i in range(1, n + 1):
                x *= down * down
                v[i] = np.maximum(
                    x - K, discount * (prob * v[i] + (1 - prob) * v[i + 1])
                )
        return v[0]

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def putAmerican(S, K, T, sigma, r, q, N=40):
    if T == 0:
        return np.maximum(K - S, 0)

    def f(s):
        s = s if s != 0 else 1.0e-6
        dt = T / N
        up = np.exp(sigma * np.sqrt(dt))
        down = 1 / up
        prob = (np.exp((r - q) * dt) - down) / (up - down)
        discount = np.exp(-r * dt)
        v = np.zeros(N + 1)
        x = s * up ** N
        v[0] = np.maximum(K - x, 0)
        for i in range(1, N + 1):
            x *= down * down
            v[i] = np.maximum(K - x, 0)
        for n in range(N - 1, -1, -1):
            x = s * up ** n
            v[0] = np.maximum(K - x, discount * (prob * v[0] + (1 - prob) * v[1]))
            for i in range(1, n + 1):
                x *= down * down
                v[i] = np.maximum(
                    K - x, discount * (prob * v[i] + (1 - prob) * v[i + 1])
                )
        return v[0]

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def figtbl(K, sigma, r, q, T):
    sigma /= 100
    r /= 100
    q /= 100

    S = np.arange(1, 2 * K + 1, 1)

    fig_put = go.Figure()
    trace2 = go.Scatter(
        x=S,
        y=putBS(S, K, T, sigma, r, q),
        mode="lines",
        name="European",
        line=dict(color=blue),
    )
    trace1 = go.Scatter(
        x=S,
        y=putAmerican(S, K, T, sigma, r, q),
        mode="lines",
        name="American",
        line=dict(color=red),
    )
    fig_put.add_trace(trace1)
    fig_put.add_trace(trace2)
    fig_put.add_trace(go.Scatter(x=S, y=put(S, K), mode="lines", name="Intrinsic"))

    fig_call = go.Figure()

    trace2 = go.Scatter(
        x=S,
        y=callBS(S, K, T, sigma, r, q),
        mode="lines",
        name="European",
        line=dict(color=blue),
    )
    trace1 = go.Scatter(
        x=S,
        y=callAmerican(S, K, T, sigma, r, q),
        mode="lines",
        name="American",
        line=dict(color=red),
    )
    fig_call.add_trace(trace1)
    fig_call.add_trace(trace2)
    fig_call.add_trace(go.Scatter(x=S, y=call(S, K), mode="lines", name="Intrinsic"))

    string = "$%{y:,.2f}<extra></extra>"
    for fig in [fig_put, fig_call]:
        fig.update_traces(mode="lines", hovertemplate=string)
        fig.update_layout(hovermode="x unified")
        fig.update_yaxes(title="Option Value")
        fig.update_layout(
            yaxis_tickprefix="$",
            yaxis_tickformat=",.0f",
            xaxis_tickprefix="$",
            xaxis_tickformat=",.0f",
        )
        fig.update_xaxes(title="Price of Underlying Asset")

    # Title
    fig_put.update_layout(
        title={
            "text": "Put",
            "y": 0.96,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )

    fig_call.update_layout(
        title={
            "text": "Call",
            "y": 0.96,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )
    fig_call.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    fig_put.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    return largefig(fig_call, showlegend=True), largefig(fig_put, showlegend=True)
