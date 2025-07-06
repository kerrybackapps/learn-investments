import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

plotly_template = pio.templates["plotly_dark"]
colors = plotly_template.layout.colorway
from scipy.stats import norm
from scipy.optimize import fsolve
from scipy.stats import multivariate_normal as mnorm
from pages.formatting import largefig, red, blue


def callBS(s, K, T, sigma, r, q):
    if s <= 0:
        return 0
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return np.exp(-q * T) * s * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)


def callDelta(s, K, T, sigma, r, q):
    if s <= 0:
        return 0
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * norm.cdf(d1)


def Dmin(K, deltaT, r):
    return (1 - np.exp(-r * deltaT)) * K


def criticalS(D, K, deltaT, sigma, r):
    def f(s):
        return s - K - callBS(s - D, K, deltaT, sigma, r, 0)

    def fprime(s):
        return 1 - callDelta(s - D, K, deltaT, sigma, r, 0)

    return fsolve(f, x0=1.5 * K, fprime=fprime).item()


def binorm(a, b, corr):
    cov = [[1, corr], [corr, 1]]
    return mnorm.cdf(x=[a, b], mean=[0, 0], cov=cov)


def AmericanCall(D, S, K, t, deltaT, sigma, r):
    # t = time until dividend
    # deltaT = time between dividend and maturity
    Z0 = S - np.exp(-r * t) * D
    if D <= Dmin(K, deltaT, r):
        return callBS(Z0, K, t + deltaT, sigma, r, 0)
    Sstar = criticalS(D, K, deltaT, sigma, r)
    Zstar = Sstar - D
    d1 = (np.log(Z0 / Zstar) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    d1prime = (np.log(Z0 / K) + (r + 0.5 * sigma ** 2) * (t + deltaT)) / (
        sigma * np.sqrt(t + deltaT)
    )
    d2prime = d1prime - sigma * np.sqrt(t + deltaT)
    N1 = norm.cdf(d1)
    N2 = norm.cdf(d2)
    corr = -np.sqrt(t / (t + deltaT))
    M1 = binorm(-d1, d1prime, corr)
    M2 = binorm(-d2, d2prime, corr)
    return (
        Z0 * (N1 + M1)
        + np.exp(-r * t) * (D - K) * N2
        - np.exp(-r * (t + deltaT)) * K * M2
    )


def callData(S, K, t, deltaT, sigma, r, div_lbd=0, div_ubd=10):
    lbd = round(Dmin(K, deltaT, r) + 0.1, 1)

    grid = np.arange(lbd, div_ubd + 0.1, 0.1)
    grid_1 = grid
    Sstar = [criticalS(D, K, deltaT, sigma, r) for D in grid]

    grid = np.arange(div_lbd, div_ubd, 0.1)
    grid_2 = grid
    European = [
        callBS(S - np.exp(-r * t) * D, K, t + deltaT, sigma, r, 0) for D in grid
    ]
    American = [AmericanCall(D, S, K, t, deltaT, sigma, r) for D in grid]

    return grid_1, Sstar, grid_2, European, American


def figtbl(K, sigma, r, t, deltaT, S):
    sigma /= 100
    r /= 100

    grid_1, Sstar, grid_2, European, American = callData(
        S, K, t, deltaT, sigma, r, div_lbd=0, div_ubd=10
    )

    # Critical price of underlying
    fig_ctc = go.Figure()
    string = "Exercise boundary = $%{y:0.2f} when dividend = $%{x:0.2f}<extra></extra>"
    fig_ctc.add_trace(go.Scatter(x=grid_1, y=Sstar, mode="lines", hovertemplate=string))
    fig_ctc.update_yaxes(title="Critical Price of Underlying")
    fig_ctc.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        xaxis_tickprefix="$",
        xaxis_tickformat=",.2f",
    )
    fig_ctc.update_xaxes(title="Dividend")

    # Option value
    fig_opt = go.Figure()

    string = "American = $%{y:,.2f}<extra></extra>"
    fig_opt.add_trace(
        go.Scatter(
            x=grid_2,
            y=American,
            mode="lines",
            name="American Call",
            hovertemplate=string,
            line=dict(color=red),
        )
    )
    string = "European = $%{y:,.2f}<extra></extra>"
    fig_opt.add_trace(
        go.Scatter(
            x=grid_2,
            y=European,
            mode="lines",
            name="European Call",
            hovertemplate=string,
            line=dict(color=blue),
        )
    )
    fig_opt.update_yaxes(title="Option Value")
    fig_opt.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        xaxis_tickprefix="$",
        xaxis_tickformat=",.2f",
    )
    fig_opt.update_xaxes(title="Dividend")
    fig_opt.update_layout(hovermode="x unified")
    fig_opt.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

    return largefig(fig_ctc), largefig(fig_opt, showlegend=True)
