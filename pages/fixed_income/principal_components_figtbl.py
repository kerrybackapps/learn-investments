import pandas as pd
from pages.data.yield_changes import yield_changes
from pages.formatting import smallfig
import plotly.graph_objects as go
import numpy as np


def figtbl(name, dates):
    start = str(dates[0]) + "-01"
    stop = str(dates[1]) + "-12"
    df = yield_changes.loc[start:stop]
    w, v = np.linalg.eigh(df.cov())
    n = len(df.columns)
    w = pd.Series(w[range(n-1, -1, -1)])
    w = w.cumsum() / w.sum()
    w.index = [f'first {i}' for i in range(1, n + 1)]
    w = pd.DataFrame(w).reset_index()
    w.columns = [name+'col1', name+'col2']
    v = pd.DataFrame(v, index=df.columns)
    v = v[range(n-1, -1, -1)]
    for i in v.columns:
        v[i] = v[i].iloc[0] * v[i]
    v = (100*v).round(1)
    v = v.reset_index()
    v.columns = ['maturity'] + [i for i in range(1, n+1)]
    v['maturity'] = [
        "1 year",
        "2 years",
        "3 years",
        "5 years",
        "10 years",
        "30 years"
    ]

    fig = go.Figure()
    #
    trace1 = go.Scatter(x=v.maturity, y=v[1],
                        mode='lines+markers',
                        name='first',
                        )

    trace2 = go.Scatter(x=v.maturity, y=v[2],
                        mode='lines+markers',
                        name='second',
                        )

    trace3 = go.Scatter(x=v.maturity, y=v[3],
                        mode='lines+markers',
                        name='third',
                        )

    for trace in [trace1, trace2, trace3]:
        fig.add_trace(trace)

    fig.update_layout(hovermode='x unified')

    fig.update_yaxes(title='Yield Changes (basis points)')
    fig.update_layout(yaxis_tickformat=',.0f',
                      xaxis_tickformat=',.0f')
    fig.update_xaxes(title='Maturity')

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
    ))

    v.columns = [name + 'maturity'] + [name + str(i) for i in range(1, n + 1)]

    return w.to_dict('records'), v.to_dict('records'), smallfig(fig, showlegend=True)

