from pages.portfolios.portfolios_class import portfolio


def data(mn1, mn2, sd1, sd2, c, rs, extra):
    c = c / 100
    rb = rs + extra
    rs = rs / 100
    rb = rb / 100
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
    df["sr_s"] = (df["mean"] - rs) / df["stdev"]
    df["sr_b"] = (df["mean"] - rb) / df["stdev"]

    return df


def rf_plus_risky(mn, sd, rs, rb, w_min, w_max):
    mn /= 100
    sd /= 100
    rs /= 100
    rb /= 100
    grid = np.linspace(w_min, w_max, 201)
    mns = [(rs + w * (mn - rs) if w <= 1 else rb + w * (mn - rb)) for w in grid]
    sds = [w * sd for w in grid]
    srs = (mn - rs) / sd
    srb = (mn - rb) / sd
    return grid, mns, sds, srs, srb


def opt_utility(mns, cov, Shorts, s, b, A):
    # P is a portfolio object based on expected returns, covariance matrix, and shorts
    P = portfolio(mns, cov, Shorts)
    gmv = P.GMV @ mns
    if s == b:
        # tangency exp ret and sd
        if (s < gmv) or (not Shorts):
            portTang = P.tangency(s)
            mnTang = portTang @ mns
            if mnTang < np.max(mns):
                sdTang = np.sqrt(portTang @ cov @ portTang)

                # optimal weight in tangency based on risk-aversion
                wgt = (mnTang - s) / (A * (sdTang ** 2))
                expret = wgt * mnTang + (1 - wgt) * s
                sdret = wgt * sdTang
                wgt_rf = 1 - wgt
                wgt_lo = wgt
                wgt_hi = 0.0
    else:
        # efficient low-risk portfolio
        if (s < gmv) or (not Shorts):
            portTangLowRisk = P.tangency(s)
            mnTangLowRisk = portTangLowRisk @ mns
            if mnTangLowRisk < np.max(mns):
                sdTangLowRisk = np.sqrt(portTangLowRisk @ cov @ portTangLowRisk)

        # efficient high-risk portfolio
        if ((b < gmv) or (not Shorts)):
            portTangHighRisk = P.tangency(b)
            mnTangHighRisk = portTangHighRisk @ mns
            if mnTangHighRisk < np.max(mns):
                sdTangHighRisk = np.sqrt(portTangHighRisk @ cov @ portTangHighRisk)

        # 1st: efficient low risk CAL
        wgt = (mnTangLowRisk - s) / (A * (sdTangLowRisk ** 2))
        expret = wgt * mnTangLowRisk + (1 - wgt) * s
        sdret = wgt * sdTangLowRisk
        wgt_rf = 1 - wgt
        wgt_lo = wgt
        wgt_hi = 0.0
        # print('Weight low risk CAL: ', wgt)
        if wgt > 1.0:
            # 2nd: efficient high risk CAL
            wgt = (mnTangHighRisk - b) / (A * (sdTangHighRisk ** 2))
            expret = wgt * mnTangHighRisk + (1 - wgt) * b
            sdret = wgt * sdTangHighRisk
            wgt_rf = 1 - wgt
            wgt_lo = 0.0
            wgt_hi = wgt
            # print('Weight high risk CAL: ', wgt)
            if wgt < 1.0:
                # 3rd: risky asset frontier
                wgt = 1  # This is should be interpreted as total weight in risky assets.
                # Method 1: solve analytically for utility-maximizing mix of efficient low and high risk portfolios
                cov_hilo = portTangLowRisk.T @ cov @ portTangHighRisk
                wgt_lo = (mnTangLowRisk - mnTangHighRisk - A * (cov_hilo - sdTangHighRisk ** 2)) / (
                            A * (sdTangLowRisk ** 2 + sdTangHighRisk ** 2 - 2 * cov_hilo))
                expret = wgt_lo * mnTangLowRisk + (1 - wgt_lo) * mnTangHighRisk
                sdret = np.sqrt(
                    (wgt_lo ** 2) * sdTangLowRisk ** 2 + ((1 - wgt_lo) ** 2) * sdTangHighRisk ** 2 + 2 * wgt_lo * (
                                1 - wgt_lo) * portTangLowRisk.T @ cov @ portTangHighRisk)
                wgt_hi = 1 - wgt_lo
                wgt_rf = 0.0

                # #Method 2: calculate frontier manually and choose max utility
                # eret_grid = np.linspace(mnTangLowRisk, mnTangHighRisk, 100)
                # df = pd.DataFrame(dtype='float', columns=['mn','sd','u'],index=np.arange(0,100))
                # for i,m in enumerate(eret_grid):
                #     portFrontier = P.frontier(m)
                #     df.loc[i,'mn'] = portFrontier @ mns
                #     df.loc[i,'sd'] = np.sqrt(portFrontier @ cov @ portFrontier)
                # df['u']  = df['mn'] - 0.5*A* df['sd']**2
                # opt_mn = df.loc[df['u'].idxmax(),'mn']
                # portFrontier = P.frontier(opt_mn)
                # expret = portFrontier @ mns
                # sdret  = np.sqrt(portFrontier @ cov @ portFrontier)
                # print('Weight frontier: ', wgt)

    u = expret - 0.5 * A * sdret ** 2
    return u, wgt, wgt_rf, wgt_lo, wgt_hi




