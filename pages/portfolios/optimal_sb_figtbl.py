import pandas as pd
from pages.formatting import largefig, green, blue, red
import numpy as np
import plotly.graph_objects as go
from pages.portfolios.portfolios_class import portfolio
from pages.data.sbb import nominal as df
# from pages.data.gold import gold


# df = pd.concat((nominal, gold), axis=1).dropna()
assets = ['S&P 500', 'Gold', 'Corporates', 'Treasuries']
df = df[assets]


def means_cov(dates):
    d1 = df.loc[dates[0]:dates[1]]
    return d1.mean().to_numpy(), d1.cov().to_numpy(), d1.corr()

def figtbl(name, dates, rs, extra, radio):

    rb = float(rs) + float(extra)
    rs = float(rs) / 100
    rb /= 100
    mns, cov, corr = means_cov(dates)
    sds = np.sqrt(np.diag(cov))
    Shorts = (radio=="s")
    P = portfolio(mns, cov, Shorts)
    N = len(mns)

    def mean(w):
        return rs * max(0, 1-np.sum(w)) - rb * max(0, np.sum(w)-1, 0) + w @ mns

    def custom(string, ports):
        cd = np.empty(shape=(len(ports), N, 1), dtype=float)
        for i in range(N):
            cd[:, i] = np.array([w[i] for w in ports]).reshape(-1, 1)
        string += "<br>"
        for i, asset in enumerate(assets):
            string += asset
            string += ": %{customdata["
            string += str(i)
            string += "]:.1%}<br>"
        string += "<extra></extra>"
        return string, cd

    assets = ["S&P 500", "Gold", "Corporates", "Treasuries"]

    ravers = np.concatenate((np.arange(2, 10, 0.1), np.arange(10, 40, 2), np.arange(40, 210, 10)))

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
        text=assets,
        hovertemplate='%{text}<br>mean = %{y:.1%}<br>std dev = %{x:.1%}<extra></extra>',
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
            string = 'tangency portfolio' if rb == rs else 'savings-rate tangency' if rb != rs else 'tangency portfolio'
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
            string = 'borrowing-rate tangency'
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
    indx = ['Risk Free'] + assets + ['Mean', 'Std Dev']
    df = pd.DataFrame(dtype=float, columns=ravers, index=indx)
    df.index.name = 'Risk Aver'
    for raver in ravers:
        w = P.optimal(raver=raver, rs=rs, rb=rb)
        save = max(0, 1 - np.sum(w))
        borrow = max(0, np.sum(w) - 1)
        df.loc['Risk Free', raver] = save - borrow
        df.loc['Mean', raver] = save * rs - borrow * rb + w @ mns
        df.loc['Std Dev', raver] = np.sqrt(w @ cov @ w)
        for i, asset in enumerate(assets):
            df.loc[asset, raver] = w[i]
    for c in df.columns:
        df[c] = df[c].map(lambda x: f'{x:.1%}')
    df = df.reset_index()
    df = df.rename(columns={df.columns[0]: "Risk Aversion"})
    df.columns = [name + str(x) for x in df.columns]

    for c in corr.columns:
        corr[c] = corr[c].map(lambda x: f'{x:.1%}')
    corr = corr.reset_index()
    corr = corr.rename(columns={corr.columns[0]: ""})
    corr.columns = [name + str(x) for x in corr.columns]

    return largefig(fig), df.to_dict('records'), corr.to_dict('records')

