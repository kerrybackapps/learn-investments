# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:33:32 2022

@author: kerry
"""

import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px
from pages.formatting import largefig
from scipy.optimize import fsolve


########################################
#
# WORK WITH MONTHLY DECIMAL r AND g
#
########################################

def growthFactors(g, M) :
    return (1+g)**np.arange(M)

def savingsFactors(r, g, M):
    return growthFactors(g,M) * (1+r)**np.arange(-1, -M-1, -1)

def withdrawalFactors(r, M, N):
    return (1+r)**np.arange(-M, -N, -1)

def fB0(r, g, M, N, S1, W):
    return W*np.sum(withdrawalFactors(r, M, N)) - S1*np.sum(savingsFactors(r, g, M))

def fS1(r, g, M, N, B0, W):
    return (W*np.sum(withdrawalFactors(r, M, N)) - B0) / np.sum(savingsFactors(r, g, M))

def fW(r, g, M, N, B0, S1):
    return (B0 + S1*np.sum(savingsFactors(r, g, M))) / np.sum(withdrawalFactors(r, M, N))

def fr(g, M, N, B0, S1, W):
    def npv(r):
        return B0 + S1*np.sum(savingsFactors(r,g,M)) - W*np.sum(withdrawalFactors(r,M,N))
    return fsolve(npv, x0=0.005).item()

def fg(r, M, N, B0, S1, W):
    def npv(g):
        return B0 + S1*np.sum(savingsFactors(r,g,M)) - W*np.sum(withdrawalFactors(r,M,N))
    return fsolve(npv, x0=0.002).item()

def solve(r, g, M, N, B0, S1, W, selection):
    if selection=='r':
        r = fr(g, M, N, B0, S1, W)
    elif selection=='g':
        g = fg(r, M, N, B0, S1, W)
    elif selection=='B0':
        B0 = fB0(r, g, M, N, S1, W)
    elif selection=='S1':
        S1 = fS1(r, g, M, N, B0, W)
    elif selection=='W':
        W = fW(r, g, M, N, B0, S1)
    return r, g, M, N, B0, S1, W

def history(r, g, M, N, B0, S1, W):
    S = S1 * (1 + g) ** np.arange(M)
    B = np.zeros(N + 1)
    B[0] = B0

    # saving period
    for i in range(1, M):
        B[i] = (1 + r) * B[i - 1] + S[i - 1]

    # date N: deposit and withdraw
    B[M] = (1 + r) * B[M - 1] + S[M - 1] - W

    # withdrawal period
    for i in range(M + 1, N):
        B[i] = (1 + r) * B[i - 1] - W

    # final period return
    B[N] = (1 + r) * B[N - 1]

    df = pd.DataFrame(B)
    df.columns = ["balance"]
    df.index.name = "year"
    df['deposit']=0
    df.loc[1:M,'deposit']=S   
    df['withdrawal'] = 0
    df.loc[M:,'withdrawal'] = -W
    df = df.reset_index()
    df["year"] = df.year / 12
    df = df[df.year % 1 == 0]        
    return df

keys = ['Initial balance', 'Initial monthly savings', 'Annual savings growth rate', 'Monthly withdrawal',
         'Annual rate of return']

values = ['B0', 'S1', 'g', 'W', 'r']

Dict = dict(zip(keys, values))

#################################################
#
# NOW INPUT ANNUAL PERCENTAGE r AND g
#
#################################################

def figtbl(B0, yearsS, yearsW, S1, ga, W, ra, selection):

    selection = Dict[selection]

    r = ra / (100*12)
    g = ga / (100*12)
    M = yearsS*12
    N = M + yearsW*12
    r, g, M, N, B0, S1, W = solve(r, g, M, N, B0, S1, W, selection)
    df = history(r, g, M, N, B0, S1, W)

    if selection=='r':
        ra = (1 + r) ** 12 - 1
        string1 = 'Required annual rate of return:'
        string2 = f'{ra:.2%}'
    elif selection=='g':
        ga = (1 + g) ** 12 - 1
        string1 = 'Required annual savings growth rate:'
        string2 = f'{ga:.2%}'
    elif selection=='B0':
        string1 = 'Required initial balance:'
        string2 = f'${B0:,.0f}'
    elif selection=='S1':
        string1 = 'Required initial monthly savings:'
        string2 = f'${S1:,.0f}'
    else:
        string1 = 'Maximum monthly withdrawal:'
        string2 = f'${W:,.0f}'


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

    return largefig(fig), string1, string2