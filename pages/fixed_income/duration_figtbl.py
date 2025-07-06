import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go


def figtbl(maturity, coupon_rate, yld):
    # coupon_rate is in pct, price is $ per 100 face
    n = int(maturity * 2)
    coupon = coupon_rate / 2  # coupon in $
    cashFlows = [coupon] * n
    cashFlows[-1] += 100
    yld /= 100

    df = pd.DataFrame(
        dtype=float,
        index=np.arange(0.5, (n + 1) / 2, 0.5),
        columns=["cf", "factor", "pv", "pct", "year_pct"],
    )
    df.index.name = "Year"
    df["cf"] = cashFlows
    df["factor"] = 1 / (1 + yld / 2) ** np.arange(1, n + 1)
    df["pv"] = df.cf * df.factor
    df["pct"] = df.pv / (df["pv"].sum())
    df["year_pct"] = np.arange(0.5, (n + 1) / 2, 0.5) * df.pct
    macaulay = df.year_pct.sum(axis=0)
    modified = macaulay / (1 + yld / 2)
    string1 = f"{macaulay:.3f}"
    string2 = f"{modified:.3f}"

    df["cf"] = df.cf.round(2)
    df["factor"] = df.factor.apply(lambda x: "{:.1%}".format(x))
    df["pct"] = df.pct.apply(lambda x: "{:.2%}".format(x))
    df["pv"] = df.pv.round(2)
    df["year_pct"] = df.year_pct.round(3)
    df = df.reset_index()
    df.columns = [
        "Year",
        "Cash Flow",
        "PV Factor @ Yield",
        "PV of Cash Flow",
        "Percent of Total",
        "Year x Percent",
    ]

    return df, string1, string2
