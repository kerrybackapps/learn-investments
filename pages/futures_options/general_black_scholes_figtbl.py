import pandas as pd
import numpy as np
from scipy.stats import norm


def figtbl(receive, deliver, sigma, T):

    receive = float(receive)
    deliver = float(deliver)
    sigma = float(sigma)
    T = float(T)

    sigma /= 100

    indx = [
        "a",
        "N(a)",
        "b",
        "N(b)",
        "value_receive x N(a)",
        "value_deliver x N(b)",
        "option value",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    a = (np.log(receive/deliver) + 0.5 * sigma ** 2 * T) / (sigma * np.sqrt(T))
    tbl.loc["a"] = a
    Na = norm.cdf(a)
    tbl.loc["N(a)"] = Na
    b = a - sigma * np.sqrt(T)
    tbl.loc["b"] = b
    Nb = norm.cdf(b)
    tbl.loc["N(b)"] = Nb
    tbl.loc["value_receive x N(a)"] = receive * Na
    tbl.loc["value_deliver x N(b)"] = deliver * Nb
    tbl.loc["option value"] = receive*Na - deliver*Nb
    tbl = tbl.round(2)
    return tbl.reset_index().to_dict("records")

