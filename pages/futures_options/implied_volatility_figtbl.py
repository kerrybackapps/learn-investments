import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import fsolve
import plotly.graph_objects as go
from pages.formatting import largefig, red, blue, green


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


def callImpliedVolatility(S, K, T, r, q, v):
    def callFunc(sigma, *args):
        S, K, T, r, q, v = args

        def f(s):
            s = s if s != 0 else 1.0e-6
            d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            return (
                np.exp(-q * T) * s * norm.cdf(d1)
                - np.exp(-r * T) * K * norm.cdf(d2)
                - v
            )

        if isinstance(S, list) or isinstance(S, np.ndarray):
            return np.array([f(s) for s in S])
        else:
            return f(S)

    inpt = (S, K, T, r, q, v)
    sol = fsolve(callFunc, 0.2, args=inpt, full_output=True)
    return sol


def putImpliedVolatility(S, K, T, r, q, v):
    def putFunc(sigma, *args):
        S, K, T, r, q, v = args

        def f(s):
            s = s if s != 0 else 1.0e-6
            d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            return (
                np.exp(-r * T) * K * norm.cdf(-d2)
                - np.exp(-q * T) * s * norm.cdf(-d1)
                - v
            )

        if isinstance(S, list) or isinstance(S, np.ndarray):
            return np.array([f(s) for s in S])
        else:
            return f(S)

    inpt = (S, K, T, r, q, v)
    sol = fsolve(putFunc, 0.2, args=inpt, full_output=True)
    return sol


def figtbl(K, vc, r, q, T, s, vp):
    r /= 100
    q /= 100

    maxprem = 2 * max(vc,vp)

    v_c_l, sigma_c_l = [], []
    sigma = 0.02
    prem = 0
    while prem < maxprem:
        prem = callBS(s, K, T, sigma, r, q)
        v_c_l.append(prem)
        sigma_c_l.append(sigma)
        sigma += 0.02

    v_p_l, sigma_p_l = [], []
    sigma = 0.02
    prem = 0
    while prem < maxprem:
        prem = putBS(s, K, T, sigma, r, q)
        v_p_l.append(prem)
        sigma_p_l.append(sigma)
        sigma += 0.02

    fig = go.Figure()

    # Call
    # figure

    sigma_c = float(callImpliedVolatility(s, K, T, r, q, vc)[0])
    # table
    indx = [
        "d1",
        "N(d1)",
        "d2",
        "N(d2)",
        "exp(-qT)S",
        "exp(-rT)K",
        "exp(-qT)SN(d1)",
        "exp(-rT)KN(d2)",
        "call value",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma_c ** 2) * T) / (sigma_c * np.sqrt(T))
    tbl.loc["d1"] = d1
    tbl.loc["N(d1)"] = norm.cdf(d1)
    d2 = d1 - sigma_c * np.sqrt(T)
    tbl.loc["d2"] = d2
    tbl.loc["N(d2)"] = norm.cdf(d2)
    tbl.loc["exp(-qT)S"] = np.exp(-q * T) * s
    tbl.loc["exp(-rT)K"] = np.exp(-r * T) * K
    tbl.loc["exp(-qT)SN(d1)"] = np.exp(-q * T) * s * norm.cdf(d1)
    tbl.loc["exp(-rT)KN(d2)"] = np.exp(-r * T) * K * norm.cdf(d2)
    tbl.loc["call value"] = np.exp(-q * T) * s * norm.cdf(d1) - np.exp(
        -r * T
    ) * K * norm.cdf(d2)
    tbl_c = tbl

    # Put
    # figure

    sigma_p = float(putImpliedVolatility(s, K, T, r, q, vp)[0])
    # table
    indx = [
        "d1",
        "N(-d1)",
        "d2",
        "N(-d2)",
        "exp(-qT)S",
        "exp(-rT)K",
        "exp(-rT)KN(-d2)",
        "exp(-qT)SN(-d1)",
        "put value",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma_p ** 2) * T) / (sigma_p * np.sqrt(T))
    tbl.loc["d1"] = d1
    tbl.loc["N(-d1)"] = norm.cdf(-d1)
    d2 = d1 - sigma_p * np.sqrt(T)
    tbl.loc["d2"] = d2
    tbl.loc["N(-d2)"] = norm.cdf(-d2)
    tbl.loc["exp(-qT)S"] = np.exp(-q * T) * s
    tbl.loc["exp(-rT)K"] = np.exp(-r * T) * K
    tbl.loc["exp(-qT)SN(-d1)"] = np.exp(-q * T) * s * norm.cdf(-d1)
    tbl.loc["exp(-rT)KN(-d2)"] = np.exp(-r * T) * K * norm.cdf(-d2)
    tbl.loc["put value"] = np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(
        -q * T
    ) * s * norm.cdf(-d1)
    tbl_p = tbl

    trace1 = go.Scatter(
        x=sigma_c_l,
        y=v_c_l,
        mode="lines",
        name="Call",
        hovertemplate="call value = $%{y:.2f} when volatility = %{x:.0%}",
        line=dict(color=blue),
    )
    trace2 = go.Scatter(
        x=sigma_p_l,
        y=v_p_l,
        mode="lines",
        name="Put",
        hovertemplate="put value = $%{y:.2f} when volatility = %{x:.0%}",
        line=dict(color=green)
    )
    trace3 = go.Scatter(
        x=sigma_c_l,
        y=[vc] * len(sigma_c_l),
        mode="lines",
        line=dict(dash="dot", color=blue),
        hovertemplate="call premium = $%{y:.2f}<extra></extra>",
        showlegend=False,
    )
    trace4 = go.Scatter(
        x=sigma_p_l,
        y=[vp] * len(sigma_p_l),
        mode="lines",
        line=dict(dash="dot", color=green),
        name="Put Premium",
        hovertemplate="put premium = $%{y:.2f}<extra></extra>",
        showlegend=False,
    )
    trace5 = go.Scatter(
        x=[sigma_c],
        y=[vc],
        mode="markers",
        hovertemplate="call implied volatility = %{x:0.1%}<extra></extra>",
        marker=dict(size=15, color=blue),
        showlegend=False,
    )
    trace6 = go.Scatter(
        x=[sigma_p],
        y=[vp],
        mode="markers",
        hovertemplate="put implied volatility = %{x:0.1%}<extra></extra>",
        marker=dict(size=15, color=green),
        showlegend=False,
    )

    for trace in [trace1, trace2, trace3, trace4, trace5, trace6]:
        fig.add_trace(trace)

    fig.update_yaxes(
        title="Option Premium", tickformat=",.1f", range=[0, np.maximum(vc, vp) * 2]
    )
    fig.update_xaxes(
        title="Volatility",
        tickformat=",.1f",
        range=[0, np.maximum(sigma_c, sigma_p) * 2],
    )

    # legend
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    tbl_c = tbl_c.round(2)
    tbl_p = tbl_p.round(2)

    return (
        tbl_c.reset_index().to_dict("records"),
        tbl_p.reset_index().to_dict("records"),
        largefig(fig, showlegend=True),
        f"{sigma_c:0.1%}",
        f"{sigma_p:0.1%}",
    )
