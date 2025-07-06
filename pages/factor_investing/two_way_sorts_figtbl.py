from pandas_datareader import DataReader as pdr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, blue, red
from pages.data.ff_monthly import ff3 as ff
import dash_bootstrap_components as dbc
from dash import dcc, html
import copy

files = [
    '25_Portfolios_5x5',
    '25_Portfolios_ME_INV_5x5',
    '25_Portfolios_ME_Prior_12_2',
    '25_Portfolios_ME_Prior_1_0',
    '25_Portfolios_ME_Prior_60_13',
    '25_Portfolios_ME_AC_5x5',
    '25_Portfolios_ME_BETA_5x5',
    '25_Portfolios_ME_NI_5x5',
    '25_Portfolios_ME_VAR_5x5',
    '25_Portfolios_ME_RESVAR_5x5'
]

chars = [
    "Book to market ratio",
    "Investment rate",
    "Momentum",
    "Short term reversal",
    "Long term reversal",
    "Accruals",
    "Beta",
    "Net equity issuance",
    "Variance",
    "Residual variance",
]

charsDict = dict(zip(chars, files))
chars.sort()

RETS = None
CHAR = None

def figtbl(char, dates):
    content = dict(char=char, dates=dates)
    global CHAR, RETS
    if char != CHAR:
        CHAR = char
        RETS = pdr(charsDict[char], "famafrench", start=1926)[0] / 100
        if char == "Net equity issuance":
            for x in RETS.columns:
                if x.split(" ")[1][0] == "Z" or x.split(" ")[1][0:2] == "Ne":
                    RETS = RETS.drop(columns=x)

    start = str(dates[0]) + "-01"
    stop = str(dates[1]) + "-12"
    df = RETS.loc[start:stop].copy()

    # see what the two chars are in the two-way sort
    s = df.columns[1].split(" ")
    s1 = s[0][:-1]             # market equity
    s2 = s[1][:-1]             # other characteristic

    def splitName(x):
        x1 = x.split(" ")[0]
        x1 = x1 if x1[0] == "M" else ("ME1" if x1[0] == "S" else "ME5")
        x2 = x.split(" ")[1]
        x2 = x2 if x2[0] == s2[0] else (s2 + "1" if x2[0] == "L" else s2 + "5")
        return x1, x2

    splits = [splitName(x) for x in df.columns]

    # 5x5 table calculations




    """
    # std devs and means

    trace = go.Scatter(
        x=sds,
        y=mns,
        mode='markers',
        text=sds.index.to_list(),
        hovertemplate='%{text}<br>Mean = %{y:.1%}<br>Std Dev = %{x:.1%}<extra></extra>',
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey"))
    )
    fig = go.Figure(trace)
    fig.layout.xaxis["title"] = "Standard Deviation of Excess Return (Annualized)"
    fig.layout.yaxis["title"] = "Mean Excess Return (Annualized)"
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%", rangemode="tozero")
    fig_mean = largefig(fig)
    """

    dates = df.reset_index().iloc[:,0].astype(str)

    accum = (1+df).cumprod()

    accum.columns = range(25)
    names = ["small char/small cap", "large char/small cap", "small char/large cap", "large char/large cap"]
    cols = [0, 4, 20, 24]
    colors = [blue, blue, red, red]
    traces = []
    for i, (col, name, color) in enumerate(zip(cols, names, colors)):
        if i%2 !=0:
            trace = go.Scatter(
                x = dates,
                y = accum[col],
                mode="lines",
                name=name,
                line=dict(color=color, dash="dash"),
                hovertemplate="%{x}<br>$%{y:.2f}<extra></extra>"
            )
        else:
            trace = go.Scatter(
                x = dates,
                y = accum[col],
                mode="lines",
                name=name,
                line=dict(color=color),
                hovertemplate="%{x}<br>$%{y:.2f}<extra></extra>"
            )
        traces.append(trace)
    accum_plot = go.Figure()
    for trace in traces:
        accum_plot.add_trace(trace)
    accum_plot.update_layout(legend=dict(x=0.01, y=0.99))

    accum_log_plot = copy.copy(accum_plot)

    accum_log_plot.update_yaxes(type="log")
    accum_plot.layout.yaxis.title="Accumulation"
    accum_log_plot.layout.yaxis.title="Accumulation (log scale)"

    # means tab
    df.columns = pd.MultiIndex.from_tuples(splits)
    df = df.subtract(ff.RF, axis="index")

    means = 12 * df.mean().unstack()
    sharpes = np.sqrt(12) * df.mean() / df.std()
    sharpes = sharpes.unstack()


    trace = go.Heatmap(
        x=means.columns.to_list(),
        y=means.index.to_list(),
        z=means,
        colorscale='Viridis',
        texttemplate="%{z:.1%}",
        hovertemplate="%{x} / %{y}<br>%{z:.2%}<extra></extra>"
    )
    means_tbl = go.Figure(trace)
    means_tbl = largefig(means_tbl)

    trace = go.Heatmap(
        x=sharpes.columns.to_list(),
        y=sharpes.index.to_list(),
        z=sharpes,
        colorscale='Viridis',
        texttemplate="%{z:.1%}",
        hovertemplate="%{x} / %{y}<br>%{z:.2%}<extra></extra>"
    )
    sharpes_tbl = go.Figure(trace)
    sharpes_tbl = largefig(sharpes_tbl)

    left = dbc.Col(
        [
            dbc.Label('Mean excess returns (annualized)'),
            dcc.Graph(figure=means_tbl),
        ],
        md=6
    )
    right = dbc.Col(
        [
            dbc.Label('Sharpe ratios (annualized)'),
            dcc.Graph(figure=sharpes_tbl),
        ],
        md=6
    )


    row = dbc.Row(
        [
            left,
            right
        ],
        align="top"
    )
    left = dbc.Col(dcc.Graph(figure=largefig(accum_plot, showlegend=True)), md=6)
    right = dbc.Col(dcc.Graph(figure=largefig(accum_log_plot, showlegend=True)), md=6)
    row2 = dbc.Row([left, right])
    content['means'] = html.Div([html.Br(), row, html.Br(), row2])
    content['alpha'] = None

    return content
