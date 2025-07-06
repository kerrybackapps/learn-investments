# -*- coding: utf-8 -*-
"""
Created on Tue May 10 09:31:31 2022

@author: Kevin
"""

import pandas as pd
import numpy as np
import plotly.express as px
from pages.formatting import largefig


# def post_tax_return(tax_treat, t_oi_0, t_cg_0, t_oi_T, t_cg_T, r, T):
def post_tax_return(tax_treat, t_oi_0, t_oi_T, r, T):
    # tax_treat: "No tax advantage", "Nondeductible IRA", "Roth IRA/529 Plan", "Deductible IRA/401(k)/403(b)"
    # tax_treat: ['no_advantage', 'nondeductible_ira','roth','401k']
    # Assumes taxes are constant from t=0 to t=T-1 and then jump at t=T
    # Assumes constant rate of return
    t_oi_0 = t_oi_0 / 100
    # t_cg_0 = t_cg_0 / 100
    t_oi_T = t_oi_T / 100
    # t_cg_T = t_cg_T / 100
    r = r / 100
    if tax_treat == "no_advantage":
        ret = (1 + r * (1 - t_oi_0)) ** (T - 1) * (1 + r * (1 - t_oi_T))
    elif tax_treat == "nondeductible_ira":
        ret = (1 - t_oi_T) * (1 + r) ** T + t_oi_T
    elif tax_treat == "roth":
        ret = (1 + r) ** T
    elif tax_treat == "401k":
        if T == 0:
            ret = ((1 - t_oi_0) * (1 + r) ** T) / (1 - t_oi_0)
        else:
            ret = ((1 - t_oi_T) * (1 + r) ** T) / (1 - t_oi_0)
    else:
        print("Tax treatment not defined")
    return ret


# def figtbl(t_oi_0, t_cg_0, t_oi_T, t_cg_T, r, T):
def figtbl(t_oi_0, t_oi_T, r, T):    
    cols = ["no_advantage", "nondeductible_ira", "roth", "401k"]
    cols = ["401k", "roth", "nondeductible_ira", "no_advantage"]
    df = pd.DataFrame(dtype=float, index=np.arange(T + 1), columns=cols)
    for t in np.arange(T + 1):
        for c in cols:
            # df.loc[t, c] = post_tax_return(c, t_oi_0, t_cg_0, t_oi_T, t_cg_T, r, t)
            df.loc[t, c] = post_tax_return(c, t_oi_0, t_oi_T, r, t)            
    df.columns = ["401k", "Roth", "Non-Deductible IRA", "No Advantage"]
    df = df.stack().reset_index()
    df.columns = ["Year", "Vehicle", "Withdrawal"]
    fig = px.line(
        df, x="Year", y="Withdrawal", color="Vehicle", custom_data=["Vehicle"]
    )
    fig.layout.xaxis["title"] = "Year of Withdrawal"
    fig.update_yaxes(
        title="After-Tax FV of $1 of After-tax Initial Investment", tickformat="$,.0f"
    )
    string = "%{customdata}<br>$%{y:,.2f}<extra></extra>"
    fig.update_traces(hovertemplate=string)
    fig.update_layout(hovermode="x unified")

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, title=""))
    return largefig(fig, showlegend=True)
