from pages.formatting import Layout, Overview

title = "Overview: Funds and taxes"
runtitle = None
chapter = "Topics"
chapter_url = 'topics'

urls = {"Python notebook": None}
text = """
This section covers two topics: mutual fund performance evaluation, and the effects of taxes on
various types of savings vehicles.  The pages are described below, and links to the pages are provided in
the navigation bar above and on the drop-down menu at the top right of each page.
"""

title1 = "Evaluation of Mutual Funds"
text1 = """
  Fund returns are compared to benchmark returns to assess active 
  performance.  Three tabs allow the user to consider an excess return over a benchmark, a beta-adjusted 
  benchmark, or a multi-factor benchmark.  The user can select the ticker to analyze, the benchmark, and a date range.
  """
title2 = "Market Timing"
text2 = """
  Funds exhibit market timing ability when their returns are convex in the market return. Fund returns are 
  simulated under the Henriksson-Merton market timing model.  Users can input the alpha, beta, and 
  gamma for the data-generating process and visualize positive and negative market timing.
  """
title3 = "Marginal and Effective Tax Rates"
text3 = """
  Total tax due and the marginal and effective tax rates are calculated for a user-input taxable 
  income.  Marginal and effective tax rates are plotted as a function of income.
  """
title4 = "Tax-Advantaged Savings Vehicles"
text4 = """
  Tax treatment of savings vehicles can substantially affect after-tax 
  returns.  Future after-tax values of investments in various tax-advantaged vehicles are calculated.  The user 
  can input the annual rate of return, initial and ending tax rates, and number of years of savings.  Account 
  balances over time are plotted.
  """
title5 = "Asset Location with Taxes"
text5 = """
  If multiple tax-advantaged accounts are available to an investor, the choice 
  of where to locate different asset classes can impact performance.  The user inputs portfolio allocations for a 
  dividend-paying stock and/or taxable coupon bond in a brokerage account, a 401(k) account, and/or a Roth IRA 
  account.  Accumulated balances in each account are plotted. 
  """
title6 = "Comparison of Asset Locations with Taxes"
text6 = """
  Future after-tax balances are calculated for three distinct 
  portfolio allocations of a dividend-paying stock and/or taxable coupon bond to a brokerage account, a 401(k) 
  account, and/or a Roth IRA account.  
   """

name = "performance-evaluation-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4, title5, title6
]
texts = [
    text1, text2, text3, text4, text5, text6
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


