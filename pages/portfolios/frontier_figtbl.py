from pages.formatting import largefig, red, green, blue
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
    c23
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
            string += "]:.1%}<br>"
        string += "<extra></extra>"
        return string, cd

    P = portfolio(means=mns, cov=cov, Shorts=True)

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

    gmv = P.GMV

    cd = np.empty(shape=(1, 3, 1), dtype=float)
    cd[:, 0] = np.array(gmv[0])
    cd[:, 1] = np.array(gmv[1])
    cd[:, 2] = np.array(gmv[2])
    string = "GMV portfolio<br>"
    string += "asset 1: %{customdata[0]:.1%}<br>"
    string += "asset 2: %{customdata[1]:.1%}<br>"
    string += "asset 3: %{customdata[2]:.1%}<br>"
    string += "<extra></extra>"
    trace1a = go.Scatter(
        x=[np.sqrt(gmv @ cov @ gmv)],
        y=[gmv @ mns],
        mode="markers",
        customdata=cd,
        hovertemplate=string,
        marker=dict(size=15, color=green)
    )

    P = portfolio(mns, cov, True)

    mingrid = 0.8*np.min(mns)
    maxgrid = 1.2*np.max(mns)
    mnsFrontier = np.linspace(mingrid, maxgrid, 50)
    portsFrontier = [P.frontier(m) for m in mnsFrontier]
    sdsFrontier = [np.sqrt(w @ cov @ w) for w in portsFrontier]

    string, cd = custom('frontier with short sales', portsFrontier)
    trace2 = go.Scatter(
        x=sdsFrontier,
        y=mnsFrontier,
        mode="lines",
        customdata=cd,
        hovertemplate=string,
        line=dict(color=blue),
    )

    gmv = P.GMV

    trace2a = go.Scatter(
        x=[np.sqrt(gmv @ cov @ gmv)],
        y = [gmv @ mns],
        mode = "markers",
        hovertemplate = 'GMV portfolio with short sales<extra></extra>',
        marker = dict(size=15, color=blue)
    )

    trace3 = go.Scatter(
        x=sds,
        y=mns,
        text=[1, 2, 3],
        hovertemplate="Asset %{text}<extra></extra>",
        mode="markers",
        marker=dict(size=15, color=red),
    )

    fig = go.Figure()
    
    # for trace in (trace1, trace1a, trace2, trace2a, trace3):
    for trace in (trace1, trace1a, trace3):
        fig.add_trace(trace)
    #trace1=frontier w/o short sales
    #trace1a=GMV portfolio w/o short sales
    #trace2=frontier with short sales
    #trace2a=GMV portfolio with short sales
    #trace3=Assets
        
        
    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    fig.update_xaxes(range=[0, 1.25 * np.max(sds)])
    fig.update_yaxes(range=[0, 1.25 * np.max(mns)])
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    return largefig(fig), is_pos_def(cov)
