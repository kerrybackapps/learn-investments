import pandas as pd
import numpy as np
import plotly.express as px
from pages.formatting import largefig


# Dividend-paying stock
def post_tax_return_divstock(tax_treat, t_oi_0, t_oi_T, t_div, t_cg, dy, cg, T):
    # tax_treat: ['brokerage','roth','401k']
    # Assumes taxes are constant from t=0 to t=T-1 and then jump at t=T
    # Assumes constant dividend yield and capital gain per year
    if tax_treat == "brokerage":
        r = 1 + dy * (1 - t_div) + cg
        ret = (r ** T) * (1 - t_cg) + t_cg * (
            1 + dy * (1 - t_div) * (1 - r ** T) / (1 - r)
        )
    elif tax_treat == "roth":
        r = dy + cg
        ret = (1 + r) ** T
    elif tax_treat == "401k":
        r = dy + cg
        if T == 0:
            ret = ((1 - t_oi_0) * (1 + r) ** T) / (1 - t_oi_0)
        else:
            ret = ((1 - t_oi_T) * (1 + r) ** T) / (1 - t_oi_0)
    else:
        print("Tax treatment not defined")
    return ret


# Taxable coupon bond (with reinvestment)
def post_tax_return_taxbond(tax_treat, t_oi_0, t_oi_T, t_cg, r, T):
    # tax_treat: ['brokerage','roth','401k']
    # Assumes taxes are constant from t=0 to t=T-1 and then jump at t=T
    # Assumes taxable coupon payment (reinvested at same rate); no capital gain/loss on bond
    if tax_treat == "brokerage":
        if T == 0:
            ret = 1
        else:
            ret = (1 + r * (1 - t_oi_0)) ** (T - 1) * (1 + r * (1 - t_oi_T))
    elif tax_treat == "roth":
        ret = (1 + r) ** T
    elif tax_treat == "401k":
        if T == 0:
            ret = ((1 - t_oi_0) * (1 + r) ** T) / (1 - t_oi_0)  # (ie. 1)
        else:
            ret = ((1 - t_oi_T) * (1 + r) ** T) / (1 - t_oi_0)
    else:
        print("Tax treatment not defined")
    return ret