df = data(mn1, mn2, sd1, sd2, c, rs, extra)

# Plot the portfolios of the two assets
trace1 = go.Scatter(
    x=df["stdev"],
    y=df["mean"],
    mode="lines",
    text=100 * df["wt1"],
    customdata=100 * df["wt2"],
    hovertemplate="asset 1: %{text:.0f}%<br>asset 2: %{customdata:.0f}%<extra></extra>",
    line=dict(color=green)
)

# Plot the two assets
df = df[df.wt1.isin([0, 1])]
df["text"] = np.where(df.wt1 == 1, "asset 1", "asset 2")
trace2a = go.Scatter(
    x=df[df.wt1 == 1]["stdev"],
    y=df[df.wt1 == 1]["mean"],
    mode="markers",
    text=df[df.wt1 == 1]["text"],
    hovertemplate="%{text}<extra></extra>",
    marker=dict(size=10, color=orange)
)
trace2b = go.Scatter(
    x=df[df.wt1 == 0]["stdev"],
    y=df[df.wt1 == 0]["mean"],
    mode="markers",
    text=df[df.wt1 == 0]["text"],
    hovertemplate="%{text}<extra></extra>",
    marker=dict(size=10, color=red)
)

fig = go.Figure()
fig.add_trace(trace2a)
fig.add_trace(trace2b)
fig.add_trace(trace1)


def custom(string, ports, srTang, borrow_flag):
    # borrow_flag=1 adds statement about "relative to borrowing rate"
    cd = np.empty(shape=(len(ports), N + 1, 1), dtype=float)
    for i in range(N):
        cd[:, i] = np.array([w[i] for w in ports]).reshape(-1, 1)
    cd[:, N] = np.round(srTang, 4)
    # print(cd)
    string += "<br>"
    for i in range(N):
        string += "asset " + str(i + 1)
        string += ": %{customdata["
        string += str(i)
        string += "]:.1%}<br>"
    if borrow_flag == 1:
        string += "Sharpe ratio (relative to borrowing rate): %{customdata[" + str(N) + "]:.4f}<br>"
    else:
        string += "Sharpe ratio: %{customdata[" + str(N) + "]:.4f}<br>"
    string += "<extra></extra>"
    return string, cd


# Plot the tangency portfolios
c = c / 100
rb = rs + extra
rs = rs / 100
rb = rb / 100
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
# print('GMV return is: ',gmv)
if (rs < gmv) or (not Shorts):
    portTang = P.tangency(rs)
    mnTang = portTang @ mns
    if mnTang < np.max(mns):
        sdTang = np.sqrt(portTang @ cov @ portTang)
        srTang = (mnTang - rs) / sdTang
        string0 = 'tangency portfolio' if rb == rs else 'efficient low risk portfolio' if rb != rs else 'tangency portfolio'
        string, cd = custom(string0, [portTang], srTang, 0)
        trace = go.Scatter(
            x=[sdTang],
            y=[mnTang],
            mode="markers",
            customdata=cd,
            hovertemplate=string,
            marker=dict(size=10, color=green)
        )
        fig.add_trace(trace)

        # Plot CAL (no leverage)
        if rb == rs:
            max_wgt = 4.0
        else:
            max_wgt = 1.0
        grid, mns_cal, sds_cal, srs_cal, srb_cal = rf_plus_risky(mnTang * 100, sdTang * 100, rs * 100, rb * 100, 0,
                                                                 max_wgt)
        portlabel = 'tangency portfolio' if rb == rs else 'efficient low risk portfolio' if rb != rs else 'tangency portfolio'
        string = "wealth in " + portlabel + " = %{text:.0f}%<br>" + "Sharpe ratio: " + "{:.4f}".format(
            srTang) + "<extra></extra>"
        trace5 = go.Scatter(
            x=sds_cal,
            y=mns_cal,
            mode="lines",
            text=100 * grid,
            hovertemplate=string,
            line=dict(color=blue)
        )
        fig.add_trace(trace5)

