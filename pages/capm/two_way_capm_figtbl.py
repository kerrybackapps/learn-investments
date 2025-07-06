from pandas_datareader import DataReader as pdr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, green, style_data_conditional, style_header, gray200
from pages.data.ff_monthly import ff3 as ff
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
from dash import dcc, html
import statsmodels.api as sm
import plotly.express as px

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

def Sharpe(df):
    return 100 * np.sqrt(12) * df.mean() / df.std()

def figtbl(name, char, dates):
    content = dict(char=char, dates=dates)
    global CHAR, RETS

    if char != CHAR:
        CHAR = char
        RETS = pdr(charsDict[char], "famafrench", start=1926)[0] / 100
        RETS = RETS.subtract(ff.RF, axis="index")
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

    mns = 12 * df.mean()
    mns.index = [a + '-' + b for a, b in splits]
    sds = np.sqrt(12) * df.std()
    sds.index = [a + '-' + b for a, b in splits]

    # 5x5 table calculations

    df.columns = pd.MultiIndex.from_tuples(splits)

    # multi-indexed index, for unstacking
    regr = pd.DataFrame(dtype=float, index=df.columns, columns=['alpha', 'beta', 'tstat', 'pval', 'empirical', 'theoretical'])
    df['Mkt-RF'] = ff['Mkt-RF']

    for port in regr.index:
        result = sm.OLS(df[port], sm.add_constant(df['Mkt-RF'])).fit()
        regr.loc[port, 'alpha'] = result.params['const']
        regr.loc[port, 'beta'] = result.params['Mkt-RF']
        regr.loc[port, 'tstat'] = result.tvalues['const']
        regr.loc[port, 'pval'] = result.pvalues['const']
        regr.loc[port, 'empirical'] = 12 * df[port].mean()
        regr.loc[port, 'theoretical'] = 12 * result.params['Mkt-RF'] * df['Mkt-RF'].mean()

    # 5 x 5 tables

    alphas = 12*regr.alpha.unstack()
    tstats = regr.tstat.unstack()


    # betas and means

    regr['port'] = mns.index
    fig1 = px.scatter(
        regr,
        x="beta",
        y="empirical",
        hover_name="port",
        trendline="ols",
    )
    fig1.update_traces(
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )

    fig2 = px.scatter(regr, x="beta", y="theoretical", hover_name="port")
    fig2.update_traces(
        marker=dict(size=12, color=green, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig = go.Figure(data=fig1.data + fig2.data)


    fig.layout.xaxis["title"] = "Beta"
    fig.layout.yaxis["title"] = "Mean Excess Return (Annualized)"
    fig.update_yaxes(tickformat=".1%")
    fig.update_xaxes(tickformat=".2")
    fig_alpha = largefig(fig)

    # alpha heatmap matrix

    trace = go.Heatmap(
        x=alphas.columns.to_list(),
        y=alphas.index.to_list(),
        z=alphas ,
        colorscale='Viridis',
        texttemplate="%{z:.1%}"
    )
    alpha_tbl = go.Figure(trace)
    alpha_tbl = largefig(alpha_tbl)

    # tstats heatmap matrix

    trace = go.Heatmap(
        x=tstats.columns.to_list(),
        y=tstats.index.to_list(),
        z=tstats,
        colorscale='Viridis',
        texttemplate="%{z:.2f}"
    )
    tstat_tbl = go.Figure(trace)
    tstat_tbl = largefig(tstat_tbl)


    left = dbc.Col(
        [
        dbc.Label('alphas (annualized)'),
        dcc.Graph(figure=alpha_tbl),
        ],
        md=6)

    right = dbc.Col(
       [
        dbc.Label('t statistics'),
        dcc.Graph(figure=tstat_tbl),
        ],
        md=6
    )


    row = dbc.Row([left, right], align="end")

    # title = html.H5(dbc.Badge("Tests of the CAPM", className="ms-1"))
    # title = dbc.Col(title, width={"size": 2, "offset": 5})
    # title = dbc.Row(title)

    content['alphas'] = html.Div([html.Br(), row, html.Br(), dcc.Graph(figure=fig_alpha)])

    return content
