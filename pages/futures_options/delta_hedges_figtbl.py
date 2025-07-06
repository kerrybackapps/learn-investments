import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.io as pio

plotly_template = pio.templates["plotly_dark"]
colors = plotly_template.layout.colorway
from pages.formatting import largefig


def call(S, K):
    return np.maximum(S - K, 0)


def put(S, K):
    return np.maximum(K - S, 0)


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


def callData(P, K, T, sigma, r, q):
    # the black scholes value as the function of the underlying price
    S = [val for val in np.arange(0, 100.1, 0.1)]

    bs_values = [callBS(s, K, T, sigma, r, q) for s in S]

    def leverage_portfolio(S, delta):
        return (delta * S) - ((delta * P) - callBS(P, K, T, sigma, r, q))

    # delta for call
    d1 = (np.log(P / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta_1 = np.exp(-q*T) * norm.cdf(d1)

    leverage_values = [leverage_portfolio(s, delta_1) for s in S]

    tang_leverage_value = leverage_portfolio(P, delta_1)

    return S, bs_values, leverage_values, delta_1, tang_leverage_value


def putData(P, K, T, sigma, r, q):
    # the black scholes value as the function of the underlying price
    S = [val for val in np.arange(0, 100.1, 0.1)]
    bs_values = [putBS(s, K, T, sigma, r, q) for s in S]

    def leverage_portfolio(S, delta):
        return (delta * S) - ((delta * P) - putBS(P, K, T, sigma, r, q))

    # delta for call
    d1 = (np.log(P / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta_1 = - np.exp(-q*T) * norm.cdf(-d1)

    leverage_values = [leverage_portfolio(s, delta_1) for s in S]

    tang_leverage_value = leverage_portfolio(P, delta_1)

    return S, bs_values, leverage_values, delta_1, tang_leverage_value


def figtbl(K, sigma, r, q, T, P):
    sigma /= 100
    r /= 100
    q /= 100

    fig_call = go.Figure()
    fig_put = go.Figure()



    for fig in [fig_call, fig_put]:
        name = "Call Value" if fig == fig_call else "Put Value"
        Data = callData if fig == fig_call else putData
        S, bs_values, leverage_values, delta, tang_leverage_value = Data(
            P, K, T, sigma, r, q
        )

        if fig == fig_call:
            delta_call = delta
        else:
            delta_put = delta
        fig.add_trace(go.Scatter(x=S, y=bs_values, mode="lines", name=name))
        fig.add_trace(
            go.Scatter(x=S, y=leverage_values, mode="lines", name="Delta Hedge")
        )

        fig.update_layout(hovermode="x unified")

        fig.update_yaxes(title=None)
        fig.update_layout(yaxis_tickformat=",.2f", xaxis_tickformat=",.2f")
        fig.update_xaxes(title="Underlying Price")

    # figure titles
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

    fig_call.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    fig_put.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

    # the dynamic text labels before displaying deltas
    label_call = "European call delta at $" + "{:.0f}".format(P) + " : "
    label_put = "European put delta at $" + "{:.0f}".format(P) + " : "

    cash_call = callBS(P, K, T, sigma, r, q) - delta_call*P
    cash_put = putBS(P, K, T, sigma, r, q) - delta_put*P

    return (
        largefig(fig_call, showlegend=True),
        largefig(fig_put, showlegend=True),
        "{:.3f}".format(delta_call),
        "{:.3f}".format(delta_put),
        label_call,
        label_put,
        f'{cash_call:.2f}',
        f'{cash_put:.2f}'
    )
