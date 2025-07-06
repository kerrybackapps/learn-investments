from scipy.optimize import minimize
import numpy as np
import plotly.graph_objects as go
from pages.formatting import largefig, blue, green

#########################################
#
# pass spots and forwards in decimal form
#
#########################################

def price(prds, **kwargs):
    c = 100 * kwargs['coupon'] / 2
    maturity = kwargs['maturity']
    if 'yld' in kwargs.keys():
        yld = kwargs['yld']
        n = int(2 * maturity)
        return c * np.sum((1 + yld/2) ** np.arange(-1, -n - 1, -1)) + 100 / (1 + yld/2) ** n
    else:
        n = int(prds * maturity)
        pphy = int(prds/2)  # periods per half year
        spots = np.array(kwargs['spots'])
        # pv_factors = (1 + spots / 2) ** (-np.arange(1, len(spots) + 1))
        pv_factors = (1 + spots / prds) ** (-np.arange(1, len(spots) + 1))
        coupons = np.zeros(n)
        coupons[(pphy - 1)::pphy] = c
        return np.sum(coupons*pv_factors[:len(coupons)]) + 100*pv_factors[n-1]

def forward_rates(prds, spots):
    pphy = int(prds / 2)  # periods per half year
    future_factors = (1 + spots / 2) ** (np.arange(1, len(spots) + 1) / pphy)
    change_logs = np.diff(np.log(future_factors))
    f = (np.exp(change_logs)-1) * prds
    return np.concatenate(([spots[0]], f))

def objective(prds, bonds, spots):
    prices = [price(prds, **bond) for bond in bonds]
    phats = [price(prds=prds, maturity=bond['maturity'], coupon=bond['coupon'], spots=spots) for bond in bonds]
    errors = [np.log(phat/p) for phat, p in zip(prices, phats)]
    sse = np.sum([e**2 for e in errors])
    forwards = forward_rates(prds, spots)
    diffs = np.sum(np.diff(np.log(1+forwards/prds))**2)
    return sse + 0.5*diffs

def spot_rates(prds, bonds):
    maturities = [bond['maturity'] for bond in bonds]
    n = int(np.max(maturities) * prds)
    result = minimize(lambda x: objective(prds, bonds, x), [0.05]*n)
    return result.x if result.success==True else np.nan

def rateTree(r, sigma, dt, phis):
    delta = sigma*np.sqrt(dt)
    return [[r + phi + delta * (i - 2 * j) for j in range(i + 1)] for i, phi in enumerate(phis)]

def phi(sigma, prds, n, forwards):
    dt = 1/prds
    m = len(forwards)
    f = forwards[:n+1] if m>=n+1 else np.concatenate((forwards, [forwards[-1]]*(n+1-m)))
    term1 = np.log(1+f*dt)
    a = np.exp(sigma*dt**(3/2)*np.arange(n+1))
    term2 = np.log(a + 1/a)
    term3 = np.log(2*(1+f[0]*dt))
    return (term1 + term2 - term3) / dt

def zeroCouponTree(prds, maturity, tree):
    n = int(prds * maturity)
    rates = [np.array(x) for x in tree]
    x = 100 * np.ones(n + 1)
    lst = [x]
    i = n - 1
    while len(x) > 1:
        x = 0.5 * (x[:-1] + x[1:]) / (1 + rates[i] / prds)
        lst.insert(0, x)
        i -= 1
    return [list(x) for x in lst]

def treePlot(tree, dt, kind='rate'):
    string = "%{y:.2%}<extra></extra>" if kind=='rate' else "$%{y:,.2f}<extra></extra>"
    color = blue if kind=="rate" else green
    spliced = []
    for a, b in zip(tree[1:], tree[:-1]):
        x = []
        for i in range(len(a)):
            x.append(a[i])
            try:
                x.append(b[i])
            except:
                pass
        spliced.append(x)
    fig = go.Figure()
    for i in range(len(tree) - 1):
        x = [1, 0, 1]
        for j in range(i):
            x.append(0)
            x.append(1)
        x = np.array(x) + i
        y = spliced[i]
        trace = go.Scatter(
            x=x*dt,
            y=y,
            mode="lines+markers",
            hovertemplate=string,
            marker=dict(size=10, color=color),
            line=dict(color=color)
        )
        fig.add_trace(trace)
    fig.update_xaxes(title="Time (years)")
    if kind == "rate":
        fig.update_layout(yaxis_tickformat=".1%")
        fig.update_yaxes(title="Annualized Short Rate")
    else:
        fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=".0f")
        fig.update_yaxes(title="Zero-Coupon Bond Price", autorange="reversed")
    return fig

def figtbl(name, zerom, params, rows):

    params[1][name+"col2"] = 2 * int(params[1][name+"col2"] / 2)
    params[2][name+"col2"] = max(1, int(params[2][name+"col2"]))

    vol = float(params[0][name+"col2"])
    prds = int(params[1][name+"col2"])
    new_num = int(params[2][name+"col2"])

    dt = 1/prds
    sigma = vol / 10000

    old_num = len(rows)

    if new_num != old_num:
        num = min(new_num, old_num)
        row = {name+"maturity": 0, name+"coupon": 0, name+"yld": 0}
        rows = rows[:num] + [row]*(new_num-num)

    for row in rows:
        row[name+"maturity"] = np.round(2*float(row[name+"maturity"]), 0) / 2

    bonds = [dict(
        maturity=row[name+"maturity"],
        coupon=row[name+"coupon"] / 100,
        yld=row[name+"yld"] / 100
    ) for row in rows if float(row[name+"maturity"]) > 0]

    total = int(prds * np.max([bond["maturity"] for bond in bonds]))
    zerom = min(zerom, (total + 1) / prds)
    spots = spot_rates(prds, bonds)
    forwards = forward_rates(prds, spots)
    phis = phi(sigma, prds, total, forwards)
    tree = rateTree(spots[0], sigma, dt, phis)
    fig1 = treePlot(tree, dt)

    zero = zeroCouponTree(prds, zerom, tree)
    price = zero[0][0]
    rate = ((100/price)**(1/(prds*zerom)) - 1)*prds
    fig2 = treePlot(zero, dt, kind="dol")

    return params, rows, largefig(fig1), largefig(fig2), f"${price:,.2f}", f"{rate:.2%}"
