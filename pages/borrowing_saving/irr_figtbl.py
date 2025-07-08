import numpy as np
import pandas as pd
import numpy_financial as npf
from pages.formatting import smallfig, blue, red, green, largefig
import plotly.graph_objects as go


def figtbl(name, N, rows):

    fig = go.Figure()

    new_numdates = max(int(N), 0) + 1
    old_numdates = len(rows)

    tbl1 = [{name + 'date': str(i)} for i in range(new_numdates)]

    if new_numdates != old_numdates:
        n = min(new_numdates, old_numdates)
        rows = rows[:n] + [{name+'cashflow': 0} for i in range(new_numdates-n)]

    cashFlows = [float(row[name+"cashflow"]) for row in rows]

    irr = npf.irr(cashFlows)
    IRR = (irr is not np.nan)

    if IRR:
        pvfactors = 1 / (1 + irr) ** np.arange(new_numdates)
        pvs = np.array(cashFlows) * pvfactors
        tbl3 = [{name + 'pv-factor': f'{factor:.1%}', name + 'pv': f'{pv:.2f}'} for factor, pv in zip(pvfactors, pvs)]
        string = f"{irr:.2%}"
        grid = (np.arange(0, 2 * irr, 0.001) if irr>0
                else np.arange(2*irr, 0, 0.001) if irr<0
                else np.arange(-.1, .1001, .001)
                )

    else:
        tbl3 = [{name + 'pv-factor': "NA", name + 'pv': "NA"} for i in range(new_numdates)]
        string = "Does Not Exist"
        grid = np.arange(0, 1, 0.001)

    npvs = [npf.npv(r, cashFlows) for r in grid]

    string1 = "NPV = $%{y:,.2f} when discount rate = %{x:.1%}<extra></extra>"
    trace1 = go.Scatter(
        x=grid, y=npvs, mode="lines", hovertemplate=string1, line=dict(color=blue)
    )
    fig.add_trace(trace1)

    if IRR:
        trace2 = go.Scatter(
            x=grid,
            y=[0] * len(grid),
            mode="lines",
            line=dict(dash="dot", color=red),
            hovertemplate="<extra></extra>",
        )

        string3 = f'NPV = 0 when discount rate = {irr:.2%}<extra></extra>'
        trace3 = go.Scatter(
            x=[irr],
            y=[0],
            mode="markers",
            marker=dict(size=15, color=green),
            hovertemplate=string3,
        )

        fig.add_trace(trace2)
        fig.add_trace(trace3)

    fig.layout.xaxis["title"] = "Discount Rate"
    fig.layout.yaxis["title"] = "Net Present Value"
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
    fig.update_layout(xaxis_tickformat=".0%")

    # Make figure with better proportions
    fig.update_layout(height=450)
    return tbl1, rows, tbl3, string, smallfig(fig)

