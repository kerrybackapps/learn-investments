import pandas as pd
from scipy.stats import norm
import numpy as np
import plotly.graph_objects as go
from pandas_datareader import DataReader as pdr
from pages.formatting import smallfig, blue, red, green
from pages.data.ff_monthly import ff3 as ff

T = 100          #number of years of monthly data

ff = pdr('F-F_Research_Data_Factors', 'famafrench', start=1900)[0] / 100
mkt = ff["Mkt-RF"]
mkt.index = mkt.index.to_timestamp()

def figtbl(mn, sd, numyears):
    '''
    mn = annual market risk premium 
    sd = annual standard deviation of excess market returns
    numyears  = number of years of used to estimate empirical market risk premium
    '''
    
    ##### Analytical uncertainty  
    mn = (mn/100)/12
    sd = (sd/100)/np.sqrt(12)

    # 90% confidence interval
    df = pd.DataFrame(dtype='float', columns=['Average','5th','95th'], index=np.arange(5*12,T*12))
    df['Average'] = mn
    df['5th']  = mn - norm.ppf(0.95)*sd/np.sqrt(df.index)
    df['95th'] = mn + norm.ppf(0.95)*sd/np.sqrt(df.index)
    df = df*12
    df['Years'] = df.index/12
    
    # Plot confidence interval
    trace3 = go.Scatter(
        x=df["Years"],
        y=df["5th"],
        mode="lines",
        line=dict(color=red, dash="dash"),
        name="5th percentile",
        hovertemplate="5th percentile = %{y:.1%}<extra></extra>"
     )
    trace2 = go.Scatter(
        x=df["Years"],
        y=df["Average"],
        mode="lines",
        line=dict(color=blue),
        name="mean",
        hovertemplate="mean = %{y:.1%}<extra></extra>"
    )
    trace1 = go.Scatter(
        x=df["Years"],
        y=df["95th"],
        mode="lines",
        line=dict(color=green, dash="dash"),
        name="95th percentile",
        hovertemplate="95th percentile = %{y:.1%}<extra></extra>"
    )
    fig1 = go.Figure()
    for trace in [trace1, trace2, trace3]:
        fig1.add_trace(trace)
    fig1.update_layout(
        yaxis_title='Market Risk Premium',
        xaxis_title='Years in Estimation Window',
        title='Hypothetical Expanding Window Estimate',
        hovermode="x unified",
        yaxis_tickformat=".0%",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, title="")
    )

    
   
    ##### Empirical estimates

    window = numyears*12

    rolling_mean = mkt.rolling(window).mean().dropna()
    rolling_se   = mkt.rolling(window).std().dropna()/np.sqrt(window)


    p5  = rolling_mean - rolling_se*norm.ppf(0.95) 
    p95 = rolling_mean + rolling_se*norm.ppf(0.95) 

    # Annualize
    rolling_mean = 12*rolling_mean
    p5  = 12*p5
    p95 = 12*p95

    trace3 = go.Scatter(
        x=p5.index.to_list(),
        y=p5,
        mode="lines",
        line=dict(color=red, dash="dash"),
        name="5th percentile",
        hovertemplate="5th percentile = %{y:.1%}<extra></extra>"
    )
    trace2 = go.Scatter(
        x=rolling_mean.index.to_list(),
        y=rolling_mean,
        mode="lines",
        line=dict(color=blue),
        name="mean",
        hovertemplate="mean = %{y:.1%}<extra></extra>"
    )
    trace1 = go.Scatter(
        x=p95.index.to_list(),
        y=p95,
        mode="lines",
        line=dict(color=green, dash="dash"),
        name="95th percentile",
        hovertemplate="95th percentile = %{y:.1%}<extra></extra>"
    )
    fig2 = go.Figure()
    for trace in [trace1, trace2, trace3]:
        fig2.add_trace(trace)
    fig2.update_layout(
        yaxis_title='Market Risk Premium',
        xaxis_title='Year',
        title='Empirical Rolling Window Estimate',
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, title="")
    )
    fig2.update_yaxes(range=[-.20, .30])
    fig2.update_yaxes(tickformat=".0%")
    
    return smallfig(fig1, showlegend=True), smallfig(fig2, showlegend=True)