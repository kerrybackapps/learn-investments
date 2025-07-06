
from pages.formatting import Layout, Overview

title = "Overview: Capital Asset Pricing Model"
runtitle = None
chapter = "Capital Asset Pricing Model"
chapter_url = "capm"

urls = {"Python notebook": None}
text = """
This section explains the formula for asset expected returns known as the Capital Asset Pricing Model (CAPM), which
was derived by Sharpe, Mossin, Lintner, and Treynor.  The pages in this section illustrate the CAPM regression,
calculate the CAPM-implied cost of equity for a ticker chosen by the user, 
discuss issues in estimating the market risk premium (a key input to the CAPM), and provide some empirical evidence
about the CAPM.  The pages are described below, and links to the pages are provided in
the navigation bar above and on the drop-down menu at the top right of each page.
"""

title1 = "Alphas and Betas"
text1 = """
  Monthly excess returns for a user-input ticker are regressed on US stock market 
  excess returns.  The alpha and beta are reported.  The best fit line and a scatterplot of the excess returns 
  relative to market excess returns are plotted.  The sample is the last sixty months.
  """
title2 = "Alphas and Mean-Variance Efficiency"
text2 = """
  Alpha is the intercept from a regression of excess returns on 
  benchmark excess returns.  Adding an asset with positive alpha to the benchmark results in an improvement in 
  mean-variance efficiency.  This page illustrates this concept graphically by plotting the tangency portfolio 
  consisting of a benchmark and an asset.  The user can input the asset's alpha as well as other characteristics 
  of the asset, benchmark, and risk-free returns.
  """
title3 = "Alphas and Sharpe Ratios"
text3 = """
  An asset's alpha with respect to a benchmark is positive if and only if the 
  asset's Sharpe ratio is higher than the benchmark's Sharpe ratio multipled by the correlation between the asset a
  nd benchmark returns.  This page illustrates this concept graphically by plotting (1) the tangency portfolio 
  consisting of a benchmark and an asset, and (2) the asset relative to a line with slope equal to the benchmark's 
  Sharpe ratio multiplied by the correlation and y-intercept equal to the risk-free rate.
  """
title4 = "CAPM Cost of Equity Calculator"
text4 = """
  A CAPM-based cost of equity consists of estimates of the risk-free rate, 
  a stock's beta relative to the market, and the market risk premium.  This page calculates a CAPM-based cost of 
  equity for a user-supplied ticker and plots the regression of the stock's excess return on the market excess 
  return, using data from Ken French's data library, Yahoo Finance, and Federal Reserve Economic Data. 
  """
title5 = "Estimating the Market Risk Premium"
text5 = """
  The market risk premium is often estimated as a sample average of 
  historical excess market returns.  This page shows the variability in estimating the market risk premium using 
  historical data (from Ken French's data library).  It shows the range of possible market risk premium 
  estimates as a function of the number of 
  years of monthly data used in the estimation.
  """
title6 = "Security Market Line for Industry Returns"
text6 = """
  The security market line (SML) is the relation between asset 
  risk premia and CAPM betas.  Theoretically, the slope of the SML is the market risk premium.  This page plots 
  the empirical SML for the Fama-French 48 industry portfolios compared to the theoretical SML for a user-specified sample 
  period, using data from Ken French's data library.  Empirically, the SML has generally been flatter 
  than implied by the CAPM (or even inverted).
  """
title7 = "CAPM for Two-Way Sorts"
text7 = """
  According to the CAPM, alphas obtained from portfolio excess returns regressed on market 
  excess returns should be zero, so large $t$ statistics for alpha (of either sign) reject CAPM.  This page 
  reports CAPM alphas and their $t$ statistics for portfolios of stocks sorted into quintiles on market equity 
  and another user-specified characteristic.  The portfolio returns and market excess return are from Ken
  French's data library.  The user can control the date range of the analysis.
   """

name = "capm-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4, title5, title6, title7,
]
texts = [
    text1, text2, text3, text4, text5, text6, text7,
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



