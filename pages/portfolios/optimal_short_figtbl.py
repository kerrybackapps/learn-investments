import pandas as pd
import numpy as np
import plotly.graph_objects as go
from cvxopt import matrix
from cvxopt.solvers import qp as Solver
from cvxopt.solvers import options as SolverOptions

SolverOptions["show_progress"] = False
from pages.formatting import largefig, red, green, blue
from pages.portfolios.portfolios_class import Portfolios


# -----------------------------------------------
#
# choice variables are xs=amount to save, xb=amount to borrow, and w=portfolio weights
# constraints are xs>=0, xb>=0, w>=0, xs + i'w <= 1, and -xb + i'w <= 1
# objective function (to minimize) is - rs*xs + rb*xb - means'w
#
# -----------------------------------------------


def optimal(rs, rb, means, cov, raver):
    n = len(means)
    Q = np.zeros((n + 2, n + 2))
    Q[2:, 2:] = raver * cov
    Q = matrix(Q, tc="d")  # quadratic form that penalizes variance
    p = np.array([-rs, rb] + list(-np.array(means)))
    p = matrix(p, (len(p), 1), tc="d")  # coefficients of objective function
    g = np.array([1, -1] + n * [1])
    a = np.zeros((2, n + 2))
    a[0, 0] = a[1, 1] = -1
    G = matrix(np.vstack([a, g]))  # coefficients of constraints
    h = np.array(2 * [0] + [1])
    h = matrix(h, (len(h), 1), tc="d")  # right-hand side of constraints
    sol = Solver(Q, p, G, h)
    return (
        pd.Series(sol["x"][2:], index=means.index)
        if sol["status"] == "optimal"
        else pd.Series(np.nan, index=means.index)
    )


def data(mn1, mn2, mn3, sd1, sd2, sd3, c12, c13, c23, rs, rb):
    rs /= 100
    rb /= 100
    mns = pd.Series(
        np.array([mn1, mn2, mn3]) / 100, index=["stock1", "stock2", "stock3"]
    )
    sds = np.array([sd1, sd2, sd3]) / 100
    C = np.identity(3)
    C[0, 1], C[1, 0] = c12 / 100, c12 / 100
    C[0, 2], C[2, 0] = c13 / 100, c13 / 100
    C[1, 2], C[2, 1] = c23 / 100, c23 / 100
    C = np.diag(sds) @ C @ np.diag(sds)
    ravers = (
        list(np.arange(0.1, 10.1, 0.1))
        + list(np.arange(10, 45, 5))
        + list(np.arange(40, 220, 10))
    )
    ravers = np.sort(list(set(ravers)))
    df = pd.DataFrame(
        dtype=float,
        index=range(len(ravers)),
        columns=["raver", "mean", "stdev", "wt1", "wt2", "wt3"],
    )
    df["raver"] = ravers
    ports = [optimal(rs, rb, mns, C, raver) for raver in ravers]
    df["mean"] = [
        rs * max(1 - np.sum(p), 0) - rb * max(np.sum(p) - 1, 0) + p @ mns for p in ports
    ]
    df["stdev"] = [np.sqrt(p @ C @ p) for p in ports]
    for i in range(3):
        df["wt" + str(i + 1)] = [100 * p[i] for p in ports]
    return df, sds, mns

