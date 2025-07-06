import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pages.formatting import largefig



# Dividend-paying stock
def stockret(tax_treat, t_oi_0, t_oi_T, t_div, t_cg, dy, cg, T):
    # tax_treat: ['brokerage','roth','401k']
    # Assumes taxes are constant from t=0 to t=T-1 and then jump at t=T
    # Assumes constant dividend yield and capital gain per year
    if tax_treat == "Brokerage":
        r = 1 + dy * (1 - t_div) + cg
        ret = (r ** T) * (1 - t_cg) + t_cg * (
            1 + dy * (1 - t_div) * (1 - r ** T) / (1 - r)
        )
    elif tax_treat == "Roth":
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
def bondret(tax_treat, t_oi_0, t_oi_T, r, T):
    # tax_treat: ['brokerage','roth','401k']
    # Assumes taxes are constant from t=0 to t=T-1 and then jump at t=T
    # Assumes taxable coupon payment (reinvested at same rate); no capital gain/loss on bond
    if tax_treat == "Brokerage":
        if T == 0:
            ret = 1
        else:
            ret = (1 + r * (1 - t_oi_0)) ** (T - 1) * (1 + r * (1 - t_oi_T))
    elif tax_treat == "Roth":
        ret = (1 + r) ** T
    elif tax_treat == "401k":
        if T == 0:
            ret = ((1 - t_oi_0) * (1 + r) ** T) / (1 - t_oi_0)  # (ie. 1)
        else:
            ret = ((1 - t_oi_T) * (1 + r) ** T) / (1 - t_oi_0)
    else:
        print("Tax treatment not defined")
    return ret

# # Dividend-paying stock
# def post_tax_return_divstock(tax_treat, t_oi_0, t_oi_T, t_div, t_cg, dy, cg, T):
#     # tax_treat: ['brokerage','roth','401k']
#     # Assumes taxes are constant from t=0 to t=T-1 and then jump at t=T
#     # Assumes constant dividend yield and capital gain per year
#     if tax_treat == "brokerage":
#         r = 1 + dy * (1 - t_div) + cg
#         ret = (r ** T) * (1 - t_cg) + t_cg * (
#             1 + dy * (1 - t_div) * (1 - r ** T) / (1 - r)
#         )
#     elif tax_treat == "roth":
#         r = dy + cg
#         ret = (1 + r) ** T
#     elif tax_treat == "401k":
#         r = dy + cg
#         if T == 0:
#             ret = ((1 - t_oi_0) * (1 + r) ** T) / (1 - t_oi_0)
#         else:
#             ret = ((1 - t_oi_T) * (1 + r) ** T) / (1 - t_oi_0)
#     else:
#         print("Tax treatment not defined")
#     return ret


