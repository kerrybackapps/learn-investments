import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.io as pio

plotly_template = pio.templates["plotly_dark"]
colors = plotly_template.layout.colorway
from pages.formatting import largefig


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


def callGreeks(S, K, T, sigma, r, q):
    def f(s):
        s = s if s != 0 else 1.0e-6
        d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        # delta
        delta = np.exp(-q * T) * norm.cdf(d1)
        # gamma
        gamma = np.exp(-q * T) * (1 / (s * sigma * np.sqrt(T))) * norm.pdf(d1)
        # theta
        theta = -np.exp(-q * T) * (s * sigma / (2 * np.sqrt(T))) * norm.pdf(d1)
        theta += q * np.exp(-q * T) * s * norm.cdf(d1)
        theta += -r * np.exp(-r * T) * K * norm.cdf(d2)
        # vega
        vega = np.exp(-q * T) * s * norm.pdf(d1) * np.sqrt(T)
        # rho
        rho = T * np.exp(-r * T) * K * norm.cdf(d2)
        return delta, gamma, theta, vega, rho

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def putGreeks(S, K, T, sigma, r, q):
    def f(s):
        s = s if s != 0 else 1.0e-6
        d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        # delta
        delta = np.exp(-q * T) * norm.cdf(d1)
        delta += -np.exp(-q * T)
        # gamma
        gamma = np.exp(-q * T) * (1 / (s * sigma * np.sqrt(T))) * norm.pdf(d1)
        # theta
        theta = -np.exp(-q * T) * (s * sigma / (2 * np.sqrt(T))) * norm.pdf(d1)
        theta += q * np.exp(-q * T) * s * norm.cdf(d1)
        theta += -r * np.exp(-r * T) * K * norm.cdf(d2)
        theta += r * np.exp(-r * T) * K - q * np.exp(-q * T) * s
        # vega
        vega = np.exp(-q * T) * s * norm.pdf(d1) * np.sqrt(T)
        # rho
        rho = T * np.exp(-r * T) * K * norm.cdf(d2)
        rho += -T * np.exp(-r * T) * K
        return delta, gamma, theta, vega, rho

    if isinstance(S, list) or isinstance(S, np.ndarray):
        return np.array([f(s) for s in S])
    else:
        return f(S)


def figtbl(K, sigma, r, q, T):
    sigma /= 100
    r /= 100
    q /= 100
    S = np.linspace(1, 100, 100)

    callgreeks = callGreeks(S, K, T, sigma, r, q)
    putgreeks = putGreeks(S, K, T, sigma, r, q)

    fig_delta = go.Figure()
    fig_gamma = go.Figure()
    fig_theta = go.Figure()
    fig_vega = go.Figure()
    fig_rho = go.Figure()

    for i, fig, fig_name in zip(
        range(5),
        [fig_delta, fig_gamma, fig_theta, fig_vega, fig_rho],
        ["Delta", "Gamma", "Theta", "Vega", "Rho"],
    ):
        fig.add_trace(
            go.Scatter(x=S, y=callgreeks[:, i], mode="lines", name="European Call")
        )
        fig.add_trace(
            go.Scatter(x=S, y=putgreeks[:, i], mode="lines", name="European Put")
        )
        fig.update_layout(hovermode="x unified")

        # fig.update_yaxes(title=fig_name)
        fig.update_layout(yaxis_tickformat=",.2f", xaxis_tickformat=",.0f")
        fig.update_xaxes(title="Underlying Price")

        # title
        fig.update_layout(
            title={
                "text": fig_name,
                "y": 0.96,
                "x": 0.2,
                "xanchor": "center",
                "yanchor": "bottom",
            }
        )

        # legend
        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return (
        largefig(fig_delta, showlegend=True),
        largefig(fig_gamma, showlegend=True),
        largefig(fig_theta, showlegend=True),
        largefig(fig_vega, showlegend=True),
        largefig(fig_rho, showlegend=True),
    )
