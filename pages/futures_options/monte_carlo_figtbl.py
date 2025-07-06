import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import smallfig, blue, red

def figtbl(n_clicks, S, K, sigma, r, q, T):

    sigma /= 100
    r /= 100
    q /= 100
    N = 20000

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    N1 = norm.cdf(d1)
    d2 = d1 - sigma * np.sqrt(T)
    N2 = norm.cdf(d2)
    call_bs = np.exp(-q*T)*S*N1 - np.exp(-r*T)*K*N2
    put_bs = np.exp(-r*T)*K*(1-N2) - np.exp(-q*T)*S*(1-N1)

    eps = norm.rvs(0, 1, N)
    ST = S * np.exp((r - q - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * eps)

    calls = [s for s in ST if s>K]
    puts = [s for s in ST if s<K]
    trace1 = go.Histogram(x=calls, name="call in the money", marker=dict(color=blue))
    trace2 = go.Histogram(x=puts, name="put in the money", marker=dict(color=red))
    fig = go.Figure()
    fig.add_trace(trace2)
    fig.add_trace(trace1)
    fig.update_xaxes(title = "Underlying Price at Maturity")
    fig_call = go.Figure(go.Histogram(x=np.array(calls)-K, marker=dict(color=blue)))
    fig_put = go.Figure(go.Histogram(x=K-np.array(puts), marker=dict(color=red)))

    fig_call.update_xaxes(title = "Call Value When in the Money")
    fig_put.update_xaxes(title = "Put Value When in the Money")

    for f in (fig, fig_call, fig_put):
        f.update_yaxes(tickvals=[])

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

    return (
        smallfig(fig, showlegend=True),
        smallfig(fig_put),
        smallfig(fig_call),
        f"${put_bs:.2f}",
        f"${call_bs:.2f}",
        f"${np.exp(-r*T)*pd.Series(np.maximum(K-ST,0)).mean():.2f}",
        f"${np.exp(-r*T)*pd.Series(np.maximum(ST-K,0)).mean():.2f}",
    )


