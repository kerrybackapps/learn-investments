from pages.formatting import Layout, Overview

title = "Overview: Risk and return"
runtitle = None
chapter = "Risk and Return"
chapter_url = "risk"

urls = {"Python notebook": None}
text = """
    This section provides an introduction to the properties of stock market returns and also bond and gold
    returns.  On most pages, the user
    can select the returns to be studied: either stock market returns downloaded from Ken French's data library
    of stock or ETF returns calculated from adjusted closing prices downloaded from Yahoo Finance.   The pages 
    are described below, and links to the pages are provided in the navigation bar above and on the 
    drop-down menu at the top right of each page.
    """
title1 = "Stock Market Returns"
text1 = """
    Historical annual returns for either the U.S. stock market (from Ken French's data library) or 
    a user-supplied ticker (dusing data from Yahoo Finance) are described in various ways: a boxplot, histogram, 
    line chart, accumulation plots, and a table of statistics (mean, standard deviation, and percentiles).
    """
title2 = "Returns at Different Frequencies"
text2 = """
    Historical daily, monthly, and annual returns for either t
    the U.S. stock market (from Ken French's data library) or 
    a user-supplied ticker (using data from Yahoo Finance) are described.  
    """
title3 = "Time Varying Volatilities"
text3 = """
    The volatility of daily returns (either of the U.S. stock market from 
    Ken French's data library or a user-supplied ticker using data from Yahoo Finance) is computed on a monthly 
    basis.  The page illustrates that volatility varies widely and is somewhat persistent but does not predict
    the subsequent month's return.
    """
title4 = "Geometric Average Returns"
text4 = """
    The page illustrates the difference between arithmetic and geometric average
    returns by computing both and showing the difference between compounding at the arithmetic average return
    and compounding at the geometric average return.  The calculations are either for the U.S. stock market return
    (obtained from Ken French's data library) or for a user-supplied ticker (using data from 
    Yahoo Finance).
    """
title5 = "Best and Worst Periods"
text5 = """
    The page examines returns over a period of either 5, 10, 20, or 30 years (selected
    by the user).  It shows the annual returns within the best and worst n-year periods, and it shows how much
    variation there has been in n-year geometric average returns.  The calculations are either for the U.S. 
    stock market return (obtained from Ken French's data library) or for a user-supplied 
    ticker (using data from Yahoo Finance).
    """
title6 = "Continuously Compounded Returns"
text6 = """
    The relationship between returns and continuously compounded returns is 
    explained graphically and via a tabulation of the distributions for the U.S. stock market (using data from
    Ken French's data library) or for a user-supplied ticker (using data from Yahoo Finance).
    """
title7 = "Simulating Returns"
text7 = """
    Geometric and arithmetic averages are compared for returns simulated from a normal
    distribution.  The user chooses the mean and standard deviation of the normal distribution and the length
    of the time period over which returns are simulated.
    """
title8 = "Skewness of Long-Run Returns"
text8 = """
    The page uses simulation to illustrate that compounding normally distributed
    returns produces a long-run return that is positively skewed with a heavy right tail.  Two different distributions
    are simulated (with parameters selected by the user) to illustrate, for example, that compounding two
    normally distributed returns with the same mean and different standard deviations produces 
    two long-run returns with different medians.
    """
title9 = "Stock, Bond, and Gold Returns"
text9 = """
    The statistics and plots provided for the U.S. stock market or individual
    tickers on the "Stock Market Returns" page are reproduced for stock, Treasury bond, corporate bond, and gold 
    returns.  The stock and bond returns are from Aswath Damodaran's website."""
title10 = "Inflation and Returns"
text10 = """
    Correlations with inflation are calculated for nominal stock, Treasury
    bond, corporate bond, gold, and Treasury bill returns.  Scatter plots of the relationships are also 
    presented.  The user selects the date range over which to compute the correlations and produce the scatter
    plots.  The stock, bond, and T-bill returns are from Aswath Damodaran's website.
    """
title11 = "Real Stock, Bond, and Gold Returns"
text11 = """
    Statistics and plots like those on the "Stock Market Returns" and "Stock, 
    Bond, and Gold Returns" pages are shown for inflation-adjusted stock, bond, and gold returns.
    """
title12 = "Correlations of Stocks or Funds"
text12 = """
    Correlations are an important consideration for portfolio
    optimization.  This page displays correlations of monthly returns for user-supplied tickers, using data
    from Yahoo Finance.
    """

name = "risk-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4, title5, title6, title7, title8, title9, title10, title11, title12
]
texts = [
    text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12
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


