import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, red, green, orange, blue

def figtbl(raver1, raver2):

    traces = []
    x = np.linspace(0,0.2,50)
    for A, color in zip((raver1, raver2), (blue, red)):
        mn = 0.02
        trace = go.Scatter(
            x=x,
            y=mn + 0.5 * A * x ** 2,
            mode="lines",
            line=dict(color=color),
            hovertemplate=f"risk aversion = {A}<br>utility = {mn:.2f}<extra></extra>",
            name=f"risk aversion = {A}"
        )
        traces.append(trace)
        for mn in (0.04, 0.06):

            trace = go.Scatter(
                x=x,
                y=mn + 0.5*A*x**2,
                mode="lines",
                line=dict(color=color),
                hovertemplate=f"risk aversion = {A}<br>utility = {mn:.2f}<extra></extra>",
                showlegend=False
            )
            traces.append(trace)

    fig = go.Figure()
    for trace in traces:
        fig.add_trace(trace)


    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    fig.update_layout(
        xaxis_title="Standard Deviation",
        yaxis_title="Expected Return",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    return largefig(fig, showlegend=True)