# # Taxable coupon bond (with reinvestment)
# def post_tax_return_taxbond(tax_treat, t_oi_0, t_oi_T, t_cg, r, T):
#     # tax_treat: ['brokerage','roth','401k']
#     # Assumes taxes are constant from t=0 to t=T-1 and then jump at t=T
#     # Assumes taxable coupon payment (reinvested at same rate); no capital gain/loss on bond
#     if tax_treat == "brokerage":
#         if T == 0:
#             ret = 1
#         else:
#             ret = (1 + r * (1 - t_oi_0)) ** (T - 1) * (1 + r * (1 - t_oi_T))
#     elif tax_treat == "roth":
#         ret = (1 + r) ** T
#     elif tax_treat == "401k":
#         if T == 0:
#             ret = ((1 - t_oi_0) * (1 + r) ** T) / (1 - t_oi_0)  # (ie. 1)
#         else:
#             ret = ((1 - t_oi_T) * (1 + r) ** T) / (1 - t_oi_0)
#     else:
#         print("Tax treatment not defined")
#     return ret


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
    frac_brok_stock,
    frac_brok_bond,
    frac_401k_stock,
    frac_401k_bond,
    frac_roth_stock,
):
    dy = dy / 100
    cg = cg / 100
    bond_rate = bond_rate / 100
    t_oi_0 = t_oi_0 / 100
    t_oi_T = t_oi_T / 100
    t_div = t_div / 100
    t_cg = t_cg / 100
    frac_brok_stock = frac_brok_stock / 100
    frac_brok_bond = frac_brok_bond / 100
    frac_401k_stock = frac_401k_stock / 100
    frac_401k_bond = frac_401k_bond / 100
    frac_roth_stock = frac_roth_stock / 100
    # Note: omitted weight is frac_roth_bond
    frac_roth_bond = (
        1
        - frac_brok_stock
        - frac_brok_bond
        - frac_401k_stock
        - frac_401k_bond
        - frac_roth_stock
    )


    portfolio = {
            "Brokerage:Stock":  frac_brok_stock,
            "Brokerage:Bond":   frac_brok_bond,
            "401k:Stock":       frac_401k_stock,
            "401k:Bond":        frac_401k_bond,
            "Roth:Stock":       frac_roth_stock,
            "Roth:Bond":        frac_roth_bond
    }
    # Calculate future values in each account
    accounts = ['Brokerage','401k', 'Roth']
    subaccts = ['Stock','Bond','Total']
    cols = pd.MultiIndex.from_product([accounts,subaccts])
    df = pd.DataFrame(dtype=float, index=1+np.arange(tot_years), columns=cols)
    for t in df.index:
        for acct in accounts:
            wgt = portfolio[acct + ":Stock"]
            df.loc[t, (acct,'Stock')] = wgt * stockret(acct, t_oi_0, t_oi_T, t_div, t_cg, dy, cg, t)

            wgt = portfolio[acct + ":Bond"]
            df.loc[t, (acct,'Bond')]  = wgt * bondret(acct, t_oi_0, t_oi_T, bond_rate, t)

    for acct in accounts:
        df[(acct,'Total')] = df[(acct,'Stock')] + df[(acct,'Bond')]
    cols_to_sum = [(acct, 'Total') for acct in accounts] 
    df[("Overall",'Total')] = df[cols_to_sum].sum(axis=1)     


    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[('Overall','Total')], mode="lines", name="Total"))
    fig.add_trace(go.Scatter(x=df.index, y=df[('Brokerage','Total')], mode="lines", name="Brokerage"))
    fig.add_trace(go.Scatter(x=df.index, y=df[('401k','Total')], mode="lines", name="401k"))
    fig.add_trace(go.Scatter(x=df.index, y=df[('Roth','Total')], mode="lines", name="Roth"))
    fig.update_xaxes(title="Year of Withdrawal", tickformat=",.0f")
    fig.update_yaxes(title="After-Tax FV", tickformat="$,.2f")
    fig.update_layout(hovermode="x unified")   

    # cols = [
    #     "brok_stock",
    #     "brok_bond",
    #     "brok_total",
    #     "401k_stock",
    #     "401k_bond",
    #     "401k_total",
    #     "roth_stock",
    #     "roth_bond",
    #     "roth_total",
    #     "total",
    # ]
    # df = pd.DataFrame(dtype=float, index=np.arange(tot_years + 1), columns=cols)

    # for t in np.arange(tot_years + 1):
    #     df.loc[t, "brok_stock"] = frac_brok_stock * post_tax_return_divstock(
    #         "brokerage", t_oi_0, t_oi_T, t_div, t_cg, dy, cg, t
    #     )
    #     df.loc[t, "401k_stock"] = frac_401k_stock * post_tax_return_divstock(
    #         "401k", t_oi_0, t_oi_T, t_div, t_cg, dy, cg, t
    #     )
    #     df.loc[t, "roth_stock"] = frac_roth_stock * post_tax_return_divstock(
    #         "roth", t_oi_0, t_oi_T, t_div, t_cg, dy, cg, t
    #     )

    #     df.loc[t, "brok_bond"] = frac_brok_bond * post_tax_return_taxbond(
    #         "brokerage", t_oi_0, t_oi_T, t_cg, bond_rate, t
    #     )
    #     df.loc[t, "401k_bond"] = frac_401k_bond * post_tax_return_taxbond(
    #         "401k", t_oi_0, t_oi_T, t_cg, bond_rate, t
    #     )
    #     df.loc[t, "roth_bond"] = frac_roth_bond * post_tax_return_taxbond(
    #         "roth", t_oi_0, t_oi_T, t_cg, bond_rate, t
    #     )

    # df["brok_total"] = df.brok_stock + df.brok_bond
    # df["401k_total"] = df["401k_stock"] + df["401k_bond"]
    # df["roth_total"] = df.roth_stock + df.roth_bond
    # df["total"] = df.brok_total + df["401k_total"] + df.roth_total

    # # return df

    # cols = [
    #     "Brokerage:Stock",
    #     "Brokerage:Bond",
    #     "Brokerage:Total",
    #     "401k:Stock",
    #     "401k:Bond",
    #     "401k:Total",
    #     "Roth:Stock",
    #     "Roth:Bond",
    #     "Roth:Total",
    #     "Total",
    # ]
    # df.columns = cols

    # # Plot a single set of weights and the values in each part of the account
    # df = df.stack().reset_index()
    # df.columns = ["Year", "Allocation", "Withdrawal"]

    # fig = px.line(
    #     df, x="Year", y="Withdrawal", color="Allocation", custom_data=["Allocation"]
    # )
    # fig.layout.xaxis["title"] = "Year of Withdrawal"
    # fig.update_yaxes(title="After-Tax FV", tickformat="$,.0f")
    # string = "%{customdata}<br>$%{y:,.2f}<extra></extra>"
    # fig.update_traces(hovertemplate=string)
    # fig.update_layout(hovermode="x unified")

    # # fig.update_layout(legend=dict(
    # #     yanchor="top",
    # #     y=0.99,
    # #     xanchor="left",
    # #     x=0.01
    # # ))
    return largefig(fig, showlegend=True)
