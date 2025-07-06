from pages.formatting import largefig, red, green, blue, yellow
import numpy as np
import plotly.graph_objects as go
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
    wt1,
    wt2,
    rf
):

    mns = np.array((mn1, mn2, mn3)) / 100
    sds = np.array((sd1, sd2, sd3)) / 100
    corr = np.identity(3)
    corr[0,1] = corr[1,0] = c12 / 100
    corr[0,2] = corr[2,0] = c13 / 100
    corr[1,2] = corr[2,1] = c23 / 100
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

    mingrid = 0
    maxgrid = 1.2*np.max(mns)
    mnsFrontier = np.linspace(mingrid, maxgrid, 50)
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
    )



    trace2 = go.Scatter(
        x=sds,
        y=mns,
        text=[1, 2, 3],
        hovertemplate="Asset %{text}<extra></extra>",
        mode="markers",
        marker=dict(size=15, color=red),
    )

    wt1 /= 100
    wt2 /= 100
    rf /= 100

    w = np.array([wt1, wt2, 1-wt1-wt2])
    mean = w @ mns
    stdev = np.sqrt(w @ cov @ w)

    cd = np.empty(shape=(1, 3, 1), dtype=float)
    cd[:, 0] = np.array(wt1)
    cd[:, 1] = np.array(wt2)
    cd[:, 2] = np.array(1-wt1-wt2)
    string = "asset 1: %{customdata[0]:.0%}<br>"
    string += "asset 2: %{customdata[1]:.0%}<br>"
    string += "asset 3: %{customdata[2]:.0%}<br>"
    string += "<extra></extra>"
    trace3 = go.Scatter(
        x=[stdev],
        y=[mean],
        mode="markers",
        marker=dict(size=15, color=blue),
        customdata=cd,
        hovertemplate=string,
    )

    x = np.linspace(0, np.max(sdsFrontier), 51)
    y = rf+x*(mean-rf)/stdev
    trace4 = go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line=dict(color=blue),
        hovertemplate=f"Sharpe ratio = {(mean-rf)/stdev:0.3f}<extra></extra>"
    )
    fig = go.Figure()

    for trace in (trace1, trace2, trace3, trace4):
        fig.add_trace(trace)

    fig.update_xaxes(
        range=[0, 1.25 * np.max(sds)],
        title="Standard Deviation",
        tickformat=".0%"
    )
    fig.update_yaxes(
        range=[0, 1.25 * np.max(mns)],
        title="Expected Return",
        tickformat=".0%"
    )

    return largefig(fig), is_pos_def(cov)
