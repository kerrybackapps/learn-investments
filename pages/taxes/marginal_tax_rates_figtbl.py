import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, blue, red, green

# 2023 information
BRACKETS = {
    'single':                   [0, 11000, 44725,  95375, 182100, 231250, 578125],
    'married filing jointly':   [0, 22000, 89450, 190750, 364200, 462500, 693750],
    'married filing separately':[0, 11000, 44725,  95375, 182100, 231250, 346875],
    'head of household':        [0, 15700, 59850,  95350, 182100, 231250, 578100]
}
RATES  = [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]   


# total tax due
def tax(income, status):
    LIMITS = BRACKETS[status]
    tax = 0
    for i, limit in enumerate(LIMITS):
        if i < len(LIMITS)-1:
            upper = LIMITS[i+1]
        else:
            upper = np.inf
        if income >= limit:
            tax +=  RATES[i] * max(0, min(income-limit, upper - limit))
    return tax


# Effective and marginal rates
# def marginal(income, status,BRACKETS,RATES):
def marginal(income, status):    
    LIMITS = BRACKETS[status]
    for i, limit in enumerate(LIMITS):
        if income >= limit:
            rate = RATES[i]
    return rate


def figtbl(income, status):
    income = float(income)

    # numeric outputs
    tax_due = tax(income,status) 
    t_marginal  = marginal(income, status)
    t_effective = tax_due / income

    # figure
    incomes = np.arange(1000,751000,1000)
    marginal_pcts  = [marginal(x,status) for x in incomes]
    effective_pcts = [tax(x,status)/x for x in incomes]


    # Scatter plot of average tax rate
    fig = go.Figure()
    trace  = go.Scatter(x=incomes, y=effective_pcts, mode="lines",name='Effective')
    fig.add_trace(trace)

    trace1  = go.Scatter(x=incomes, y=marginal_pcts, mode="lines", name='Marginal')
    fig.add_trace(trace1)

    # Formatting
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Taxable Income',
        xaxis_tickformat=",.0f",
        xaxis_tickprefix='$',
        yaxis_title='Tax Rate',
        yaxis_tickformat=".1%",
        title='Filing Status: ' + status.title(),
        legend=dict(
            yanchor="top", 
            y=0.99, 
            xanchor="left", 
            x=0.01)
    )
    return (
            largefig(fig, showlegend=True),
            f'${tax_due:,.2f}',
            f'{t_marginal:.1%}',
            f'{t_effective:.1%}',
        )    
