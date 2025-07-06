import pandas as pd
from pages.data.inflation import inflation
from pages.data.sbb import nominal
from pages.formatting import smallfig
import plotly.express as px


df = pd.concat((nominal, inflation), axis=1).dropna()
assets = ['S&P 500', 'Gold', 'Corporates', 'Treasuries', 'TBills']
df = df[assets + ['Inflation']]


def figtbl(name, dates):

    d1 = df.loc[dates[0]:dates[1]].copy()
    corrs = d1.corr().iloc[-1][:-1]
    d1 = d1.reset_index()

    tbl = []
    for asset in assets:
        tbl.append({name + 'col1': asset, name + 'col2': f'{corrs.loc[asset]:.1%}'})

    figs = []
    for asset in assets:
        fig = px.scatter(
            d1,
            x="Inflation",
            y=asset,
            trendline="ols",
            hover_data=dict({x: False for x in d1.columns}),
            hover_name="index",
        )
        fig.layout.xaxis["title"] = "Inflation"
        fig.layout.yaxis["title"] = None
        fig.update_traces(
            marker=dict(size=10, line=dict(width=2, color="DarkSlateGrey")),
            selector=dict(mode="markers"),
        )
        fig.update_layout(
            title={
                "text": asset,
                "y": 0.94,
                "x": 0.2,
                "xanchor": "center",
                "yanchor": "bottom",
            }
        )
        fig.update_yaxes(tickformat=".0%")
        fig.update_xaxes(tickformat=".0%")
        figs.append(fig)
    return [smallfig(fig) for fig in figs] + [tbl]

