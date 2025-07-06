from pages.formatting import Layout, Overview

title = "Overview: Sorts and factors"
runtitle = None
chapter = "Sorts and Factors"
chapter_url = "factor-investing"

urls = {"Python notebook": None}
text = """
Asset pricing models attempt to explain expected returns in terms of covariances with
systematic risk factors.  Factors are frequently constructed as long-minus-short returns
of portfolios formed from sorts on firm characteristics.  This section presents some evidence about the
returns of portfolios formed from sorts.  It also explains calculating a firm's cost of equity
from the Fama-French model, which is a
popular model of this type and which generalizes the CAPM.  Some empirical evidence is also presented about
the Fama-French model.  The pages are described below, and links to the pages are provided in
the navigation bar above and on the drop-down menu at the top right of each page.
"""

title1 = "Sorts on Characteristics"
text1 = """
  Stocks are grouped into quintile portfolios by sorting on a user-selected 
  firm characteristic.  This page reports return characteristics of the quintile portfolios.  The portfolio
  returns are
  from Ken French's data library.
  """
title2 = "Two-Way Sorts"
text2 = """
  Stocks are independently sorted into quintiles on market equity and another user-specified 
  characteristic.  This page reports mean excess returns and Sharpe ratios for the resulting 25 
  portfolios.  The portfolio returns and risk-free rates are from Ken French's data library.
  """
title3 = "Fama-French Cost of Equity Calculator"
text3 = """
  A Fama-French-based cost of equity is determined by estimates of 
  the risk-free rate, a stock's betas relative to the Fama-French factors, and the factor risk premia.  This page 
  calculates a Fama-French-based cost of equity for a user-selected ticker.  Monthly stock returns are computed
  from data provided by Yahoo Finance, the current risk-free rate is from Federal Reserve Economic Data, and 
  the other data is from Ken French's data library.
  """
title4 = "Fama-French Model for Two-Way Sorts"
text4 = """
  This page reports Fama-French alphas and their t statistics for 
  portfolios of stocks sorted into quintiles on market equity and another user-specified characteristic.  The user 
  can control the date range of the analysis.  The portfolio returns and Fama-French factors are from Ken 
  French's data library.
  """

name = "factor-investing-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4,
]
texts = [
    text1, text2, text3, text4,
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


