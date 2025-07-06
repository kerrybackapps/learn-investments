import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig, blue, red


def figtbl(maturity, coupon_rate, radio, price, yld):
    # coupon_rate is in pct, price is $ per 100 face
    yld /= 100
    n = maturity * 2
    coupon = coupon_rate / 2  # coupon in $
    if radio == "yld":
        cashFlows = [-price] + [coupon] * n
        cashFlows[-1] += 100
        yld = 2 * npf.irr(cashFlows)  # double the semi-annual yield
        string1 = f"{yld:.2%}"
        string2 = ""

    else:
        cashFlows = [0] + [coupon] * n
        cashFlows[-1] += 100
        price = np.sum(cashFlows * (1+yld/2)**np.arange(0, -n-1, -1))
        string1 = ""
        string2 = f"${price:.2f}"

    # now compute arrays of yields and prices
    grid = np.arange(0.01, 2 * yld + 0.01, 0.0001)
    prices = [np.sum(cashFlows[1:] / (1 + y / 2) ** np.arange(1, n + 1)) for y in grid]

    trace1 = go.Scatter(
        x=[0] + list(grid),
        y=[price] * (1 + len(grid)),
        mode="lines",
        line=dict(dash="dot", color=red),
        hovertemplate="price<extra></extra>",
    )

    string = "price = $%{y:.02f} when yield = %{x:,.2%}<extra></extra>"
    trace2 = go.Scatter(
        x=grid, y=prices, mode="lines", hovertemplate=string, line=dict(color=blue)
    )
    string = "price = $%{y:.02f} when yield = %{x:,.2%}<extra></extra>"
    trace0 = go.Scatter(
        x=[yld],
        y=[price],
        mode="markers",
        hovertemplate=string,
        marker=dict(size=15, color=red),
    )
    fig = go.Figure(trace1)
    fig.add_trace(trace2)
    fig.add_trace(trace0)
    fig.layout.xaxis["title"] = "Yield"
    fig.layout.yaxis["title"] = "Price"
    fig.update_layout(xaxis_tickformat=".0%")
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    fig.update_xaxes(rangemode="tozero")

    df = pd.DataFrame(
        dtype=float, index=range(1, n + 1), columns=["cf", "factor", "pv"]
    )
    df.index.name = "period"
    df["cf"] = cashFlows[1:]
    df["factor"] = 1 / (1 + yld / 2) ** np.arange(1, n + 1)
    df["pv"] = df.cf * df.factor
    df["factor"] = df.factor.round(3)
    df[["cf", "pv"]] = df[["cf", "pv"]].round(2)
    df = df.reset_index()
    df.columns = ["Period", "Cash Flow", "PV Factor @ Yield", "PV of Cash Flow"]
    return df, largefig(fig), string1, string2
