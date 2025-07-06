import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import largefig, blue, red, green

def figtbl(n_clicks, alpha, beta, gamma):

    alpha = alpha / 100

    # convert to monthly
    alpha = alpha / 12
    MN_MKTRF = 0.05/12              # market expected rturn
    SD_MKTRF = 0.20/np.sqrt(12)     # market return standard deviation
    SD_EPS   = 0.05/np.sqrt(12)     # standard deviation of fund's residual return
    NOBS  = 120                     # number of monthly observations to simulate

    # Simulate returns with market-timing ability
    df = pd.DataFrame(dtype=float, columns = ['xret', 'mkt', 'eps'])
    df['mkt']  = norm.rvs(loc=MN_MKTRF, scale=SD_MKTRF, size=NOBS)
    df['eps']  = norm.rvs(loc=0, scale=SD_EPS, size=NOBS)
    df['mkt_plus'] = np.where(df['mkt']>0, df['mkt'],0)
    df['xret'] = alpha + beta*df['mkt'] + gamma*df['mkt_plus'] + df['eps']

    # Run market model
    mm = sm.OLS(df['xret'], sm.add_constant(df['mkt'])).fit()
    a_mm = mm.params['const']
    b_mm = mm.params['mkt'] 

    # Run Henriksson/Merton model
    hm = sm.OLS(df['xret'], sm.add_constant(df[['mkt','mkt_plus']])).fit()
    a_hm = hm.params['const']
    b_hm = hm.params['mkt'] 
    g_hm = hm.params['mkt_plus'] 

    # Figure
    fig = go.Figure()

    # Simulated data
    trace  = go.Scatter(
        x=df['mkt'], 
        y=df['xret'], 
        mode="markers", 
        hovertemplate="Fund return:    %{y:.1%}<br>Market return: %{x:.1%}<extra></extra>",
        name = 'Returns')
    fig.add_trace(trace)

    # Market model
    grid = np.linspace(df.mkt.min(), df.mkt.max(),100)
    string = f'Market model: {a_mm:.3f} + {b_mm:.2f}*market<extra></extra>'
    fit_mm = np.array([a_mm + b_mm*x for x in grid])
    trace_mm= go.Scatter(
        x=grid, 
        y=fit_mm, 
        mode='lines',
        hovertemplate=string,
        name='Market Model')
    fig.add_trace(trace_mm)

    # Market-timing model
    string = f'Market-timing model: {a_hm:.3f} + {b_hm:.2f}*market + {g_hm:.2f}*max(market,0)<extra></extra>'
    fit_hm = np.array([a_hm + b_hm*x + g_hm*max(x,0) for x in grid])
    trace_timing= go.Scatter(
        x=grid, 
        y=fit_hm, 
        mode='lines',
        hovertemplate=string ,    
        name='Market-Timing Model')
    fig.add_trace(trace_timing)

    # Formatting
    fig.update_layout(
        xaxis_title='Market Excess Return',
        xaxis_tickformat=".1%",
        yaxis_title='Fund Excess Return',
        yaxis_tickformat=".1%",
        legend=dict(
            yanchor="top", 
            y=0.99, 
            xanchor="left", 
            x=0.01)
    )

    return (
        largefig(fig, showlegend=True),
        f'{a_mm*12:.1%}',
        f'{b_mm:.2f}',
        f'{a_hm*12:.1%}',
        f'{b_hm:.2f}',
        f'{g_hm:.2f}'
    )