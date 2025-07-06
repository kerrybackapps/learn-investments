from pages.formatting import Layout, Overview

title = "Overview: Portfolios"
runtitle = None
chapter = "Portfolios"
chapter_url = "portfolios"

urls = {"Python notebook": None}
text = """
    This section explains mean-variance optimal portfolios with or without short sales constraints and with or
    without different borrowing and saving rates.  Most of the pages use inputs selected by the user, but some of the
    final pages allow the user to select stocks or ETFs, and returns are calculated from adjusted closing prices
    downloaded from Yahoo Finance.  The pages are described below, and links to the pages are provided in
    the navigation bar above and on the drop-down menu at the top right of each page.
    """
title1 = "Two Risky Assets"
text1 = """
       Expected returns and standard deviations of portfolios of two assets are 
       plotted.  The portfolio weights are all nonnegative (there are no short positions).  The user inputs 
       the expected returns and standard deviations of each asset and the correlation between the assets.
       """
title2 = "Three Risky Assets"
text2 = """
       Expected returns and standard deviations of portfolios of three assets 
       are plotted.  The portfolio weights are all nonnegative (there are no short positions).  The user inputs 
       the expected returns and standard deviations of each asset and the correlations between the assets. 
       """
title3 = "Diversification"
text3 = """
       Combining multiple assets in a portfolio can reduce overall portfolio 
       risk.  This page illustrates how the standard deviation of an equally weighted portfolio of 
       assets declines as the number of assets in the portfolio increases.  The assets are assumed to have the 
       same standard 
       deviation and to have the same correlation with each other.  The user inputs the common standard 
       deviation and correlation.  
       """
title4 = "Short Sales"
text4 = """
       This extends the "two risky assets" page by allowing for short sales as negative 
       portfolio weights.  Allowing short sales extends the curve of possible portfolio risk/mean combinations.
       * **Frontier portfolios** The minimum risk portfolio of three assets for each expected return is 
       calculated, assuming short selling is unconstrained.  The Global Minimum Variance portfolio is also
       computed.  The user inputs the expected returns and 
       standard deviations of each asset and the correlations between the assets.
       """
title5 = "Risk-Free Asset"
text5 = """
       A risky asset can be combined with risk-free saving or borrowing.  This page 
       plots expected returns and standard deviations of such portfolios.  The user inputs the 
       expected return and standard deviation of the risky asset as well as the risk-free savings rate and 
       the excess of the risk-free borrowing rate over the savings rate.
       """
title6 = "Sharpe Ratios"
text6 = """
       The Sharpe ratio of a risky asset or portfolio is the ratio of its risk premium 
       to its standard deviation.  The Sharpe ratio is the slope of the capital allocation line.  The user can 
       see how changing portfolio weights for three assets changes the portfolio's Sharpe ratio and distance 
       from the frontier.
       """
title7 = "Tangency Portfolio"
text7 = """
       The portfolio of assets with the highest attainable Sharpe ratio is called 
       the tangency portfolio.  This page plots the tangency portfolio for three assets.  The user inputs 
       the expected returns and standard deviations of each asset, the correlations between the assets, and 
       the risk-free rate.
       """
title8 = "Preferences"
text8 = """
       Investors typically like higher expected returns with less risk. This 
       page plots mean-variance indifference curves, that is, risk-return combinations among which a mean variance 
       investor is indifferent.  The investor's utility is modeled as expected return minus a penalty for variance,
       and the user inputs the penalty parameter (risk aversion) along with asset parameters.
       """
title9 = "Optimal Capital Allocation"
text9 = """
       The optimal portfolio of a set of risky assets that can be shorted 
       frictionlessly and a risk-free asset that can be frictionlessly borrowed and lent is a combination of 
       the risk-free asset and a tangency portfolio.  The particular combination depends on an investor's 
       preferences.  This page shows this optimal portfolio, the capital allocation line, the tangency portfolio, 
       and the frontier.
       """
title10 = "Optimal Capital Allocation with Different Rates"
text10 = """
       Borrowing rates are usually higher than savings 
       rates.  This page incorporates this friction into the optimal capital allocation problem.  The optimal 
       portfolio is plotted in risk-expected return space, and the optimal allocation to risky assets is plotted as a function 
       of risk aversion.
       """
title11 = "Effect of Short-Sales Constraints"
text11 = """
       Short selling may be restricted in practice for various 
       reasons.  This page compares the efficient frontiers for a three asset portfolio if shorting is allowed 
       to that when shorting is not allowed.  
       """
title12 = "Optimal Portfolios with More Assets"
text12 = """
       This page calculates the frontier, tangency portfolio(s), and 
       optimal portfolio allocations based on user-input means, standard deviations, and correlations and 
       user-selected interest rates for up to eight assets.  The user can 
       also specify whether the borrowing and savings rates differ and whether or not short-sales are allowed.
       """
title13 = "Optimal Portfolios of Stocks, Bonds, and Gold"
text13 = """
       Optimal portfolios of the S&P 500, gold, corporate
       bonds and Treasury bonds are calculated, using historical returns to estimate the expected returns, 
       standard deviations, and correlations.  The stock and bond returns are from Aswath Damodaran's 
       website. Various levels of risk aversion are considered. Saving and 
       borrowing are allowed, at possibly different rates, and short sales can be allowed.
       """
title14 = "Optimal Portfolios of Stocks or Funds"
text14 = """
       Optimal portfolios of user-specified tickers are 
       calculated, using historical returns (calculated from adjusted closing prices provided by Yahoo Finance)
       to estimate the expected returns, standard deviations, and 
       correlations, for investors with various levels of risk aversion. Saving and borrowing are allowed, at 
       possibly different rates, and short sales can be allowed.  
       """

name = "portfolios-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4, title5, title6, title7, title8,
    title9, title10, title11, title12, title13, title14
]
texts = [
    text1, text2, text3, text4, text5, text6, text7, text8,
    text9, text10, text11, text12, text13, text14
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



