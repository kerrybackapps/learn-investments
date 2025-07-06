import numpy as np
import pandas as pd

def figtbl(name, N, r, g, cf, rows):

    cf = float(cf)

    N = max(int(N), 0)
    old_N = len(rows)

    tbl1 = [{name+'date': str(i+1)} for i in range(N)]

    if N != old_N:
        n = min(N, old_N)
        rows = rows[:n] + [{name+'cashflow': 0} for i in range(N-n)]

    cashFlows = np.array([float(row[name+"cashflow"]) for row in rows])

    r = float(r) / 100
    g = float(g) / 100

    pv1 = np.sum(cashFlows / (1+r)**np.arange(1,N+1))
    if r > g:
        tv = cf / (r-g)  # (1+g) * cashFlows[-1] / (r-g)
        pv2 = tv / (1+r)**N
        npv = pv1 + pv2
        s1 = f'{tv:,.2f}'
        s2 = f'{pv2:,.2f}'
        s3 = f'{npv:,.2f}'

    else:
        s1 = 'Infinite'
        s2 = 'Infinite'
        s3 = 'Infinite'

    tbl3 = [
        {name+'col1': 'Terminal value', name+'col2': s1},
        {name+'col1': 'PV of terminal value', name+'col2': s2},
        {name + 'col1': 'PV of first-stage cash flows', name + 'col2': f'{pv1:,.2f}'},
        {name+'col1': 'Total present value', name+'col2': s3}
        ]

    return tbl1, rows, tbl3