# Calculate each subaccount future value
def figtbl(
    dy,
    cg,
    bond_rate,
    t_oi_0,
    t_oi_T,
    t_div,
    t_cg,
    tot_years,
    frac_brok_stock1,
    frac_brok_bond1,
    frac_401k_stock1,
    frac_401k_bond1,
    frac_roth_stock1,
    frac_brok_stock2,
    frac_brok_bond2,
    frac_401k_stock2,
    frac_401k_bond2,
    frac_roth_stock2,
    frac_brok_stock3,
    frac_brok_bond3,
    frac_401k_stock3,
    frac_401k_bond3,
    frac_roth_stock3,
):
    dy = dy / 100
    cg = cg / 100
    bond_rate = bond_rate / 100
    t_oi_0 = t_oi_0 / 100
    t_oi_T = t_oi_T / 100
    t_div = t_div / 100
    t_cg = t_cg / 100
    frac_brok_stock1 = frac_brok_stock1 / 100
    frac_brok_bond1 = frac_brok_bond1 / 100
    frac_401k_stock1 = frac_401k_stock1 / 100
    frac_401k_bond1 = frac_401k_bond1 / 100
    frac_roth_stock1 = frac_roth_stock1 / 100

    frac_brok_stock2 = frac_brok_stock2 / 100
    frac_brok_bond2 = frac_brok_bond2 / 100
    frac_401k_stock2 = frac_401k_stock2 / 100
    frac_401k_bond2 = frac_401k_bond2 / 100
    frac_roth_stock2 = frac_roth_stock2 / 100

    frac_brok_stock3 = frac_brok_stock3 / 100
    frac_brok_bond3 = frac_brok_bond3 / 100
    frac_401k_stock3 = frac_401k_stock3 / 100
    frac_401k_bond3 = frac_401k_bond3 / 100
    frac_roth_stock3 = frac_roth_stock3 / 100

    wgts0 = [
        frac_brok_stock1,
        frac_brok_bond1,
        frac_401k_stock1,
        frac_401k_bond1,
        frac_roth_stock1,
    ]
    wgts1 = [
        frac_brok_stock2,
        frac_brok_bond2,
        frac_401k_stock2,
        frac_401k_bond2,
        frac_roth_stock2,
    ]
    wgts2 = [
        frac_brok_stock3,
        frac_brok_bond3,
        frac_401k_stock3,
        frac_401k_bond3,
        frac_roth_stock3,
    ]

    # If all sliders are at zero, ignore 2nd and 3rd allocations
    if np.sum(wgts2) > 0:
        allocations = [wgts0, wgts1, wgts2]
    else:
        if np.sum(wgts1) > 0:
            allocations = [wgts0, wgts1]
        else:
            allocations = [wgts0]

    numwgts = len(allocations)

    totcols = ["Portfolio " + str(x + 1) for x in np.arange(len(allocations))]
    totals = pd.DataFrame(dtype=float, index=np.arange(tot_years + 1), columns=totcols)

    for i, wgt in enumerate(allocations):
        (
            frac_brok_stock,
            frac_brok_bond,
            frac_401k_stock,
            frac_401k_bond,
            frac_roth_stock,
        ) = wgt

        # Note: omitted weight is frac_roth_bond
        frac_roth_bond = (
            1
            - frac_brok_stock
            - frac_brok_bond
            - frac_401k_stock
            - frac_401k_bond
            - frac_roth_stock
        )

        cols = [
            "brok_stock",
            "brok_bond",
            "brok_total",
            "401k_stock",
            "401k_bond",
            "401k_total",
            "roth_stock",
            "roth_bond",
            "roth_total",
            "total",
        ]
        df = pd.DataFrame(dtype=float, index=np.arange(tot_years + 1), columns=cols)

        for t in np.arange(tot_years + 1):
            df.loc[t, "brok_stock"] = frac_brok_stock * post_tax_return_divstock(
                "brokerage", t_oi_0, t_oi_T, t_div, t_cg, dy, cg, t
            )
            df.loc[t, "401k_stock"] = frac_401k_stock * post_tax_return_divstock(
                "401k", t_oi_0, t_oi_T, t_div, t_cg, dy, cg, t
            )
            df.loc[t, "roth_stock"] = frac_roth_stock * post_tax_return_divstock(
                "roth", t_oi_0, t_oi_T, t_div, t_cg, dy, cg, t
            )

            df.loc[t, "brok_bond"] = frac_brok_bond * post_tax_return_taxbond(
                "brokerage", t_oi_0, t_oi_T, t_cg, bond_rate, t
            )
            df.loc[t, "401k_bond"] = frac_401k_bond * post_tax_return_taxbond(
                "401k", t_oi_0, t_oi_T, t_cg, bond_rate, t
            )
            df.loc[t, "roth_bond"] = frac_roth_bond * post_tax_return_taxbond(
                "roth", t_oi_0, t_oi_T, t_cg, bond_rate, t
            )

        df["brok_total"] = df.brok_stock + df.brok_bond
        df["401k_total"] = df["401k_stock"] + df["401k_bond"]
        df["roth_total"] = df.roth_stock + df.roth_bond
        df["total"] = df.brok_total + df["401k_total"] + df.roth_total
        totals["Portfolio " + str(i + 1)] = df["total"]

    totals = totals.stack().reset_index()
    totals.columns = ["Year", "Portfolio", "Withdrawal"]

    fig = px.line(
        totals, x="Year", y="Withdrawal", color="Portfolio", custom_data=["Portfolio"]
    )
    fig.layout.xaxis["title"] = "Year of Withdrawal"
    fig.update_yaxes(title="After-Tax FV", tickformat="$,.0f")
    string = "%{customdata}<br>$%{y:,.2f}<extra></extra>"
    fig.update_traces(hovertemplate=string)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, title=""))
    return largefig(fig, showlegend=True)
