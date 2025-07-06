import plotly.express as px
from pandas_datareader import DataReader as pdr
from pages.formatting import largefig

def figtbl(nclicks):

    files = ["DFII" + x for x in ["5", "7", "10", "20", "30"]]
    df = pdr(files, "fred", start=1920) / 100
    df.index.name = "date"
    df = df.reset_index()

    df["month"] = df.date.dt.to_period("M").astype(str)
    df = df.groupby("month").first()
    df = df.drop(columns=["date"])
    # df = df.dropna(subset=['DFII30'])
    df = df.dropna(subset=["DFII20"])
    df.columns = [5, 7, 10, 20, 30]

    df = df.stack()
    df = df.reset_index()
    df.columns = ["month", "term", "rate"]

    fig = px.line(
        df,
        x="term",
        y="rate",
        animation_frame="month",
        hover_data={"month": True, "term": True, "rate": True}
    )
    fig.for_each_trace(lambda t: t.update(mode='lines+markers', marker=dict(size=10)))
    for fr in fig.frames:
        for d in fr.data:
            d.update(mode='markers+lines', marker=dict(size=10))
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig.update_layout(
        xaxis=dict(
            title="Years to Maturity",
            tickvals=[1, 3, 5, 10, 20, 30],
            range=[0, 30]
        ),
        yaxis=dict(
            tickformat=".1%",
            title="Real Yield",
            range=[df.rate.min() - 0.001, df.rate.max() + 0.001],

        ),
    )
    return largefig(fig)

