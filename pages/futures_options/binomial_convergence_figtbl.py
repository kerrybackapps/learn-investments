import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import largefig, red


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


def callEuropean(S, K, T, sigma, r, q, N=100):
    def f(s):
        s = s if s != 0 else 1.0e-6  # to allow 0 in the stock price grid when we use it
        dt = T / N
        up = np.exp(sigma * np.sqrt(dt))
        down = 1 / up
        prob = (np.exp((r - q) * dt) - down) / (up - down)
        discount = np.exp(-r * dt)
        v = np.zeros(N + 1)
        x = s * up ** N
        v[0] = np.maximum(x - K, 0)

        # v will become the last column of the df
        for i in range(1, N + 1):
            x *= down * down
            v[i] = np.maximum(x - K, 0)

        # x now is the lowest price

        # for the previous N columns
        for n in range(N - 1, -1, -1):
            x = s * up ** n  # x now is the highest price of the n-th column
            v[0] = discount * (prob * v[0] + (1 - prob) * v[1])
            for i in range(1, n + 1):
                x *= down * down
                v[i] = discount * (prob * v[i] + (1 - prob) * v[i + 1])
            # v now is the previous column
        return v[0]

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def putEuropean(S, K, T, sigma, r, q, N=100):
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
            v[0] = discount * (prob * v[0] + (1 - prob) * v[1])
            for i in range(1, n + 1):
                x *= down * down
                v[i] = discount * (prob * v[i] + (1 - prob) * v[i + 1])
        return v[0]

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def figtbl(K, sigma, r, q, T, S, maxN=50):
    # maxN in the maximum interation.
    #   maximum depth of binomial tree is 2 * maxN since we only simulate even numbers of depths.
    sigma /= 100
    r /= 100
    q /= 100

    a = np.linspace(1, maxN, maxN) * 2
    b = np.zeros(maxN)

    for i in range(maxN):
        b[i] = callEuropean(S, K, T, sigma, r, q, int(a[i]))
    fig_call = go.Figure()
    fig_call.add_trace(go.Scatter(x=a, y=b, mode="markers",
                       marker=dict(size=10),
                       name="Binomial Value",
                       hovertemplate="Binomial value = $%{y:0.2f}<extra></extra>")
                       )
    fig_call.add_trace(
        go.Scatter(
            x = np.linspace(0, 2*maxN, 100),
            y= [callBS(S, K, T, sigma, r, q)] * 100,
            name = "Black-Scholes",
            hovertemplate="Black-Scholes value = $%{y:0.2f}<extra></extra>"
        )
    )
    # annotation_text="Black-Scholes value",
    # annotation_position="top right")


    b = np.zeros(maxN)
    for i in range(maxN):
        b[i] = putEuropean(S, K, T, sigma, r, q, int(a[i]))
    fig_put = go.Figure()
    fig_put.add_trace(go.Scatter(x=a, y=b, mode="markers",
                                  marker=dict(size=10),
                                  name="Binomial Value",
                                  hovertemplate="Binomial value = $%{y:0.2f}<extra></extra>")
                       )
    fig_put.add_trace(
        go.Scatter(
            x=np.linspace(0, 2 * maxN, 100),
            y=[putBS(S, K, T, sigma, r, q)] * 100,
            name="Black-Scholes",
            hovertemplate="Black-Scholes value = $%{y:0.2f}<extra></extra>"
        )
    )
    # annotation_text="Black-Scholes value",
    # annotation_position="top right")

    for fig in [fig_call, fig_put]:
        fig.update_yaxes(title="Option Value")
        fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.2f",
                          legend=dict(x=0.90, xanchor="right", y=0.99, yanchor="top"))
        fig.update_xaxes(title="Number of Time Steps in Binomial Model")

    fig_call.update_layout(
        title={
            "text": "European Call",
            "y": 0.96,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )

    fig_put.update_layout(
        title={
            "text": "European Put",
            "y": 0.96,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )

    return largefig(fig_call, showlegend=True), largefig(fig_put, showlegend=True)
