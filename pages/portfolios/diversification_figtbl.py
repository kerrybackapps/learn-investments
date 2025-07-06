import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pages.formatting import largefig


# Range of x-axis
Num = 200


def figtbl(std, cor):

    # The inputs are in percents
    std /= 100
    cor /= 100
    var = std ** 2
    cov = var * cor
    stdevs = [np.sqrt(var / n + (n - 1) * cov / n) for n in range(1, Num + 1)]
    df = pd.DataFrame(stdevs)
    df.columns = ["Standard Deviation"]
    df["Number of Assets"] = [i for i in range(1, Num + 1)]

    # Plotting
    trace1 = go.Scatter(
        x=df["Number of Assets"],
        y=df["Standard Deviation"],
        mode="lines",
        hovertemplate="Number of Assets = %{x}<br>Standard Deviation = %{y:0.2%} <extra></extra>",
    )

    fig = go.Figure()
    fig.add_trace(trace1)
    fig.update_yaxes(tickformat=",.0%", rangemode="tozero")
    fig.layout.xaxis["title"] = "Number of Assets"
    fig.layout.yaxis["title"] = "Standard Deviation"
    return largefig(fig)
