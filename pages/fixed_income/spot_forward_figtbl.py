from scipy.optimize import minimize
import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, blue, red, green

def price(**kwargs):
    n = int(2 * kwargs['maturity'])
    c = 100 * kwargs['coupon'] / 2
    if 'yld' in kwargs.keys():
        yld = kwargs['yld'] / 2
        return c * np.sum((1 + yld) ** np.arange(-1, -n - 1, -1)) + 100 / (1 + yld) ** n
    else:
        spots = np.array(kwargs['spots']) / 2
        return c * np.sum((1 + spots[:n]) ** np.arange(-1, -n - 1, -1)) + 100 / (1 + spots[n - 1]) ** n

def error(bond, spots):
    p = price(**bond)
    m = bond['maturity']
    n = int(2 * m)
    phat = price(maturity=m, coupon=bond['coupon'], spots=spots[:n])
    return np.log(phat / p)

def forward_rates(spots):
    future_factors = (1+spots/2)**np.arange(1,len(spots)+1)
    change_logs = np.diff(np.log(future_factors))
    f = 2 * (np.exp(change_logs)-1)
    return np.concatenate(([spots[0]], f))

def objective(bonds, spots):
    sse = np.sum([error(bond, spots)**2 for bond in bonds])
    forwards = forward_rates(spots)
    diffs = np.sum(np.diff(np.log(1+forwards/2))**2)
    return sse + 0.5*diffs

def spot_rates(bonds):
    maturities = [bond['maturity'] for bond in bonds]
    n = int(2*np.max(maturities))
    result = minimize(lambda x: objective(bonds, x), [0.05]*n)
    return result.x if result.success==True else np.nan

def figtbl(name, num, rows):
    new_num = max(int(num), 1)
    old_num = len(rows)

    if new_num != old_num:
        n = min(new_num, old_num)
        row = {name+"maturity": 0, name+"coupon": 0, name+"yld": 0}
        rows = rows[:n] + [row]*(new_num-n)

    for row in rows:
        row[name+"maturity"] = np.round(2*float(row[name+"maturity"]),0) / 2

    bonds = [dict(
        maturity=row[name+"maturity"],
        coupon=row[name+"coupon"] / 100,
        yld=row[name+"yld"] / 100
    ) for row in rows if float(row[name+"maturity"])>0]

    trace1 = go.Scatter(
        x=[bond['maturity'] for bond in bonds],
        y=[bond['yld'] for bond in bonds],
        name='yield',
        mode='markers',
        marker=dict(size=10, color=red)
    )

    maxmaturity = np.max([bond['maturity'] for bond in bonds])
    spots = spot_rates(bonds)
    forwards = forward_rates(spots)

    trace2 = go.Scatter(
        x=np.arange(0.5, maxmaturity + 0.5, 0.5),
        y=spots,
        name='spot rate',
        mode='markers+lines',
        marker=dict(color=green),
        line=dict(color=green)
    )
    trace3 = go.Scatter(
        x=np.arange(0.5, maxmaturity + 0.5, 0.5),
        y=forwards,
        name='forward rate',
        mode='markers+lines',
        marker=dict(color=blue),
        line=dict(color=blue)
    )
    fig = go.Figure()
    fig.add_trace(trace3)
    fig.add_trace(trace2)
    fig.add_trace(trace1)

    fig.update_xaxes(rangemode="tozero")
    fig.layout.xaxis["title"] = "Maturity (years)"
    fig.layout.yaxis["title"] = "Rate"
    fig.update_yaxes(tickformat=".2%")
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.update_layout(hovermode="x unified")

    ymax = np.max([bond['yld'] for bond in bonds])
    ymin = np.min([bond['yld'] for bond in bonds])
    smax = np.max(spots)
    smin = np.min(spots)
    fmax = np.max(forwards)
    fmin = np.min(forwards)
    amax = np.max([ymax,smax,fmax])
    amin = np.min([ymin,smin,fmin])
    amid = (amax+amin)/2
    amax = np.max([amax+0.01, amid+0.02])
    amin = np.min([amin-0.01,amid-0.02])
    fig.update_layout(yaxis=dict(range=[amin,amax]))

    return rows, largefig(fig, showlegend=True)
