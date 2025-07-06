import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig, green, red, orange, blue, yellow
from pages.portfolios.portfolios_class import portfolio

def data(mn1, mn2, sd1, sd2, c, rs, extra):
    c = c / 100
    rb = rs + extra   
    rs = rs/100
    rb = rb/100
    mns = [mn1, mn2]
    sds = [sd1, sd2]
    grid = np.linspace(0, 1, 101)
    ports = [np.array([w, 1 - w]) for w in grid]
    means = [p.T @ np.array(mns) for p in ports]
    df = pd.DataFrame(means)
    df.columns = ["mean"]
    cov = np.array(
        [[sds[0] ** 2, sds[0] * sds[1] * c], [sds[0] * sds[1] * c, sds[1] ** 2]]
    ).reshape(2, 2)
    df["stdev"] = [np.sqrt(p.T @ cov @ p) for p in ports]
    df["wt1"] = grid
    df["wt2"] = 1 - df.wt1
    for col in ["mean", "stdev"]:
        df[col] = df[col] / 100
    df["sr_s"]= (df["mean"] - rs)/df["stdev"]
    df["sr_b"]= (df["mean"] - rb)/df["stdev"]
   
    return df

def rf_plus_risky(mn, sd, rs, rb, w_min, w_max):
    mn /= 100
    sd /= 100
    rs /= 100
    rb /= 100
    grid = np.linspace(w_min, w_max, 201)
    mns = [(rs + w * (mn - rs) if w <= 1 else rb + w * (mn - rb)) for w in grid]
    sds = [w * sd for w in grid]
    srs = (mn - rs)/sd
    srb = (mn - rb)/sd
    return grid, mns, sds, srs, srb

def rf_plus_risky_nokink(mn, sd, rf, w_min, w_max):
    mn /= 100
    sd /= 100
    rf /= 100
    grid = np.linspace(w_min, w_max, 201)
    mns = [(rf + w * (mn - rf)) for w in grid]
    sds = [w * sd for w in grid]
    return grid, mns, sds


