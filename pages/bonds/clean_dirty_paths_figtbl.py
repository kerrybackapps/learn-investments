import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig, green, red, blue


class bond:
    def __init__(self, coupon_rate, coupons_remaining, days_to_next=180):
        self.coupon = 100 * coupon_rate / 2
        self.n = coupons_remaining
        # I changed self.days to be integer, or it won't work if we set coupons_remaining as 4.5/5.5/6.5...
        self.days = int((coupons_remaining - 1) * 180 + days_to_next)
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


def figtbl(coupon_rate, coupons_remaining, days_to_next_coupon, yld):
    coupon_rate = coupon_rate / 100
    yld = yld / 100
    b = bond(coupon_rate, coupons_remaining, days_to_next_coupon)

    # plot
    days = [i for i in range(b.days)]
    clean = [b.clean(d, yld) for d in days]
    dirty = [b.dirty(d, yld) for d in days]

    string1 = "clean price = %{y:.02f}<extra></extra>"
    string2 = "dirty price = %{y:.02f}<extra></extra>"
    trace1 = go.Scatter(
        x=days, y=clean, mode="lines", hovertemplate=string1, name="clean price"
    )
    trace2 = go.Scatter(
        x=days,
        y=dirty,
        mode="lines",
        hovertemplate=string2,
        name="dirty price",
        line=dict(color=blue),
    )
    trace3 = go.Scatter(
        x=days,
        y=[100] * len(days),
        hovertemplate="face value<extra></extra>",
        mode="lines",
        line=dict(color=red, dash="dot"),
        name="face value",
    )
    fig = go.Figure(trace3)
    fig.add_trace(trace2)
    fig.add_trace(trace1)
    fig.update_layout(xaxis_title="Days")
    fig.update_layout(yaxis_tickprefix="$")
    fig.update_layout(hovermode="x unified")
    fig.update_layout(legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99))

    return largefig(fig, showlegend=True)
