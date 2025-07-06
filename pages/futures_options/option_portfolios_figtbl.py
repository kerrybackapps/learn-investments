# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 17:50:07 2022

@author: kerry
"""

import numpy as np
import pandas as pd
import plotly.express as px
from pages.formatting import largefig


class Option(list):
    def add(self, security, quantity, strike=None):
        self.append(dict(security=security, quantity=quantity, strike=strike))

    def strikes(self):
        return [
            d["strike"] for d in self if d["security"] not in ["Underlying", "Cash"]
        ]

    def grid(self):
        strikes = self.strikes()
        maxstrike = 100 if len(strikes) == 0 else 1.5 * np.max(strikes)
        return np.linspace(0, maxstrike, 200)

    def value(self):
        grid = self.grid()
        value = np.zeros(len(grid))
        for x in self:
            if x["security"] == "Cash":
                value += x["quantity"]
            elif x["security"] == "Underlying":
                value += x["quantity"] * grid
            elif x["security"] == "Call":
                value += x["quantity"] * np.maximum(grid - x["strike"], 0)
            else:
                value += x["quantity"] * np.maximum(x["strike"] - grid, 0)
        return value

    def plot(self):
        df = pd.DataFrame(self.grid(), columns=["Underlying"])
        df["Portfolio"] = self.value()
        fig = px.line(df, x="Underlying", y="Portfolio")
        fig.layout.xaxis["title"] = "Underlying Price"
        fig.layout.yaxis["title"] = "Portfolio Value"
        fig.update_layout(xaxis_tickprefix="$", xaxis_tickformat=",.0f")
        fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
        return largefig(fig)


def figtbl(*args):
    x = Option()
    cash = args[0]
    if cash == "Long":
        x.add(security="Cash", quantity=args[1])
    elif cash == "Short":
        x.add(security="Cash", quantity=-args[1])
    underlying = args[2]
    if underlying == "Long":
        x.add(security="Underlying", quantity=args[3])
    elif underlying == "Short":
        x.add(security="Underlying", quantity=-args[3])
    for i, arg in enumerate(args):
        if arg == "Call":
            x.add(security="Call", strike=args[i + 1], quantity=args[i + 2])
        elif arg == "Put":
            x.add(security="Put", strike=args[i + 1], quantity=args[i + 2])
    return x.plot()
