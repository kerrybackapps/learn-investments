from pages.formatting import Layout, Overview


title = "Overview: Fixed income"
runtitle = None
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = {"Python notebook": None}




text = """
This section introduces some basic concepts about bonds and interest rates.  It also presents a movie of the history of
the U.S. term structure of interest rates, an explanation of duration risk, and an illustration of the principal 
components of term structure movements.  This section also develops the Ho-Lee model for generating
a binomial tree for interest rate movements that matches the initial term structure and uses the model to compute
option adjusted spreads.  The pages are described below, and links to the pages are provided in
the navigation bar above and on the drop-down menu at the top right of each page.
"""

title1="Bond Prices and Yields"
text1="""
    The yield of a bond is the interest rate that equates the present value of its
    cash flows to its market price.  The price is above the face value if and only if the yield is below the
    coupon rate.  This page illustrates these relationships in tabular and graphical form.
    """
title2 = "Term Structure of Interest Rates"
text2 = """
    The term structure of interest rates is the relation between the time to 
    maturity of a bond and its yield.  The term structure changes over time.  This page presents an animation of the 
    history of the term structure of U.S. Treasury yields.
    """
title3 = "Credit Spreads"
text3 = """
    This page presents the history of U.S. corporate bond yields, for bonds of different
    credit ratings: BBB, A, AA, and AAA.
    """
title4 = "Treasury Inflation-Protected Securities"
text4 = """ 
    The coupons and face values of TIPS are indexed to inflation,
    so the yields at which they trade are real yields.  This page illustrates how the real and nominal payouts of
    both regular Treasury bonds and TIPS change with inflation.
    """
title5 = "Term Structure of Real Interest Rates"
text5 = """
    This page presents an animation of the history of real U.S. Treasury yields.
    """
title6 = "Clean and Dirty Bond Prices and Yields"
text6 = """
    Bond traders quote a "clean" price that does not include accrued
    interest since the last coupon payment.  The actual price paid in a transaction is the clean price plus accrued
    interest, which is called the "dirty" price. Discounting the cash flows at the bond yield produces the dirty
    price.  This page explains the relation between bond prices and yields in tabular and graphical form while 
    distinguishing between clean and dirty prices.
    """
title7 = "Hypothetical Clean and Dirty Price Paths"
text7 = """
    If a bond's yield remains constant over time, then its clean price
    is pulled smoothly to par, meaning that it increases smoothly over time to face value if trading at a discount
    and decreases smoothly over time to face value if trading at a premium.  Meanwhile the dirty price rises as a
    coupon date is approached and falls when the coupon is paid.  This page illustrates these facts graphically.
    """
title8 = "Duration"
text8 = """ 
    The present value of each cash flow of a bond can be calculated by discounting it at the bond's 
    yield.  The Macaulay duration of a bond is defined as a weighted average of the times to maturity of the separate
    cash flows, where the weight on each cash flow is the fraction of the total present value that the cash flow
    constitutes.  This page illustrates the calculation of Macaulay duration in tabular form.
    """
title9 = "Duration and Risk"
text9 = """ 
    Modified duration is defined as Macaulay duration divided by 1 plus the yield.  Given a
    small change in the yield, the percent change in the bond price is approximately minus modified duration multiplied
    by the change in the yield.  This page illustrates the relationship graphically.
    """
title10 = "Spot and Forward Rates"
text10 = """
   Given a collection of bonds of different maturities and/or coupons, the implied spot
    rates are the rates for different times to maturity such that all of the bonds are correctly priced by discounting
    the individual cash flows at the spot rate for tha time to maturity of the cash flow.  Forward rates are rates
    that can be locked in for forward loans by trading bonds of different maturities and/or coupons today.  This page
    graphically illustrates the relationships between bond yields, spot rates, and forward rates.
    """
title11 = "Interest Rate Trees"
text11 = """
    This page generates the Ho-Lee binomial tree for the short rate (spot rate at the 
    shortest maturity) and shows how the tree is calibrated from a volatility and bond parameters input by the user.
    """
title12 = "Option Adjusted Spreads"
text12 = """
    This page shows how to use the Ho-Lee tree to value a bond with an embedded option and
    how to compute the yield at which the bond would trade if it did not include the option, which is called the
    option-adjusted spread.
    """
title13 = "Term Structure Movements"
text13 = """
    This page presents statistics about the month-to-month changes in yields of
    U.S. Treasury bonds at different maturities: means, standard deviations, and correlations.
    """
title14 = "Principal Components"
text14 = """
    The principal components of month-to-month changes in U.S. Treasury yields are 
    calculated and plotted.  The first is a level change, the second is a slope change, and the third is a curvature
    change.
    """

name = "fixed-income-home"

titles = [
    title1, title2, title3, title4, title5, title6, title7, title8, title9, title10,
    title11, title12, title13, title14
]
texts = [
    text1, text2, text3, text4, text5, text6, text7, text8, text9, text10,
    text11, text12, text13, text14
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

