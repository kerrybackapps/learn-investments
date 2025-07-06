import pandas as pd
import numpy as np
from scipy.stats import norm


def figtbl(K, sigma, r, q, T, s):

    K = float(K)
    sigma = float(sigma)
    r = float(r)
    q = float(q)
    T = float(T)
    s = float(s)

    sigma /= 100
    r /= 100
    q /= 100

    # call
    indx = [
        "d1",
        "N(d1)",
        "d2",
        "N(d2)",
        "exp(-qT)S",
        "exp(-rT)K",
        "exp(-qT)SN(d1)",
        "exp(-rT)KN(d2)",
        "call value",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    tbl.loc["d1"] = d1
    tbl.loc["N(d1)"] = norm.cdf(d1)
    d2 = d1 - sigma * np.sqrt(T)
    tbl.loc["d2"] = d2
    tbl.loc["N(d2)"] = norm.cdf(d2)
    tbl.loc["exp(-qT)S"] = np.exp(-q * T) * s
    tbl.loc["exp(-rT)K"] = np.exp(-r * T) * K
    tbl.loc["exp(-qT)SN(d1)"] = np.exp(-q * T) * s * norm.cdf(d1)
    tbl.loc["exp(-rT)KN(d2)"] = np.exp(-r * T) * K * norm.cdf(d2)
    tbl.loc["call value"] = np.exp(-q * T) * s * norm.cdf(d1) - np.exp(
        -r * T
    ) * K * norm.cdf(d2)
    tbl = tbl.round(4)
    tbl_call = tbl.reset_index().to_dict("records")

    # put
    #  np.exp(-r*T)*K*norm.cdf(-d2) - np.exp(-q*T)*s*norm.cdf(-d1)
    indx = [
        "d1",
        "N(-d1)",
        "d2",
        "N(-d2)",
        "exp(-qT)S",
        "exp(-rT)K",
        "exp(-rT)KN(-d2)",
        "exp(-qT)SN(-d1)",
        "put value",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    d1 = (np.log(s / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    tbl.loc["d1"] = d1
    tbl.loc["N(-d1)"] = norm.cdf(-d1)
    d2 = d1 - sigma * np.sqrt(T)
    tbl.loc["d2"] = d2
    tbl.loc["N(-d2)"] = norm.cdf(-d2)
    tbl.loc["exp(-qT)S"] = np.exp(-q * T) * s
    tbl.loc["exp(-rT)K"] = np.exp(-r * T) * K
    tbl.loc["exp(-qT)SN(-d1)"] = np.exp(-q * T) * s * norm.cdf(-d1)
    tbl.loc["exp(-rT)KN(-d2)"] = np.exp(-r * T) * K * norm.cdf(-d2)
    tbl.loc["put value"] = np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(
        -q * T
    ) * s * norm.cdf(-d1)
    tbl = tbl.round(4)
    tbl_put = tbl.reset_index().to_dict("records")

    return tbl_call, tbl_put
