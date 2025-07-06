import pandas as pd
from pages.formatting import largefig, green, blue, red
from pages.portfolios.portfolios_class import portfolio
import numpy as np
import plotly.graph_objects as go



def is_pos_def(x):
    if np.all(np.linalg.eigvals(x) > 0):
        return 'True'
    else:
        return 'False'

def figtbl(name, mns, sds, corr, radio, rs, extra):

    ravers = np.concatenate((np.arange(2, 10, 0.1), np.arange(10, 40, 5), np.arange(40, 210, 10)))

    sds = np.array(sds) / 100
    mns = np.array(mns) / 100
    cov = np.diag(sds) @ np.array(corr) @ np.diag(sds) / 100
    Shorts = (radio == "Yes")
    rb = rs + extra
    rs /= 100
    rb /= 100
    N = len(mns)
    P = portfolio(mns, cov, Shorts)

    def mean(w):
        return max(0, 1 - np.sum(w)) * rs - max(0, np.sum(w) - 1) * rb + w @ mns

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

    mingrid = 0.8 * np.min(mns) if Shorts else np.min(mns)
    maxgrid = 1.2 * np.max(mns) if Shorts else np.max(mns)
    mnsFrontier = np.linspace(mingrid, maxgrid, 50)
    portsFrontier = [P.frontier(m) for m in mnsFrontier]
    sdsFrontier = [np.sqrt(w @ cov @ w) for w in portsFrontier]

    string, cd = custom('frontier w/o borrowing or saving', portsFrontier)
    trace1 = go.Scatter(
        x=sdsFrontier,
        y=mnsFrontier,
        mode="lines",
        customdata=cd,
        hovertemplate=string,
        line=dict(color=green),
    )

    portsOptimal = [P.optimal(raver=raver, rs=rs, rb=rb) for raver in ravers]
    mnsOptimal = [mean(w) for w in portsOptimal]
    sdsOptimal = [np.sqrt(w @ cov @ w) for w in portsOptimal]

    string, cd = custom('risk aversion = %{text:.1f}', portsOptimal)
    trace2 = go.Scatter(
        x=sdsOptimal,
        y=mnsOptimal,
        mode="lines",
        text=ravers,
        customdata=cd,
        hovertemplate=string,
        line=dict(color=blue)
    )



    trace3 = go.Scatter(
        x=sds,
        y=mns,
        mode='markers',
        text=[f'Asset {i + 1}' for i in range(N)],
        hovertemplate='%{text}<extra></extra>',
        marker=dict(size=15, color=red)
    )

    fig = go.Figure()
    for trace in (trace2, trace1, trace3):
        fig.add_trace(trace)

    gmv = P.GMV @ mns
    if (rs < gmv) or (not Shorts):
        portTang = P.tangency(rs)
        mnTang = portTang @ mns
        if mnTang < max(np.max(mnsFrontier), np.max(mnsOptimal)):
            sdTang = np.sqrt(portTang @ cov @ portTang)
            string = 'tangency portfolio' if rb == rs else 'efficient low risk portfolio' if rb != rs else 'tangency portfolio'
            string, cd = custom(string, [portTang])
            trace = go.Scatter(
                x=[sdTang],
                y=[mnTang],
                mode="markers",
                customdata=cd,
                hovertemplate=string,
                marker=dict(size=15, color=green),
            )
            fig.add_trace(trace)

    if (rb != rs) and ((gmv > rb) or (not Shorts)):
        portTang = P.tangency(rb)
        mnTang = portTang @ mns
        if mnTang < max(np.max(mnsFrontier), np.max(mnsOptimal)):
            sdTang = np.sqrt(portTang @ cov @ portTang)
            string = 'efficient high mean portfolio'
            string, cd = custom(string, [portTang])
            trace = go.Scatter(
                x=[sdTang],
                y=[mnTang],
                mode="markers",
                customdata=cd,
                hovertemplate=string,
                marker=dict(size=15, color=green),
            )
            fig.add_trace(trace)

    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")

    ravers = [10, 8, 6, 4, 2]
    indx = ['Risk Free'] + ['Asset ' + str(i + 1) for i in range(N)] + ['Mean', 'Std Dev']
    df = pd.DataFrame(dtype=float, columns=ravers, index=indx)
    df.index.name = 'Risk Aver'
    for raver in ravers:
        w = P.optimal(raver=raver, rs=rs, rb=rb)
        save = max(0, 1 - np.sum(w))
        borrow = max(0, np.sum(w) - 1)
        df.loc['Risk Free', raver] = save - borrow
        df.loc['Mean', raver] = save * rs - borrow * rb + w @ mns
        df.loc['Std Dev', raver] = np.sqrt(w @ cov @ w)
        for i in range(N):
            df.loc[f'Asset {i + 1}', raver] = w[i]
    df = df.reset_index()
    df.columns = [name + str(x) for x in df.columns]
    # return largefig(fig), df.to_dict('records'), 
    return largefig(fig), is_pos_def(cov), df.to_dict('records'), 