def figtbl(mn1, mn2, mn3, sd1, sd2, sd3, c12, c13, c23, rs, xtra):
    df, sds, mns = data(mn1, mn2, mn3, sd1, sd2, sd3, c12, c13, c23, rs, rs + xtra)

    mns_l = [mn1, mn2, mn3]
    sds_l = [sd1, sd2, sd3]
    c_l = [c12, c13, c23]
    assets = Portfolios.fromCorrelations(
        3, mns_l, sds_l, c_l, saving_rate=rs, borrowing_extra=xtra
    )
    port_s, mn_s, std_s = assets.tang_port(isSaving=True)
    port_b, mn_b, std_b = assets.tang_port(isSaving=False)

    # Optimal curve, blue line
    cd = np.empty(shape=(df.shape[0], 3, 1), dtype=float)
    cd[:, 0] = np.array(df.wt1).reshape(-1, 1)
    cd[:, 1] = np.array(df.wt2).reshape(-1, 1)
    cd[:, 2] = np.array(df.wt3).reshape(-1, 1)
    string = "risk aversion=%{text:.1f}<br>"
    string += "asset 1: %{customdata[0]:.0f}%<br>"
    string += "asset 2: %{customdata[1]:.0f}%<br>"
    string += "asset 3: %{customdata[2]:.0f}%<br>"
    string += "<extra></extra>"
    trace1 = go.Scatter(
        x=df["stdev"],
        y=df["mean"],
        mode="lines",
        text=df.raver,
        customdata=cd,
        hovertemplate=string,
        line=dict(color=blue),
    )

    # Asset dots
    trace2 = go.Scatter(
        x=sds,
        y=mns,
        mode="markers",
        text=["asset 1", "asset 2", "asset 3"],
        hovertemplate="%{text}<extra></extra>",
        marker=dict(size=15, color=red),
    )

    # Tangency portfolios
    cd = np.empty(shape=(1, 3, 1), dtype=float)
    cd[:, 0] = np.array(df.wt1).reshape(-1, 1)
    cd[:, 1] = np.array(df.wt2).reshape(-1, 1)
    cd[:, 2] = np.array(df.wt3).reshape(-1, 1)
    string = "%{text}<br>"
    string += "asset 1: %{customdata[0]:.0f}%<br>"
    string += "asset 2: %{customdata[1]:.0f}%<br>"
    string += "asset 3: %{customdata[2]:.0f}%<br>"
    string += "<extra></extra>"
    trace3 = go.Scatter(
        x=[std_s],
        y=[mn_s],
        mode="markers",
        text=["tangency portfolio"],
        customdata=cd,
        hovertemplate=string,
        marker=dict(size=20, color=green, symbol="star"),
    )

    trace4 = go.Scatter(
        x=[std_s],
        y=[mn_s],
        mode="markers",
        text=["efficient low-risk portfolio"],
        hovertemplate="%{text}<extra></extra>",
        marker=dict(size=15, color=green),
    )
    trace5 = go.Scatter(
        x=[std_b],
        y=[mn_b],
        mode="markers",
        text=["efficient high-mean portfolio"],
        hovertemplate="%{text}<extra></extra>",
        marker=dict(size=15, color=green),
    )

    # Extended frontiers
    #   at saving rate
    sharpe_s = (mn_s - assets.rs) / std_s  # sharpe ratio
    dx = np.linspace(0, 5, 10)
    sds_s = std_s + dx
    mns_s = mn_s + sharpe_s * dx
    trace6 = go.Scatter(
        x=sds_s, y=mns_s, mode="lines", line=dict(color=blue, dash="dot")
    )

    #   at borrowing rate
    sharpe_b = (mn_b - assets.rb) / std_b
    dx = np.linspace(-std_b, 0, 10)
    sds_b = std_b + dx
    mns_b = mn_b + sharpe_b * dx
    trace7 = go.Scatter(
        x=sds_b, y=mns_b, mode="lines", line=dict(color=blue, dash="dot")
    )

    # Optimal with no risk-free asset, green line
    assets.short = True
    assets.risk_free = False
    trace8 = assets.curve_trace(line=dict(color=green))

    fig = go.Figure()
    if xtra == 0:  # when borrowing rate = saving rate
        for trace in [
            trace8,
            trace7,
            trace6,
            trace3,
            trace2,
            trace1,
        ]:  # The order here matters. The latter layer shows on the top.
            fig.add_trace(trace)
    elif assets.rb < assets.gmv_port()[1]:  # when gmv return > borrowing rate
        for trace in [trace8, trace7, trace6, trace5, trace4, trace2, trace1]:
            fig.add_trace(trace)
    else:  # when gmv return <= borrowing rate, hide tangency portfolio and dotted at borrowing rate
        for trace in [trace8, trace6, trace4, trace2, trace1]:
            fig.add_trace(trace)

    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    fig.update_xaxes(range=[0, 1.25 * max(np.max(sds), std_b)])
    fig.update_yaxes(range=[0, 1.25 * max(np.max(mns), mn_b)])
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    return largefig(fig)
