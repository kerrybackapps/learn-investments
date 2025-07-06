import pandas as pd
import numpy as np
import plotly.graph_objects as go
import numpy_financial as npf
from pages.formatting import largefig, blue, red, green


def mortgage(principal, r, n, balloon, termtype):
    r /= 100
    if termtype == "Monthly":
        r /= 12
        n *= 12
    pmt = -npf.pmt(rate=r, nper=n, pv=principal, fv=-balloon)
    balances = principal * (1 + r) ** np.arange(n + 1) - pmt * np.array(
        [np.sum((1 + r) ** np.arange(i)) for i in range(n + 1)]
    )
    interest = r * balances[:-1]
    balances = pd.DataFrame(balances).reset_index(drop=False)
    balances.columns = ["Period", "Balance"]
    return balances, pmt, interest


def figtbl(principal, r, n, balloon, termtype):
    df, pmt, interest = mortgage(principal, r, n, balloon, termtype)
    df["Balance"].iloc[1:] += pmt
    n = len(interest)
    pp = pmt - interest
    string = "payoff at period %{x:.0f} is $%{y:,.2f}<extra></extra>"
    fig = go.Figure(
        go.Scatter(
            x=df.Period,
            y=df.Balance,
            mode="lines",
            hovertemplate=string,
            fill="tozeroy",
            line={"color": blue},
            name="Remaining Balance",
        )
    )
    fig.layout.xaxis["title"] = "Period"
    fig.layout.yaxis["title"] = "Remaining Loan Balance"
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    fig.update_layout(legend=dict(yanchor="bottom", y=0.01, xanchor="left", x=0.01))

    fig2 = go.Figure()
    string = "interest payment at period %{x:.0f} is $%{customdata:,.2f}<extra></extra>"
    trace1 = go.Scatter(
        x=[i for i in range(1, n + 1)],
        y=[pmt] * n,
        customdata=interest,
        mode="lines",
        hovertemplate=string,
        fill="tonexty",
        line={"color": red},
        name="Interest",
    )
    string = "principal payment at period %{x:.0f} is $%{y:,.2f}<extra></extra>"
    trace2 = go.Scatter(
        x=[i for i in range(1, n + 1)],
        y=pp,
        mode="lines",
        hovertemplate=string,
        fill="tozeroy",
        name="Principal",
        line={"color": green},
    )
    fig2.add_trace(trace1)
    fig2.add_trace(trace2)
    fig2.update_xaxes(rangemode="tozero")
    fig2.layout.xaxis["title"] = "Period"
    fig2.layout.yaxis["title"] = "Allocation of Payment"
    fig2.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    fig2.update_layout(legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99))

    return (
        largefig(fig, showlegend=True),
        largefig(fig2, showlegend=True),
        f"${pmt:,.2f}",
    )
