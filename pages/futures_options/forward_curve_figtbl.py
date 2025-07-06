# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:11:44 2022

@author: kerry
"""

import pandas as pd
from pages.formatting import largefig
import plotly.express as px

DATA = None
FLAG = False

dct = {
    "CME Australian Dollar Futures": ["CME_AD", "currency", 1, "Australian Dollar"],
    "CME Soybean Oil Futures": ["CME_BO", "commodity", 100, "Pound"],
    "CME British Pound Futures": ["CME_BP", "currency", 1, "British Pound"],
    "CME Corn Futures": ["CME_C", "commodity", 100, "Bushel"],
    "CME Canadian Dollar Futures": ["CME_CD", "currency", 1, "Canadian Dollar"],
    "CME Crude Oil Futures": ["CME_CL", "commodity", 1, "Barrel"],
    "CME Dow Jones Ind Avg (DJIA)": ["CME_DJ", "index", 1],
    "CME Euro FX Futures": ["CME_EC", "currency", 1, "Euro"],
    "CME Eurodollar Futures": ["CME_ED", "index", 1],
    "CME E-mini S&P 500 Futures": ["CME_ES", "index", 1],
    "CME 30 Day Federal Funds Futures": ["CME_FF", "index", 1],
    "CME 5 Yr Note Futures": ["CME_FV", "index", 1],
    "CME Gold Futures": ["CME_GC", "commodity", 1, "Ounce"],
    "CME Copper Futures": ["CME_HG", "commodity", 1, "Pound"],
    "CME NY Harbor ULSD Futures": ["CME_HO", "commodity", 1, "Gallon"],
    "CME Japanese Yen Futures": ["CME_JY", "currency", 100000, "Japanese Yen"],
    "CME KC HRW Wheat Futures": ["CME_KW", "commodity", 100, "Bushel"],
    "CME Live Cattle Futures": ["CME_LC", "commodity", 100, "Pound"],
    "CME Lean Hog Futures": ["CME_LN", "commodity", 100, "Pound"],
    "CME E-mini S&P MidCap 400 Futures": ["CME_MD", "index", 1],
    "CME Mexican Peso Futures": ["CME_MP", "currency", 100000, "Mexican Peso"],
    "CME New Zealand Dollar Futures": ["CME_NE", "currency", 1, "New Zealand Dollar"],
    "CME Natural Gas (Henry Hub) Physical Futures": ["CME_NG", "commodity", 1, "MMBtu"],
    "CME Nikkei/USD Futures": ["CME_NK", "index", 1],
    "CME E-mini NASDAQ 100 Futures": ["CME_NQ", "index", 1,],
    "CME Oats Futures": ["CME_O", "commodity", 100, "Bushel"],
    "CME Palladium Futures": ["CME_PA", "commodity", 1, "Ounce"],
    "CME Platinum Futures": ["CME_PL", "commodity", 1, "Ounce"],
    "CME RBOB Gasoline Physical Futures": ["CME_RB", "commodity", 1, "Gallon"],
    "CME E-mini Russell 1000 Index Futures": ["CME_RS1", "index", 1],
    "CME E-mini Russell 2000 Index Futures": ["CME_RTY", "index", 1],
    "CME Soybean Futures": ["CME_S", "commodity", 100, "Bushel"],
    "CME Swiss Franc Futures": ["CME_SF", "currency", 1, "Swiss Franc"],
    "CME Silver Futures": ["CME_SI", "commodity", 1, "Ounce"],
    "CME Soybean Meal Futures": ["CME_SM", "commodity", 1, "Ton"],
    "CME S&P 500 Futures": ["CME_SP", "index", 1],
    "CME 2 Yr Note Futures": ["CME_TU", "index", 1],
    "CME 10 Yr Note Futures": ["CME_TY", "index", 1],
    "CME U.S. Treasury Bond Futures": ["CME_US", "index", 1],
    "CME Wheat Futures": ["CME_W", "commodity", 100, "Bushel"],
    "ICE Rotterdam Coal Futures": ["ICE_ATW", "commodity", 1, "Ton"],
    "ICE Brent Crude Oil Futures": ["ICE_B", "commodity", 1, "Barrel"],
    "ICE Cocoa Futures": ["ICE_CC", "commodity", 1, "Ton"],
    "ICE Cotton Futures": ["ICE_CT", "commodity", 100, "Pound"],
    "ICE US Dollar Index Futures": ["ICE_DX", "index", 1],
    "ICE Gasoil Futures": ["ICE_G", "commodity", 1, "Ton"],
    "ICE Coffee C Futures": ["ICE_KC", "commodity", 100, "Pound"],
    "ICE UK Natural Gas Futures": ["ICE_M", "commodity", 1, "Therm"],
    "ICE British Pound GBP Futures": ["ICE_MP", "currency", 1, "British Pound GBP"],
    "ICE Heating Oil Futures": ["ICE_O", "commodity", 1, "Gallon"],
    "ICE Orange Juice Futures": ["ICE_OJ", "commodity", 100, "Pound"],
    "ICE Russell 1000 Index Mini": ["ICE_RF", "index", 1],
    "ICE Sugar No. 11": ["ICE_SB", "commodity", 100, "Pound"],
    "ICE WTI Crude Oil Futures": ["ICE_T", "commodity", 1, "Barrel"],
    "ICE Russell 2000 Index Mini": ["ICE_TF", "index", 1],
}

keys = list(dct.keys())
keys.sort()


def figtbl(name):
    global DATA, FLAG
    if not FLAG:
        DATA = pd.read_csv('https://www.dropbox.com/s/832hth1es40f4g7/newfutures.csv?dl=1')
        FLAG = True

    contract = dct[name][0]
    d2 = DATA[DATA.code==contract].copy()
    d2.settle = d2.settle / dct[name][2]

    # get the title of y_axis
    if dct[name][1] == "commodity" or dct[name][1] == "currency":
        # E.g. 'Price per Pound', 'Price per Euro'
        yaxis_title = "Price per " + dct[name][3]
    else:
        # E.g., for S&P 500 Futures, it prints 'S&P 500 Index'
        words = name.split()
        for word in words:
            if word in ['CME', 'ICE', 'E-mini', 'Futures', 'Index']:
                words.remove(word)
        if "E-mini" in words:
            words.remove("E-mini")
        yaxis_title = " ".join(words)
        yaxis_title += " Index"

    fig = px.line(
        d2,
        x='months past front month',
        y='settle',
        animation_frame='date'
    )

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100
    fig.update_yaxes(range=[min(0, d2.settle.min()), 1.1 * d2.settle.max()])
    fig.update_xaxes(range=[0, d2["months past front month"].max()])
    fig.for_each_trace(lambda t: t.update(mode='lines+markers', marker=dict(size=10)))
    for fr in fig.frames:
        for d in fr.data:
            d.update(mode='markers+lines', marker=dict(size=10))
    fig.update_yaxes(tickformat=".2f", title=yaxis_title)
    if name in ['CME S&P 500 Futures',
                "CME Dow Jones Ind Avg (DJIA)",
                "CME E-mini S&P 500 Futures",
                "CME Gold Futures",
                "CME E-mini Russell 1000 Index Futures",
                "CME E-mini Russell 2000 Index Futures",
                "ICE Russell 2000 Index Mini",
                "CME E-mini NASDAQ 100 Futures",
                "CME E-mini S&P MidCap 400 Futures"
                ]:
        fig.update_yaxes(tickformat=".0f")
    fig.update_xaxes(title="Months Past Front Month")
    # fig.update_yaxes(rangemode="tozero")

    return largefig(fig)
