import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.formatting import largefig, red, green, orange

# # Parameters
# raver1 = 2
# raver2 = 2
# raver3 = 2
# u1 = 0.05
# u2 = 0.075
# u3 = 0.10

def figtbl(raver1, raver2, raver3, u1, u2, u3):
    u1 = u1/100
    u2 = u2/100
    u3 = u3/100
    
    
    # Generate data
    sd = np.arange(0,0.405,0.005)
    mu1 = u1 + 0.5*raver1* (sd**2)
    mu2 = u2 + 0.5*raver2* (sd**2) 
    mu3 = u3 + 0.5*raver3* (sd**2)
    df = pd.DataFrame(data={'Standard Deviation': sd, 'Indifference 1': mu1, 'Indifference 2': mu2,'Indifference 3': mu3})
    df['Utility Level 1']=u1
    df['Utility Level 2']=u2
    df['Utility Level 3']=u3
    df = df*100
    df['Risk Aversion 1']=raver1
    df['Risk Aversion 2']=raver2
    df['Risk Aversion 3']=raver3
    
    # Plot data
    trace1 = go.Scatter(
        x=df["Standard Deviation"],
        y=df["Indifference 1"],
        mode="lines",
        line={'color': red},
        text=df["Utility Level 1"],
        customdata=df["Risk Aversion 1"],
        hovertemplate="Utility: %{text:.0f}% <br> Risk Aversion: %{customdata:.0f}<extra></extra>",
        name="Utility 1"
    )
    trace2 = go.Scatter(
        x=df["Standard Deviation"],
        y=df["Indifference 2"],
        mode="lines",
        line={'color': orange},
        text=df["Utility Level 2"],
        customdata=df["Risk Aversion 2"],
        hovertemplate="Utility: %{text:.0f}% <br> Risk Aversion: %{customdata:.0f}<extra></extra>",
        name="Utility 2"
    )
    trace3 = go.Scatter(
        x=df["Standard Deviation"],
        y=df["Indifference 3"],
        mode="lines",
        line={'color': green},
        text=df["Utility Level 3"],
        customdata=df["Risk Aversion 3"],
        hovertemplate="Utility: %{text:.0f}% <br> Risk Aversion: %{customdata:.0f}<extra></extra>",
        name="Utility 3"
    )

    fig = go.Figure()
    fig.add_trace(trace3)
    fig.add_trace(trace2)
    fig.add_trace(trace1)
    fig.update_yaxes(tickformat=".0f", ticksuffix="%")
    fig.update_xaxes(tickformat=".0f", ticksuffix="%")
    fig.update_layout(
        xaxis_title="Standard Deviation",
        yaxis_title="Expected Return",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    return largefig(fig, showlegend=True), go.Figure()
