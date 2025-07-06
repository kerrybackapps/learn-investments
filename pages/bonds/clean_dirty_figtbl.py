import numpy as np
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go
from scipy.optimize import fsolve
from pages.formatting import largefig, plotly_template, red, blue


class bond:
    def __init__(self, coupon_rate, coupons_remaining, days_to_next=180):
        self.coupon = 100 * coupon_rate / 2
        self.n = coupons_remaining
        self.days = (coupons_remaining - 1) * 180 + days_to_next
        self.days_to_next = days_to_next

    def days_remaining(self, day):
        return self.days - day

    def coupons_remaining(self, day):
        return int(np.ceil((self.days_remaining(day)) / 180))

    def fp(self, day):
        x = 180 - self.days_remaining(day) % 180
        return x / 180 if x < 180 else 0

    def accrued(self, day):
        return self.coupon * self.fp(day)

    def dirty(self, day, yld):
        periods = 1 - self.fp(day) + np.arange(self.coupons_remaining(day))
        pvFactors = 1 / (1 + yld / 2) ** periods
        cashFlows = [self.coupon] * (self.coupons_remaining(day) - 1) + [
            100 + self.coupon
        ]
        return np.sum(pvFactors * cashFlows)

    def clean(self, day, yld):
        return self.dirty(day, yld) - self.accrued(day)


def figtbl(coupon_rate, coupons_remaining, days_to_next_coupon, clean_price):
    coupon_rate = coupon_rate / 100
    b = bond(coupon_rate, coupons_remaining, days_to_next_coupon)

    # compute yield
    coupon = coupon_rate * 100 / 2
    partial_period = days_to_next_coupon / 180
    accrued = (1 - partial_period) * coupon
    dirty_price = clean_price + accrued
    cashFlows = [coupon] * (coupons_remaining - 1) + [100 + coupon]

    def pvFactors(y):
        return 1 / (1 + y / 2) ** np.arange(
            partial_period, partial_period + coupons_remaining
        )

    def f(y):
        return dirty_price - np.sum(cashFlows * pvFactors(y))

    yld = fsolve(f, x0=coupon_rate).item()
    yld_str = "{:.2%}".format(yld)
    # c_price = "{:.2f}".format(clean_price)
    dirty_price = "{:.2f}".format(dirty_price)

    # plot
    ylds = np.arange(0, 2 * coupon_rate + 0.001, 0.001)
    prices = [b.clean(0, y) for y in ylds]
    trace1 = go.Scatter(
        x=ylds,
        y=[clean_price] * len(prices),
        mode="lines",
        line=dict(dash="dot", color=red),
        hovertemplate="clean price<extra></extra>",
    )
    string = "clean price = $%{y:.2f} when yield = %{x:,.2%}<extra></extra>"
    trace2 = go.Scatter(
        x=ylds, y=prices, mode="lines", hovertemplate=string, line=dict(color=blue)
    )
    string = "clean price = $%{y:.2f} when yield = %{x:,.2%}<extra></extra>"
    trace0 = go.Scatter(
        x=[yld],
        y=[clean_price],
        mode="markers",
        hovertemplate=string,
        marker=dict(size=15, color=red),
    )
    fig = go.Figure(trace2)
    # fig.add_trace(trace2)
    # fig.add_trace(trace0)
    fig.layout.yaxis["title"] = "Clean Price"
    fig.layout.xaxis["title"] = "Yield"
    fig.update_layout(xaxis_tickformat=".0%")
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")

    # table
    df = pd.DataFrame(
        dtype=float, index=range(1, b.n + 1), columns=["cf", "factor", "pv"]
    )
    df.index.name = "time"
    df["cf"] = cashFlows
    df["factor"] = 1 / (1 + yld / 2) ** np.arange(1, b.n + 1)
    df["pv"] = df.cf * df.factor
    df["factor"] = df.factor.round(3)
    df[["cf", "pv"]] = df[["cf", "pv"]].round(2)
    df = df.reset_index()
    df.columns = ["Time", "Cash Flow", "PV Factor @ Yield", "PV of Cash Flow"]

    return df, yld_str, dirty_price, largefig(fig)
