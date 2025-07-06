# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:33:32 2022

@author: kerry
"""

import pandas as pd
import numpy as np
import plotly.express as px
from pages.formatting import largefig


def data(
    initial_balance,
    years_saving,
    years_withdrawing,
    initial_deposit,
    deposit_growth_rate,
    withdrawals,
    rate_of_return,
):

    B0 = initial_balance
    N = years_saving
    M = N + years_withdrawing
    S0 = initial_deposit
    g = deposit_growth_rate / 100
    r = rate_of_return / 100
    W = withdrawals

    S = S0 * (1 + g) ** np.arange(N)
    B = np.zeros(M + 1)
    B[0] = B0

    # saving period
    for i in range(1, N+1):
        B[i] = (1 + r) * B[i - 1] + S[i - 1]

    # withdrawal period
    for i in range(N + 1, M+1):
        B[i] = (1 + r) * B[i - 1] - W

    df = pd.DataFrame(B)
    df.columns = ["balance"]
    df.index.name = "year"
    df['deposit']=0
    df.loc[1:N,'deposit']=S   
    df['withdrawal'] = 0
    df.loc[N+1:,'withdrawal'] = -W
    df = df.reset_index()
    # df["year"] = df.year / 12
    # df = df[df.year % 1 == 0]
    return df


def figtbl(
    initial_balance,
    years_saving,
    years_withdrawing,
    initial_deposit,
    deposit_growth_rate,
    withdrawals,
    rate_of_return,
):
    df = data(
        initial_balance,
        years_saving,
        years_withdrawing,
        initial_deposit,
        deposit_growth_rate,
        withdrawals,
        rate_of_return,
    )
    string = "at year %{x:.0f}:<br> balance = $%{y:,.0f} <br> deposit = $%{customdata[0]:,.0f} <br> withdrawal = $%{customdata[1]:,.0f} <extra></extra> "
    fig = px.line(data_frame=df,
                     x='year',
                     y='balance',
                     custom_data=['deposit','withdrawal']
                    )
    fig.update_traces(hovertemplate=string)
    fig.layout.xaxis["title"] = "Year"
    fig.layout.yaxis["title"] = "Account Balance"
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")

    string = f"${df.balance.iloc[-1]:,.0f}"

    return largefig(fig), string

nothing = 0