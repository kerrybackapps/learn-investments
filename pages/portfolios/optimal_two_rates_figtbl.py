import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.portfolios.portfolios_class import portfolio
from pages.formatting import largefig, green, red, orange, blue, yellow

""" ---------------------------------------------------
set parameters so that saving rate < gmv mean
and saving rate < borrowing rate
three regions in frontier if borrowing rate < gmv mean
two regions if borrowing rate >= gmv mean
----------------------------------------------------"""

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

RAVERS = np.linspace(0.5, 20, 196)

def figtbl(mn1, mn2, mn3, sd1, sd2, sd3, c12, c13, c23, rs, extra, raver):

    mn1, mn2, mn3 = mn1/100, mn2/100, mn3/100
    sd1, sd2, sd3 = sd1/100, sd2/100, sd3/100
    c12, c13, c23 = c12/100, c13/100, c23/100
    rs, extra = rs/100, extra/100
    rb = rs + extra

    mns = np.array([mn1, mn2, mn3])
    sds = np.array([sd1, sd2, sd3])

    R = np.identity(3)
    R[0,1] = R[1,0] = c12
    R[0,2] = R[2,0] = c13
    R[1,2] = R[2,1] = c23
    S = np.diag(sds)
    cov = S @ R @ S

    """--------------------------------------------------
    stop calculations if cov matrix is not pos definite
    -----------------------------------------------------"""

    pdcov = np.all(np.linalg.eigvals(cov) > 0)
    if not pdcov:
        return largefig(go.Figure()), largefig(go.Figure()), "False", ""

    """----------------------------------------------------
    capital allocation curve (fig2)
    -------------------------------------------------------"""

    P = portfolio(mns, cov, Shorts=True)
    opts = [P.optimal(raver=A, rs=rs, rb=rb) for A in RAVERS]
    allocs = [np.sum(x) for x in opts]
    trace = go.Scatter(
        x=RAVERS,
        y=allocs,
        mode="lines",
        hovertemplate="risk aversion = %{x:.1f}<br>allocation to risky assets = %{y:.1%}<extra></extra>"
    )
    fig2 = go.Figure(trace)
    fig2.update_layout(
        xaxis_title="Risk Aversion",
        yaxis_title="Optimal Allocation to Risky Assets",
        yaxis_tickformat=".0%"
    )


    """---------------------------------------------------
    plot three assets
    ------------------------------------------------------"""

    fig1 = go.Figure()

    trace_assets = go.Scatter(
        x=sds,
        y=mns,
        text=["asset 1", "asset 2", "asset 3"],
        mode="markers",
        marker=dict(size=15, color=red),
        hovertemplate="%{text}<extra></extra>",
        showlegend=False
    )

    fig1.add_trace(trace_assets)

    """-----------------------------------------
    plot tangency portfolio at savings rate
    --------------------------------------------"""

    tangs = np.linalg.solve(cov, mns - rs)
    tangs /= np.sum(tangs)
    tangs_mn = tangs @ mns
    tangs_sd = np.sqrt(tangs @ cov @ tangs)

    cd = np.empty(shape=(1, 3, 1), dtype=float)
    for i in range(3):
        cd[:, i] = [tangs[i]]

    trace_tangs = go.Scatter(
        showlegend=False,
        x=[tangs_sd],
        y=[tangs_mn],
        customdata = cd,
        mode = "markers",
        marker = dict(size=15, color=green),
        hovertemplate = "tangency portfolio at the savings rate<br>asset 1 = %{customdata[0]:.1%}<br>asset 2 = %{customdata[1]:.1%}<br>asset 3 = %{customdata[2]:.1%}<br>",
    )

    fig1.add_trace(trace_tangs)

    """-------------------------------------------
    plot frontier from savings rate to tangency
    ----------------------------------------------"""

    grid = np.linspace(0, 1, 51)
    trace_lines = go.Scatter(
        x=[w * tangs_sd for w in grid],
        y=[rs + w * (tangs_mn - rs) for w in grid],
        text=grid,
        mode="lines",
        line=dict(color=blue),
        hovertemplate="allocation to savings-rate tangency portfolio is<br>%{text: .1%}<extra></extra>",
        name="saving",
        legendrank=4
    )

    fig1.add_trace(trace_lines)

    """---------------------------------------------------
    gmv portfolio
    ------------------------------------------------------"""

    gmv = np.linalg.solve(cov, np.ones(3))
    gmv /= np.sum(gmv)
    gmv_mn = gmv @ mns

    """----------------------------------------------------
    optimal portfolio
    -------------------------------------------------------"""

    opt = P.optimal(raver=raver, rs=rs, rb=rb)
    opt_mn = rs + opt @ (mns-rs) if np.sum(opt)<=1 else rb + opt @ (mns-rb)
    opt_sd = np.sqrt(opt @ cov @ opt)

    """----------------------------------------------------
    plot indifference curve
    -------------------------------------------------------"""

    const = opt_mn - 0.5 * raver * opt_sd ** 2
    maxgrid = min(2*opt_sd, max(1.5*opt_sd, 1.2*np.max(sds)))
    grid = np.linspace(0, maxgrid, 51)
    means = const + 0.5 * raver * grid ** 2
    trace_indiff = go.Scatter(
        name="indifference curve",
        x=grid,
        y=means,
        text=[opt_mn]*len(grid),
        customdata=[opt_sd]*len(grid),
        mode="lines",
        line=dict(color=yellow, dash="dot"),
        hovertemplate="equally as good as<br>expected return = %{text:.1%}<br>standard deviation = %{customdata:.1%}<extra></extra>",
        legendrank=2,
    )

    fig1.add_trace(trace_indiff)

    """---------------------------------------------------
    CASES: (i) borrowing rate high, (ii) borrowing rate low
    ------------------------------------------------------"""

    if rb >= gmv_mn:

        """------------------------------------------------
        plot risky assets only 
        ---------------------------------------------------"""

        maxmn = gmv_mn + 3 * (tangs_mn - gmv_mn)
        maxmn = max(maxmn, 1.2 * np.max(mns))
        maxw = (maxmn - rb) / (tangs_mn - rb)
        minw = gmv_mn / (gmv_mn - tangs_mn)
        grid = np.linspace(minw, maxw, 201)
        ports = [w * tangs + (1 - w) * gmv for w in grid]

        trace_risky = go.Scatter(
            x=[np.sqrt(p @ cov @ p) for p in ports],
            y=[p @ mns for p in ports],
            mode="lines",
            line=dict(color=green),
            text=grid,
            customdata=1 - grid,
            hovertemplate="allocation to saving-rate tangency is %{text: .1%}<br>allocation to GMV portfolio is %{customdata: .1%}<extra></extra>",
            name="risky assets only",
            legendrank=3
        )

        """---------------------------------------------
        plot optimum
        ------------------------------------------------"""

        if opt_mn < tangs_mn:
            w = (opt_mn-rs) / (tangs_mn-rs)
            alloc = w
            trace_opt = go.Scatter(
                name="optimum",
                legendrank=1,
                x=[opt_sd],
                y=[opt_mn],
                mode="markers",
                marker=dict(size=18, symbol="star", color=yellow),
                text=[w],
                hovertemplate="optimal portfolio<br>allocation to saving-rate tangency is %{text:.1%}<br>expected return = %{y:.1%}<br>standrd deviation = %{x:.1%}<extra></extra>"
            )
        else:
            w = (opt_mn-gmv_mn) / (tangs_mn-gmv_mn)
            alloc = 1
            trace_opt = go.Scatter(
                name="optimum",
                legendrank=1,
                x=[opt_sd],
                y=[opt_mn],
                mode="markers",
                marker=dict(size=18, symbol="star", color=yellow),
                text=[w],
                customdata=[1-w],
                hovertemplate="optimal portfolio<br>allocation to saving-rate tangency is %{text:.1%}<br>allocation to GMV is %{customdata:.1%}<br>expected return = %{y:.1%}<br>standrd deviation = %{x:.1%}<extra></extra>"
            )




    else:

        """--------------------------------------------
        plot tangency portfolio at borrowing rate
        -----------------------------------------------"""

        tangb = np.linalg.solve(cov, mns - rb)
        tangb /= np.sum(tangb)
        tangb_mn = tangb @ mns
        tangb_sd = np.sqrt(tangb @ cov @ tangb)

        cd = np.empty(shape=(1, 3, 1), dtype=float)
        for i in range(3):
            cd[:, i] = [tangb[i]]

        trace_tangb = go.Scatter(
            showlegend=False,
            x=[tangb_sd],
            y=[tangb_mn],
            customdata=cd,
            mode="markers",
            marker=dict(size=15, color=green),
            hovertemplate="tangency portfolio at the borrowing rate<br>asset 1 = %{customdata[0]:.1%}<br>asset 2 = %{customdata[1]:.1%}<br>asset 3 = %{customdata[2]:.1%}<br>"
        )

        fig1.add_trace(trace_tangb)

        """--------------------------------------------------
        decide how far up to take tangency line and 
        risky-asset-only frontier.  choose max mean for 
        tangency line and use same std dev for risky frontier.
        this is just aesthetics
        ------------------------------------------------------"""

        maxmn = gmv_mn + 2*(tangb_mn - gmv_mn)
        maxmn = max(maxmn, 1.2*np.max(mns))
        maxw = (maxmn-rb) / (tangb_mn-rb)
        grid = np.linspace(1, maxw, 51)

        """---------------------------------------------------
        plot line from borrowing tangency
        ------------------------------------------------------"""

        trace_lineb = go.Scatter(
            x=[w * tangb_sd for w in grid],
            y=[rb + w * (tangb_mn - rb) for w in grid],
            text=grid,
            mode="lines",
            line=dict(color=blue),
            hovertemplate="allocation to borrowing-rate tangency portfolio is<br>%{text: .1%}<extra></extra>",
            name="borrowing",
            legendrank=5
        )

        fig1.add_trace(trace_lineb)

        """------------------------------------------------
        plot risky assets only
        ---------------------------------------------------"""

        maxw = (maxmn - tangs_mn) / (tangb_mn - tangs_mn)
        minw = tangs_mn / (tangs_mn - tangb_mn)
        grid = np.linspace(minw, maxw, 200)

        ports = [w*tangb + (1-w)*tangs for w in grid]
        risky_mns = [p @ mns for p in ports]
        risky_sds = [np.sqrt(p @ cov @ p) for p in ports]

        trace_risky = go.Scatter(
            x=risky_sds,
            y=risky_mns,
            text=1-grid,
            customdata=grid,
            mode="lines",
            line=dict(color=green),
            hovertemplate="allocation to saving-rate tangency is %{text:.0%}<br>allocation to borrowing-rate tangency is %{customdata:.0%}<extra></extra>",
            name="risky assets only",
            legendrank=3
        )

        """---------------------------------------------
        plot optimum
        ------------------------------------------------"""

        if opt_mn < tangs_mn:
            w = (opt_mn - rs) / (tangs_mn - rs)
            alloc = w
            trace_opt = go.Scatter(
                name="optimum",
                legendrank=1,
                x=[opt_sd],
                y=[opt_mn],
                text=[w],
                mode="markers",
                marker=dict(size=18, symbol="star", color=yellow),
                hovertemplate="optimal portfolio<br>allocation to saving-rate tangency is %{text:.1%}<br>expected return = %{y:.1%}<br>standard deviation = %{x:.1%}<extra></extra>"
            )

        elif opt_mn < tangb_mn:
            w = (opt_mn - tangs_mn) / (tangb_mn - tangs_mn)
            alloc = 1
            trace_opt = go.Scatter(
                name="optimum",
                legendrank=1,
                x=[opt_sd],
                y=[opt_mn],
                text=[w],
                customdata=[1-w],
                mode="markers",
                marker=dict(size=18, symbol="star", color=yellow),
                hovertemplate="optimal portfolio<br>allocation to borrowing-rate tangency is %{text:.1%}<br>allocation to saving-rate tangency is %{customdata:.1%}<br>expected return = %{y:.1%}<br>standard deviation = %{x:.1%}<extra></extra>"
            )

        else:
            w = (opt_mn - rb) / (tangb_mn - rb)
            alloc = w
            trace_opt = go.Scatter(
                name="optimum",
                legendrank=1,
                x=[opt_sd],
                y=[opt_mn],
                text=[w],
                mode="markers",
                marker=dict(size=18, symbol="star", color=yellow),
                hovertemplate="optimal portfolio<br>allocation to borrowing-rate tangency is %{text:.1%}<br>expected return = %{y:.1%}<br>standard deviation = %{x:.1%}<extra></extra>"
            )


    fig1.add_trace(trace_risky)
    fig1.add_trace(trace_opt)
    fig1.update_layout(
        xaxis_title="Standard Deviation",
        yaxis_title="Expected Return",
        yaxis_tickformat=".0%",
        xaxis_tickformat=".0%",
        legend=dict(
            xanchor="left",
            yanchor="top",
            y=0.99,
            x=0.01,
        )
    )
    return largefig(fig1, showlegend=True), largefig(fig2), "True", f"{alloc:.1%}"

