import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import minimize
import plotly.graph_objects as go
from pages.formatting import largefig, red, blue

N = 30

def BS(S, K, T, sigma, r, q, kind):
    S = np.maximum(S, 1.0e-6)
    d1 = np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T
    d1 /= sigma * np.sqrt(T)
    d2 = d1 - sigma * np.sqrt(T)
    if kind == "call":
        return (
                np.exp(-q * T) * S * norm.cdf(d1) -
                np.exp(-r * T) * K * norm.cdf(d2)
        )
    else:
        return (
                np.exp(-r * T) * K * norm.cdf(-d2) -
                np.exp(-q * T) * S * norm.cdf(-d1)
        )


def American(S, K, T, sigma, r, q, kind):
    intrinsic = lambda x: (x - K if kind == "call" else K - x)
    dt = T / N
    up = np.exp(sigma * np.sqrt(dt))
    down = 1 / up
    prob = (np.exp((r - q) * dt) - down) / (up - down)
    discount = np.exp(-r * dt)

    # Black-Scholes at penultimate date
    x = S * up ** np.arange(N - 1, -N - 1, -2)
    v = np.maximum(intrinsic(x), BS(x, K, dt, sigma, r, q, kind))

    # step backward in the tree until date 1
    for n in range(N - 2, 0, -1):
        x = S * up ** n
        v[0] = np.maximum(
            intrinsic(x),
            discount * (prob * v[0] + (1 - prob) * v[1])
        )
        for i in range(1, n + 1):
            x *= down * down
            v[i] = np.maximum(
                intrinsic(x),
                discount * (prob * v[i] + (1 - prob) * v[i + 1])
            )
    # calculate value at date 0 if not exercised (will compare to intrinsic value later)
    return discount * (prob * v[0] + (1 - prob) * v[1])



from scipy.optimize import minimize





def figtbl(K, sigma, r, q, T):
    times = T * np.array([0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.98, 1])
    def Boundary(kind):
        times = T * np.array([0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.98, 1])
        intrinsic = lambda x: (max(x - K, 0) if kind == "call" else max(K - x, 0))
        bdys = []

        for t in times[:-1]:
            constraints = [{
                "type": "ineq",
                "fun": lambda x: American(x, K, T - t, sigma, r, q, kind) - intrinsic(x) - 0.01
            }]
            objective = lambda x: x if kind == "put" else -x

            b = minimize(objective, x0=K, method="SLSQP", constraints=constraints).x[0]
            bdys.append(b)

        bdys.append(K)
        return bdys

    fig_call = go.Figure()
    fig_put = go.Figure()
    for fig in [fig_put, fig_call]:
        fig.add_trace(
            go.Scatter(
                x=[0, T], y=[K, K], mode="lines", line=dict(dash="dot", color=red)
            )
        )
        fig.update_traces(hovertemplate="$%{y:,.2f}<extra></extra>")
        fig.update_yaxes(title="Underlying Price")
        fig.update_layout(
            yaxis_tickprefix="$", yaxis_tickformat=",.0f", xaxis_tickformat=",.1f"
        )
        fig.update_xaxes(title="Time (years)")

    # Title
    fig_put.update_layout(
        title={
            "text": "American Put",
            "y": 0.96,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )

    fig_call.update_layout(
        title={
            "text": "American Call",
            "y": 0.96,
            "x": 0.2,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )

    sigma /= 100
    r /= 100
    q /= 100

    string = "boundary = $%{y:,.2f} at t = %{x:0.2f}<extra></extra>"
    if q > 0:
        b_call = Boundary("call")
        callmax = np.max(b_call)
        fig_call.add_trace(
            go.Scatter(
                x=times, y=[callmax] * len(times), mode="lines", line=dict(color=blue)
            )
        )
        fig_call.add_trace(
            go.Scatter(
                x=times,
                y=b_call,
                mode="lines",
                name="American call boundary",
                hovertemplate=string,
                line=dict(color=blue),
                fill="tonexty",
            )
        )
    range1 = 1.4 * K if q == 0 else max(1.05 * callmax, 1.4 * K)

    b_put = Boundary("put")
    fig_put.add_trace(
        go.Scatter(
            x=times,
            y=b_put,
            mode="lines",
            hovertemplate=string,
            name="American put boundary",
            line=dict(color=blue),
            fill="tozeroy",
        )
    )

    for fig in [fig_call, fig_put]:
        fig.update_yaxes(range=[0, range1])

    return largefig(fig_call), largefig(fig_put)