def figtbl(mn1, mn2, sd1, sd2, c, rs, extra):
    df = data(mn1, mn2, sd1, sd2, c, rs, extra)
    
    #Plot the portfolios of the two assets
    trace1 = go.Scatter(
        x=df["stdev"],
        y=df["mean"],
        mode="lines",
        line={'color': green},
        text=100 * df["wt1"],
        customdata=100 * df["wt2"],
        hovertemplate="asset 1: %{text:.0f}%<br>asset 2: %{customdata:.0f}%<extra></extra>",
    )
    
    # Plot each asset
    df = df[df.wt1.isin([0, 1])]
    df["text"] = np.where(df.wt1 == 1, "asset 1", "asset 2")
    trace2 = go.Scatter(
        x=df["stdev"],
        y=df["mean"],
        mode="markers",
        text=df["text"],
        hovertemplate="%{text}<extra></extra>",
        marker=dict(size=15, color=red),
    )

    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    
    def custom(string, ports,srTang):
        cd = np.empty(shape=(len(ports), N+1, 1), dtype=float)
        for i in range(N):
            cd[:, i] = np.array([w[i] for w in ports]).reshape(-1, 1)
        cd[:,N] = np.round(srTang,4)
        print(cd)
        string += "<br>"
        for i in range(N):
            string += "asset " + str(i + 1)
            string += ": %{customdata["
            string += str(i)
            string += "]:.1%}<br>"
        string += "Sharpe ratio: %{customdata[" +  str(N) + "]:.4f}<br>"
        string += "<extra></extra>"
        return string, cd  

    # Plot the tangency portfolios
    c = c / 100
    rb = rs + extra     
    rs = rs/100
    rb = rb/100
    mns = [mn1, mn2]
    mns = np.array(mns) / 100
    sds = [sd1, sd2]
    sds = np.array(sds) / 100
    cov = np.array(
        [[sds[0] ** 2, sds[0] * sds[1] * c], [sds[0] * sds[1] * c, sds[1] ** 2]]
    ).reshape(2, 2)
    
    Shorts = 0.0     
    N = len(mns)
    P = portfolio(mns, cov, Shorts)    
    gmv = P.GMV @ mns
    print('GMV return is: ',gmv)
    if (rs < gmv) or (not Shorts):
        portTang = P.tangency(rs)
        mnTang = portTang @ mns
        if mnTang < np.max(mns):
            sdTang = np.sqrt(portTang @ cov @ portTang)
            srTang = (mnTang - rs)/sdTang
            string = 'tangency portfolio' if rb == rs else 'efficient low risk portfolio' if rb != rs else 'tangency portfolio'
            string, cd = custom(string, [portTang], srTang)
            trace = go.Scatter(
                x=[sdTang],
                y=[mnTang],
                mode="markers",
                customdata=cd,
                hovertemplate=string,
                marker=dict(size=15, color=green),
            )
            fig.add_trace(trace)
            
            #Plot CAL (no leverage)
            grid, mns_cal, sds_cal = rf_plus_risky_nokink(mnTang*100, sdTang*100, rs*100,0, 1.0)
            portlabel = 'tangency portfolio' if rb == rs else 'efficient low risk portfolio' if rb != rs else 'tangency portfolio'
            string = "wealth in "+portlabel + " = %{text:.0f}%<br>" + "Sharpe ratio: " +  "{:.4f}".format(srTang) +"<extra></extra>"
            trace5 = go.Scatter(
                x=sds_cal, y=mns_cal, mode="lines", text=100 * grid, hovertemplate=string, line=dict(color=blue)
            )           
            fig.add_trace(trace5)
            
            #Plot CAL (with leverage)
            grid, mns_cal, sds_cal = rf_plus_risky_nokink(mnTang*100, sdTang*100, rs*100,1.0, 1.5)
            trace5a = go.Scatter(
                x=sds_cal, y=mns_cal, mode="lines", text=100 * grid, hovertemplate=string, line=dict(color=blue, dash='dot')
            )           
            fig.add_trace(trace5a)           
            
            
            
            

    if (rb != rs) and ((gmv > rb) or (not Shorts)):
        portTang = P.tangency(rb)
        mnTang = portTang @ mns
        if mnTang < np.max(mns):
            sdTang = np.sqrt(portTang @ cov @ portTang)
            srTang = (mnTang - rb)/sdTang
            string = 'efficient high mean portfolio'
            string, cd = custom(string, [portTang], srTang)
            trace = go.Scatter(
                x=[sdTang],
                y=[mnTang],
                mode="markers",
                customdata=cd,
                hovertemplate=string,
                marker=dict(size=15, color=green),
            )
            fig.add_trace(trace)
            
            #Plot CAL (with leverage)            
            grid, mns_cal, sds_cal = rf_plus_risky_nokink(mnTang*100, sdTang*100, rb*100, 1.0, 1.5)
            string = "wealth in efficient high mean portfolio = %{text:.0f}%<br>" + "Sharpe ratio (relative to borrowing rate): " + "{:.4f}".format(srTang) +"<extra></extra>"
            trace6 = go.Scatter(
                x=sds_cal, y=mns_cal, mode="lines", text=100 * grid, hovertemplate=string, line=dict(color=blue)
            )           
            fig.add_trace(trace6)   
            
            #Plot CAL (without leverage) 
            grid, mns_cal, sds_cal = rf_plus_risky_nokink(mnTang*100, sdTang*100, rb*100, 0, 1)
            trace6a = go.Scatter(
                x=sds_cal, y=mns_cal, mode="lines", text=100 * grid, hovertemplate=string, line=dict(color=blue, dash='dot')
            )           
            fig.add_trace(trace6a)      

    # Plot the combination of the risk-free and each asset
    grid, mns_cal, sds_cal, srs_cal, srb_cal = rf_plus_risky(mn1, sd1, rs*100, rb*100, 0, 1.0)
    string = "wealth in asset 1 = %{text:.0f}%<br>" + "Sharpe ratio: " + "{:.4f}".format(srs_cal) +"<extra></extra>"
    trace3 = go.Scatter(
        x=sds_cal, y=mns_cal, mode="lines", text=100 * grid, hovertemplate=string, line=dict(color=yellow)
    )
    grid, mns_cal, sds_cal, srs_cal, srb_cal = rf_plus_risky(mn2, sd2, rs*100, rb*100,0, 1.0)
    string = "wealth in asset 2 = %{text:.0f}%<br>" + "Sharpe ratio : " + "{:.4f}".format(srs_cal) +"<extra></extra>"
    trace4 = go.Scatter(
        x=sds_cal, y=mns_cal, mode="lines", text=100 * grid, hovertemplate=string, line=dict(color=yellow)
    )
 
    fig.add_trace(trace3)
    fig.add_trace(trace4)       
    fig.layout.xaxis["title"] = "Standard Deviation"
    fig.layout.yaxis["title"] = "Expected Return"
    fig.update_xaxes(range=[0, 1.25 * df["stdev"].max()])
    fig.update_yaxes(range=[0, 1.25 * df["mean"].max()])
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    # fig.show()
    return largefig(fig)
