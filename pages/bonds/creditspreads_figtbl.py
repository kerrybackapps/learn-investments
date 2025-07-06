import pandas as pd
import plotly.express as px
from pandas_datareader import DataReader as pdr
from pages.formatting import largefig

def figtbl(nclicks):

    files = ["BAMLC0A4CBBB", "BAMLC0A3CA", "BAMLC0A2CAA", "BAMLC0A1CAAA"]

    df = pdr(files, "fred", start=1920) / 100
    df.index.name = "date"
    df = df.reset_index()
    df["month"] = df.date.dt.to_period("M").astype(str)
    df = df.groupby("month").first()
    df = df.drop(columns=["date"])
    df = df.dropna()
    df.columns = ["BBB", "A", "AA", "AAA"]

    # stack the dataframe and make a column of rating
    df.columns.name = "Rating"
    d1 = df.stack()
    d1.name = "yield"
    d1 = d1.reset_index()
    d1["yield_percent"] = d1["yield"] * 100
    d1["yield_percent"] = d1["yield_percent"].round(decimals=4)

    fig = px.line(
        d1,
        x="month",
        y="yield",
        color="Rating",
        custom_data=["Rating"],
        hover_data=["yield_percent"],
    )
    fig.layout.xaxis["title"] = "Date"
    fig.layout.yaxis["title"] = "Credit Spread"
    string = "%{customdata[0]}<br>%{customdata[1]}%<extra></extra>"
    fig.update_traces(hovertemplate=string)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, title=""))

    return largefig(fig, showlegend=True)
