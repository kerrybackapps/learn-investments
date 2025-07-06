import numpy as np
from scipy.stats import norm
from pages.formatting import largefig, red, blue
import plotly.graph_objects as go


def callBS(S, K, T, sigma, r, q):
    def f(s):
        s = s if s != 0 else 1.0e-6
        d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return np.exp(-q * T) * s * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)

    return (
        np.array([f(s) for s in S])
        if (isinstance(S, list) or isinstance(S, np.ndarray))
        else f(S)
    )


def callDelta(s, K, T, sigma, r, q):
    s = s if s != 0 else 1.0e-6
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q * T) * norm.cdf(d1)


def putBS(S, K, T, sigma, r, q):
    def f(s):
        s = s if s != 0 else 1.0e-6
        d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * s * norm.cdf(-d1)

    return (
        np.array([f(s) for s in S])
        if (isinstance(S, list) or isinstance(S, np.ndarray))
        else f(S)
    )


def putDelta(s, K, T, sigma, r, q):
    s = s if s != 0 else 1.0e-6
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return -np.exp(-q * T) * norm.cdf(-d1)


class Option(list):
    def add(self, security, quantity, strike=None, time=None):
        self.append(
            dict(security=security, quantity=quantity, strike=strike, time=time)
        )

    def strikes(self):
        return [d["strike"] for d in self if d["security"] != "Underlying"]

    def grid(self, S):
        strikes = self.strikes()
        maxgrid = 2 * S if len(strikes) == 0 else np.max((2 * S, 1.5 * np.max(strikes)))
        return np.arange(0.5, maxgrid+0.5, 0.5)

    def calculate(self, S, sigma, r, q):
        grid = self.grid(S)
        value = 0
        value_line = np.zeros(len(grid))
        delta = 0
        for x in self:
            if x["security"] == "Underlying":
                value += x["quantity"] * S
                value_line += x["quantity"] * grid
                delta += x["quantity"]
            elif x["security"] == "Call":
                K = x["strike"]
                T = x["time"]
                value += x["quantity"] * callBS(S, K, T, sigma, r, q)
                value_line += x["quantity"] * callBS(grid, K, T, sigma, r, q)
                delta += x["quantity"] * callDelta(S, K, T, sigma, r, q)
            else:
                K = x["strike"]
                T = x["time"]
                value += x["quantity"] * putBS(S, K, T, sigma, r, q)
                value_line += x["quantity"] * putBS(grid, K, T, sigma, r, q)
                delta += x["quantity"] * putDelta(S, K, T, sigma, r, q)
        delta_line = delta * grid + value - delta * S
        return value, value_line, delta, delta_line


def figtbl(S, sigma, r, q, *args):
    sigma /= 100
    r /= 100
    q /= 100
    x = Option()
    underlying = args[0]
    if underlying == "Long":
        x.add(security="Underlying", quantity=int(args[1]))
    elif underlying == "Short":
        x.add(security="Underlying", quantity=-int(args[1]))
    for i, arg in enumerate(args):
        if arg == "Call":
            x.add(
                security="Call",
                strike=args[i + 1],
                time=args[i + 2],
                quantity=int(args[i + 3]),
            )
        elif arg == "Put":
            x.add(
                security="Put",
                strike=args[i + 1],
                time=args[i + 2],
                quantity=int(args[i + 3]),
            )
    grid = x.grid(S)
    value, value_line, delta, delta_line = x.calculate(S, sigma, r, q)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=grid, y=delta_line, mode="lines", name="Delta Hedge", line=dict(color=red)
        )
    )
    fig.add_trace(
        go.Scatter(
            x=grid, y=value_line, mode="lines", name="Portfolio", line=dict(color=blue)
        )
    )

    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(title=None)
    fig.update_layout(yaxis_tickformat=",.2f", xaxis_tickformat=",.2f")
    fig.update_xaxes(title="Underlying Price")

    string1 = f"Portfolio delta at ${S:.0f}:"
    string2 = f"{delta:.3f}"

    cash = value - delta*S
    return largefig(fig), string1, string2, f'{cash:.2f}'
