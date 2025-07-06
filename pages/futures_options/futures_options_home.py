

from pages.formatting import Layout, Overview

title = "Overview: Futures and options"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"

urls = {"Python notebook": None}
text = """
This section presents animations of the histories of forward curves based on CME futures prices for commodities,
metals, currencies, and financials.  Most of the section concerns options: option spreads, Black-Scholes, 
implied vols, delta hedging, and binomial trees.  The pages are described below, and links to the pages are provided in
the navigation bar above and on the drop-down menu at the top right of each page.
"""

title1 = "Forward Curves"
text1 = """
  This page presents animations of the histories of forward curves based on CME futures 
  prices.  The user selects the commodity, metal, currency, or financial futures contract to be presented. 
  """
title2 = "Market Option Data"
text2 = """
  This page displays data provided by Yahoo Finance on 15-minute delayed stock and ETF 
  put and call option quotes, transaction prices, volume, open interest, and implied volatilities.  The user
  specifies the ticker and the maturity of the options.
  """
title3 = "Option Portfolios"
text3 = """
  This page creates plots of the value at maturity of a portfolio in an underlying asset, cash,
  put options, and call options.  The user inputs the securities in the portfolio and the strike prices of the
  options.  The page is useful for illustrating option hedges and spreads.
  """
title4 = "Put-Call Parity"
text4 = """ 
  This page explains the put-call parity relationship for European options.  The difference
  between call and put prices is plotted as a function of the underlying price for user-specified option and 
  underlying parameters.
  """
title5 = "Black-Scholes Formula"
text5 = """
  This page demonstrates the calculation of the Black-Scholes formula for call and
  put prices in a tabular form for user-specified option and underlying parameters.
  """
title6 = "Black-Scholes Plots"
text6 = """
  This page plots the Black-Scholes formula as a function of the underlying price for 
  user-specified option and underlying parameters.
  """
title7 = "Monte Carlo Option Valuation"
text7 = """
  This page explains how the Black-Scholes formulas can be approximated by
  discounting the average simulated option value at maturity, simulating under the risk-neutral 
  distribution.  Histograms of 
  call and put values at maturity are presented.  The user specifies the option and underlying parameters and can
  regenerate the simulation.
  """
title8 = "Implied Volatilities"
text8 = """
  This page explains implied volatilities as the volatilities in the Black-Scholes formula
  that equate the formula to market option premia.  The user specifies the option and underlying parameters and also
  the call and put premia.
  """
title9 = "Market Implied Volatilities"
text9 = """
  This page plots implied volatilities supplied by Yahoo Finance and based on
  market data for calls and puts as functions of the option strike prices.  The user specifies the ticker and
  the maturity of the options.
  """
title10 = "Option Greeks"
text10 = """
  The delta, gamma, vega, theta, and rho of calls and puts based on the Black-Scholes formula 
  are calculated and plotted for user-specified option and underlying parameters.
  """
title11 = "Delta Hedges"
text11 = """
  Delta hedges for calls and puts are calculated from the Black-Scholes formula and plotted for
  user-specified option and underlying parameters.  The plots illustrate that delta hedges are linear (cash + position
  in underlying) approximations to the Black-Scholes formula.
  """
title12 = "Delta Hedges of Option Portfolios"
text12 = """
  The user specifies a portfolio of cash, the underlying, and puts and calls
  as in the "Option Portfolios" page.  A delta hedge is calculated from the Black-Scholes formula for user
  specified parameters, and the Black-Scholes
  value of the portfolio and the delta hedge are plotted as functions of the underlying price.  The page illustrates 
  that an investor who wants to delta hedge only needs to hedge the net delta of the portfolio.
  """
title13 = "Binomial Trees"
text13 = """
  Binomial trees are generated and plotted for the underlying asset price and call and put values for
  user-specified inputs.  The user specifies the risk-free rate and volatility on a per-period basis, as well as the
  number of periods in the trees.
  """
title14 = "Calibrated Binomial Trees"
text14 = """
  Binomial trees are generated and plotted for the underlying asset price and call and put values for
  user-specified inputs.  The user specifies the risk-free rate, dividend yield, and volatility on an annual basis.  The
  user also specifies the time to maturity of the options and the number of periods in the trees.
  """
title15 = "Binomial Convergence"
text15 = """
  This page plots call and put values calculated from binomial trees with 2 to 100 time
  periods to illustrate the convergence of the values to the Black-Scholes values as the number of time steps 
  is increased.  The user specifies the option
  and underlying parameters.
  """
title16 = "American Option Exercise Boundaries"
text16 = """
  This page calculates optimal exercise boundaries for American options,
  based on a binomial model, for user-specified option and underlying parameters.
  """
title17 = "European and American Option Values"
text17 = """
  This page plots European and American option values as functions of the
  underlying asset price.  The European option values are computed from the Black-Scholes
  formula, and American option values are computed from a binomial model.  American option values are equal
  to European option values for call options on non-dividend paying assets ("calls are better alive than dead") but are
  typically higher.  A European option value can sometimes be less than the option's intrinsic value.
  """
title18 = "American call with a Single Cash Dividend"
text18 = """
  This page prices an American call with a single cash dividend prior
  to the option's maturity by assuning that the underlying asset price, when stripped of the dividend value, has a
  lognormal distribution as in the Black-Scholes model.  The optimal exericse time is either just before the asset
  goes ex-dividend or at the option's maturity.
  """
title19 = "General Black-Scholes Formula"
text19 = """
  Calls and puts are special cases of exchange options.  This page illustrates the
  version of the Black-Scholes formula that applies to exchange options (the Margrabe formula).  The only inputs, which
  are specified by the user, are the present value of the option to be delivered, the present value of the option to
  be received, the time to maturity, and the volatility of the ratio of values.  
   """

name = "futures-otions-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4, title5, title6, title7, title8, title9, title10,
    title11, title12, title13, title14, title15, title16, title17, title18, title19
]
texts = [
    text1, text2, text3, text4, text5, text6, text7, text8, text9, text10,
    text11, text12, text13, text14, text15, text16, text17, text18, text19
]
body = Overview(titles, texts)

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

