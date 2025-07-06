import pandas as pd
import numpy as np
from pages.portfolios.portfolios_class import portfolio
from pages.formatting import largefig, green, blue, red
import plotly.graph_objects as go
import yfinance as yf


DATA = pd.DataFrame(0, index=[0], columns=["NotATicker"])

def get_rets(tickers):
    global DATA
    if set(tickers).issubset(set(DATA.columns.to_list())):
        return DATA
    else:
        try:
            df = yf.download(" ".join(tickers), start="1970-01-01")
            DATA = df["Close"].resample("M").last().pct_change().dropna().iloc[:-1]
            DATA.index = DATA.index.to_period("M").astype(str)
            return DATA
        except:
            return DATA

def figtbl(name, dates, rs, extra, radio, tickers):

    minyear = str(dates[0])
    maxyear = str(int(dates[1]) + 1)

    data = get_rets(tickers).copy()
    tickers = data.columns.to_list()

    data = data[(data.index >= minyear) & (data.index < maxyear)]
    mindate = data.index.min()
    maxdate = data.index.max()

    rb = float(rs) + float(extra)
    rs = float(rs) / 100
    rb /= 100
    tickers = [t.upper() for t in tickers]
    Shorts = (radio=="s")
    N = len(tickers)


    mns = data.mean().to_numpy()
    cov = data.cov().to_numpy()
    sds = np.sqrt(np.diag(cov))
    corr = data.corr()
    P = portfolio(mns, cov, Shorts)

    rs /= 12
    rb /= 12

    def mean(w):
        return rs * max(0, 1-np.sum(w)) - rb * max(0, np.sum(w)-1, 0) + w @ mns

    def custom(string, ports):
        cd = np.empty(shape=(len(ports), N, 1), dtype=float)
        for i in range(N):
            cd[:, i] = np.array([w[i] for w in ports]).reshape(-1, 1)
        string += "<br>"
        for i, asset in enumerate(tickers):
            string += asset
            string += ": %{customdata["
            string += str(i)
            string += "]:.1%}<br>"
        string += "<extra></extra>"
        return string, cd

    ravers = np.concatenate((np.arange(2, 10, 0.1), np.arange(10, 40, 5), np.arange(40, 210, 10)))
    mingrid = 0.8 * np.min(mns) if Shorts else np.min(mns)
    maxgrid = 1.2 * np.max(mns) if Shorts else np.max(mns)
    mnsFrontier = np.linspace(mingrid, maxgrid, 50)
    portsFrontier = [P.frontier(m) for m in mnsFrontier]
    mnsFrontier = 12 * mnsFrontier
    sdsFrontier = [np.sqrt(12 * w @ cov @ w) for w in portsFrontier]

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
    portsOptimal = [w for w in portsOptimal if mean(w) <= 1.2 * np.max(mns)]
    mnsOptimal = [12*mean(w) for w in portsOptimal]
    sdsOptimal = [np.sqrt(12 * w @ cov @ w) for w in portsOptimal]

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
        x=np.sqrt(12) * sds,
        y=12*mns,
        mode='markers',
        text=tickers,
        hovertemplate='%{text}<br>mean = %{y:.1%}<br>st dev = %{x:.1%}<extra></extra>',
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
                x=[np.sqrt(12)*sdTang],
                y=[12*mnTang],
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
                x=[np.sqrt(12)*sdTang],
                y=[12*mnTang],
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
    indx = ['Risk Free'] + tickers + ['Mean', 'Std Dev']
    df = pd.DataFrame(dtype=float, columns=ravers, index=indx)
    df.index.name = 'Risk Aver'
    for raver in ravers:
        w = P.optimal(raver=raver, rs=rs, rb=rb)
        save = max(0, 1 - np.sum(w))
        borrow = max(0, np.sum(w) - 1)
        df.loc['Risk Free', raver] = save - borrow
        df.loc['Mean', raver] = 12 * (save * rs - borrow * rb + w @ mns)
        df.loc['Std Dev', raver] = np.sqrt(12 * w @ cov @ w)
        for i, asset in enumerate(tickers):
            df.loc[asset, raver] = w[i]
    for c in df.columns:
        df[c] = df[c].map(lambda x: f'{x:.1%}')
    df = df.reset_index()
    df = df.rename(columns={df.columns[0]: "Risk Aver"})
    df.columns = [name + str(x) for x in df.columns]

    for c in corr.columns:
        corr[c] = corr[c].map(lambda x: f'{x:.1%}')
    corr = corr.reset_index()
    corr = corr.rename(columns={corr.columns[0]: ""})

    return mindate + " through " + maxdate, largefig(fig), df.to_dict('records'), corr.to_dict('records')

