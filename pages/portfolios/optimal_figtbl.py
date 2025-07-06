import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig, green, red, orange, blue, yellow
from pages.portfolios.portfolios_class import portfolio

def is_pos_def(x):
    if np.all(np.linalg.eigvals(x) > 0):
        return 'True'
    else:
        return 'False'


def figtbl(
        mn1,
        mn2,
        mn3,
        sd1,
        sd2,
        sd3,
        c12,
        c13,
        c23,
        rf,
        A
):
    mns = np.array((mn1, mn2, mn3)) / 100
    sds = np.array((sd1, sd2, sd3)) / 100
    corr = np.identity(3)
    corr[0, 1] = corr[1, 0] = c12 / 100
    corr[0, 2] = corr[2, 0] = c13 / 100
    corr[1, 2] = corr[2, 1] = c23 / 100
    cov = np.diag(sds) @ corr @ np.diag(sds)
    N = 3

    def custom(string, ports):
        cd = np.empty(shape=(len(ports), N, 1), dtype=float)
        for i in range(N):
            cd[:, i] = np.array([w[i] for w in ports]).reshape(-1, 1)
        string += "<br>"
        for i in range(N):
            string += "asset " + str(i + 1)
            string += ": %{customdata["
            string += str(i)
            string += "]:.0%}<br>"
        string += "<extra></extra>"
        return string, cd

    P = portfolio(mns, cov, True)

    maxgrid = 1.2 * np.max(mns)
    w = P.frontier(maxgrid)
    maxstd = np.sqrt(w @ cov @ w)
    while maxstd < 1.1*np.max(sds):
        maxgrid *= 1.1
        w = P.frontier(maxgrid)
        maxstd = np.sqrt(w @ cov @ w)

    mnsFrontier = np.linspace(0, maxgrid, 50)
    portsFrontier = [P.frontier(m) for m in mnsFrontier]
    sdsFrontier = [np.sqrt(w @ cov @ w) for w in portsFrontier]

    string, cd = custom('frontier', portsFrontier)
    trace1 = go.Scatter(
        x=sdsFrontier,
        y=mnsFrontier,
        mode="lines",
        customdata=cd,
        hovertemplate=string,
        line=dict(color=green),
        name = 'frontier',
        legendrank=3
    )

    trace2 = go.Scatter(
        x=sds,
        y=mns,
        text=[1, 2, 3],
        hovertemplate="Asset %{text}<extra></extra>",
        mode="markers",
        marker=dict(size=15, color=red),
        showlegend=False,
    )

    rf /= 100
    w = P.tangency(rf)
    tangmean = w @ mns
    tangstd = np.sqrt(w @ cov @ w)
    sharpe = (tangmean-rf) / tangstd

    cd = np.empty(shape=(1, 3, 1), dtype=float)
    cd[:, 0] = np.array(w[0])
    cd[:, 1] = np.array(w[1])
    cd[:, 2] = np.array(w[2])
    string = "Tangency portfolio:<br>"
    string += "asset 1: %{customdata[0]:.0%}<br>"
    string += "asset 2: %{customdata[1]:.0%}<br>"
    string += "asset 3: %{customdata[2]:.0%}<br>"
    string += "<extra></extra>"
    trace3 = go.Scatter(
        x=[tangstd],
        y=[tangmean],
        mode="markers",
        marker=dict(size=15, color=blue),
        customdata=cd,
        hovertemplate=string,
        name='tangency',
        legendrank=5
    )

    opt = np.linalg.solve(cov, (mns-rf)/A)
    optmean = rf + opt @ (mns-rf)
    optstd = np.sqrt(opt @ cov @ opt)
    optalloc = np.sum(opt)

    trace5 = go.Scatter(
        x=[optstd],
        y=[optmean],
        mode="markers",
        marker=dict(size=18, symbol="star", color=yellow),
        text=[optalloc],
        hovertemplate="""
        Optimal portfolio<br>
        allocation to risky assets = %{text:.1%}<br>
        expected return = %{y:.1%}<br>
        standard deviation = %{x: .1%}<extra></extra>
        """,
        name='optimum',
        legendrank=1
    )

    maxgrid = max(1.2*optstd, np.max(sdsFrontier))
    x = np.linspace(0, maxgrid, 51)
    y = rf + x * (tangmean - rf) / tangstd
    z = (y-rf) / (tangmean-rf)
    trace4 = go.Scatter(
        x=x,
        y=y,
        text=z,
        mode="lines",
        line=dict(color=blue),
        hovertemplate="Allocation to tangency portfolio = %{text:.1%}<extra></extra>",
        name='capital allocation line',
        legendrank=4
    )

    const = optmean - 0.5*A*optstd**2
    grid = np.linspace(0, maxgrid, 51)
    means = const + 0.5*A*grid**2
    trace6 = go.Scatter(
        x=grid,
        y=means,
        mode="lines",
        line=dict(color=yellow, dash="dot"),
        hovertemplate=f"""
        equally as good as<br>
        expected return = {optmean:.1%},<br>
        standard deviation = {optstd:.1%}<extra></extra>
        """,
        name='indifference curve',
        legendrank=2
    )
    fig = go.Figure()

    for trace in (trace1, trace2, trace3, trace4, trace5, trace6):
        fig.add_trace(trace)

    fig.update_xaxes(
        range=[0, maxgrid],
        title="Standard Deviation",
        tickformat=".0%"
    )
    fig.update_yaxes(
        range=[0, rf+sharpe*maxgrid],
        title="Expected Return",
        tickformat=".0%"
    )
    fig.update_layout(
        legend=dict(
            xanchor="left",
            yanchor="top",
            y=0.99,
            x=0.01,
        )
    )

    return largefig(fig, showlegend=True), is_pos_def(cov), f"{optalloc:.1%}"