if (rb != rs) and ((gmv > rb) or (not Shorts)):
    portTang = P.tangency(rb)
    mnTang = portTang @ mns
    if mnTang < np.max(mns):
        sdTang = np.sqrt(portTang @ cov @ portTang)
        srTang = (mnTang - rb) / sdTang
        string = 'efficient high mean portfolio'
        string, cd = custom(string, [portTang], srTang, 1)
        trace = go.Scatter(
            x=[sdTang],
            y=[mnTang],
            mode="markers",
            customdata=cd,
            hovertemplate=string,
            marker=dict(size=10, color=green)
        )
        fig.add_trace(trace)

        # Plot CAL (with leverage)
        grid, mns_cal, sds_cal, srs_cal, srb_cal = rf_plus_risky(mnTang * 100, sdTang * 100, rs * 100, rb * 100, 1.0,
                                                                 1.5)
        string = "wealth in efficient high mean portfolio = %{text:.0f}%<br>" + "Sharpe ratio (relative to borrowing rate): " + "{:.4f}".format(
            srTang) + "<extra></extra>"
        trace6 = go.Scatter(
            x=sds_cal,
            y=mns_cal,
            mode="lines",
            text=100 * grid,
            hovertemplate=string,
            line=dict(color=blue)
        )
        fig.add_trace(trace6)

    # Utility plot info
u1, wgt, wgt_rf, wgt_lo, wgt_hi = opt_utility(mns, cov, Shorts, rs, rb, raver)
grid = np.linspace(0, 1.4, 100)
sds = [w * np.max(sds) for w in grid]
eret = [u1 + 0.5 * raver * (sd ** 2) for sd in sds]
string = "indifference curve for <br> optimal utility for risk aversion of " + str(
    np.round(raver, 1)) + "<extra></extra>"
trace7 = go.Scatter(
    x=sds, y=eret, mode="lines", hovertemplate=string, line=dict(color=yellow, dash='dot'),
)
fig.add_trace(trace7)

fig.layout.xaxis["title"] = "Standard Deviation"
fig.layout.yaxis["title"] = "Expected Return"
fig.update_xaxes(range=[0, 1.25 * df["stdev"].max()])
fig.update_yaxes(range=[0, 1.25 * df["mean"].max()])
fig.update_yaxes(tickformat=".0%")
fig.update_xaxes(tickformat=".0%")
# fig.show()


# 2nd plot of risky asset share as function of risk aversion:
ravers = np.arange(0.2, 20, 0.1)
cd = np.empty(shape=(len(ravers), 5, 1), dtype=float)
wgts = [opt_utility(mns, cov, Shorts, rs, rb, A) for A in ravers]
df = pd.DataFrame(wgts, columns=['u', 'wgt_risky', 'wgt_rf', 'wgt_lowrisk', 'wgt_highrisk'])
if (rb != rs):
    custdat = np.empty(shape=(df.shape[0], 3, 1), dtype=float)
    custdat[:, 0] = np.array(100 * df.wgt_rf).reshape(-1, 1)
    custdat[:, 1] = np.array(100 * df.wgt_lowrisk).reshape(-1, 1)
    custdat[:, 2] = np.array(100 * df.wgt_highrisk).reshape(-1, 1)
    string = 'risk aversion: %{x:.1f}<br>'
    string += 'risk-free: %{customdata[0]:.0f}%<br>'
    string += 'efficient low risk: %{customdata[1]:.0f}%<br>'
    string += 'efficient high mean: %{customdata[2]:.0f}%<br>'
    string += '<extra></extra>'
    trace1 = go.Scatter(
        x=ravers,
        y=df['wgt_risky'],
        mode='lines',
        customdata=custdat,
        hovertemplate=string,
        line=dict(color=blue)
    )
    fig2 = go.Figure()
    fig2.add_trace(trace1)
else:
    custdat = np.empty(shape=(df.shape[0], 2, 1), dtype=float)
    custdat[:, 0] = np.array(100 * df.wgt_rf).reshape(-1, 1)
    custdat[:, 1] = np.array(100 * df.wgt_lowrisk).reshape(-1, 1)
    string = 'risk-free: %{customdata[0]:.0f}%<br>'
    string += 'tangency: %{customdata[1]:.0f}%<br>'
    string += '<extra></extra>'
    trace1 = go.Scatter(
        x=ravers,
        y=df['wgt_risky'],
        mode='lines',
        customdata=custdat,
        hovertemplate=string,
        line=dict(color=blue)
    )
    fig2 = go.Figure()
    fig2.add_trace(trace1)
fig2.layout.xaxis["title"] = "Risk Aversion"
fig2.layout.yaxis["title"] = "Weight in Risky Assets"
fig2.update_yaxes(tickformat=".0%")
fig2.update_xaxes(tickformat=".2")
# fig2.show()