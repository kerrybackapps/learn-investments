import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig, plotly_template


def figtbl(maturity, inflation, coupon_rate_treasury, coupon_rate_tips):
    # coupon_rate is in pct
    principal = 100
    n = int(maturity * 2)
    coupon_treasury = coupon_rate_treasury / 2  # coupon of regular treasury in $
    coupon_tips = coupon_rate_tips / 2  # coupon of tips in $
    inflation = inflation / 2  # inflation rate for semi-year

    # nominal cash flows
    # tips
    adj_principal_nominal = principal * ((1 + inflation / 100) ** np.arange(1, n + 1))
    ncashFlows_tips = adj_principal_nominal * (coupon_tips / 100)
    ncashFlows_tips[-1] += adj_principal_nominal[-1]

    # regular treasury
    ncashFlows_treasury = [coupon_treasury] * n
    ncashFlows_treasury[-1] += 100

    # real cash flows
    # tips
    rcashFlows_tips = [coupon_tips] * n
    rcashFlows_tips[-1] += 100

    # regular treasury
    adj_principal_real = principal / ((1 + inflation / 100) ** np.arange(1, n + 1))
    rcashFlows_treasury = adj_principal_real * (coupon_treasury / 100)
    rcashFlows_treasury[-1] += adj_principal_real[-1]

    df = pd.DataFrame(
        dtype=float,
        index=np.arange(0.5, (n + 1) / 2, 0.5),
        columns=[
            "cf_nominal_tips",
            "cf_nominal_treasury",
            "cf_real_tips",
            "cf_real_treasury",
        ],
    )
    df.index.name = "Year"
    df["cf_nominal_tips"] = ncashFlows_tips
    df["cf_nominal_treasury"] = ncashFlows_treasury
    df["cf_real_tips"] = rcashFlows_tips
    df["cf_real_treasury"] = rcashFlows_treasury
    df["cf_nominal_tips"] = df.cf_nominal_tips.round(2)
    df["cf_real_treasury"] = df.cf_real_treasury.round(2)
    df = df.reset_index()

    trace1 = go.Bar(
        x=df["Year"], y=df["cf_nominal_tips"], name="TIPS", hovertemplate="%{y}"
    )
    trace2 = go.Bar(
        x=df["Year"],
        y=df["cf_nominal_treasury"],
        name="Regular Treasury",
        hovertemplate="%{y}",
    )
    trace_n = [trace1, trace2]
    fig1 = go.Figure(data=trace_n)
    fig1.update_layout(xaxis_title="Year")
    fig1.update_layout(xaxis=dict(dtick=1))
    fig1.update_layout(yaxis_title="Nominal Cash Flows")
    fig1.update_layout(title_text="Nominal Cash Flows", title_x=0.5)
    fig1.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig1.update_yaxes(type="log")
    trace3 = go.Bar(
        x=df["Year"], y=df["cf_real_tips"], name="TIPS", hovertemplate="%{y}"
    )
    trace4 = go.Bar(
        x=df["Year"],
        y=df["cf_real_treasury"],
        name="Regular Treasury",
        hovertemplate="%{y}",
    )
    trace_r = [trace3, trace4]
    fig2 = go.Figure(data=trace_r)
    fig2.update_layout(xaxis_title="Year")
    fig2.update_layout(xaxis=dict(dtick=1))
    fig2.update_layout(yaxis_title="Real Cash Flows")
    fig2.update_layout(title_text="Real Cash Flows", title_x=0.5)
    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig2.update_yaxes(type="log")
    return largefig(fig1, showlegend=True), largefig(fig2, showlegend=True)
