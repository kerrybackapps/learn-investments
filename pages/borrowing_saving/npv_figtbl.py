import numpy as np
import pandas as pd

def figtbl(name, N, r, rows):
    new_numdates = max(int(N), 0) + 1
    old_numdates = len(rows)

    tbl1 = [{name+'date': str(i)} for i in range(new_numdates)]

    if new_numdates != old_numdates:
        n = min(new_numdates, old_numdates)
        rows = rows[:n] + [{name+'cashflow': 0} for i in range(new_numdates-n)]

    cashFlows = [float(row[name+"cashflow"]) for row in rows]

    r = float(r) / 100

    pvfactors = 1 / (1+r)**np.arange(new_numdates)
    pvs = np.array(cashFlows) * pvfactors
    tbl3 = [{name+'pv-factor': f'{factor:.1%}', name+'pv': f'{pv:.2f}'} for factor, pv in zip(pvfactors, pvs)]

    string = f"${np.sum(pvs):.2f}"
    return tbl1, rows, tbl3, string

