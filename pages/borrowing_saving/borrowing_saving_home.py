from pages.formatting import Layout, Overview


title = "Overview: Time value of money"
runtitle = None
chapter = "Time Value of Money"
chapter_url = "borrowing-saving"
urls = {"Python notebook": None}
text = """
    This section covers the basics of valuation - discounting cash flows - and the implications for
    loan terms.  It also conducts a retirement planning exercise and explains the difference between
    real and nominal returns.   The pages are described below, and links to the pages are provided in
    the navigation bar above and on the drop-down menu at the top right of each page.
    """
title1 = "Net Present Value"
text1 = """
      Net present values (NPVs) are calculated as sums of present value factors 
      multiplied by cash flows in 
      a tabular framework.  The user can input the discount rate, number of periods, and the cash flows.
      """
title2 = "Internal Rate of Return"
text2 = """
      The internal rate of return (IRR) is explained graphically as the discount rate that
      makes the net present value equal to zero.  The user can input the number of periods and the cash flows.
      """
title3 = "Two-Stage Valuation Model"
text3 = """
      The present value is calculated of a project that has a first stage of cash flows
      input by the user and a second stage that grows perpetually at a rate input by the user.  The present value is
      broken down into the present value of the first stage and the value at the end of the first stage of the
      perpetual cash flows (terminal value) which is then discounted to the project initiation.
      """
title4 = "Amortization"
text4 = """
      Four loan parameters are calculated, each given the other three (input by 
      the user): the loan payment,
      the amount that can be borrowed, the balloon payment at the end, and the interest rate that makes the 
      payments sufficient to retire the loan.
      """
title5 = "Amortization Schedule"
text5 = """
      The remaining loan payoff and the fractions of each payment that go towards 
      interest and towards principal are illustrated graphically.  The user inputs the loan parameters.
      """
title6 = "Retirement Planning"
text6 = """
      The feasibility of a retirement plan is analyzed assuming a constant rate of return
      on the retirement account.  The user inputs the number of years to retirement, the number of years the
      account will need to support the planner during retirement, the initial monthly savings, the rate at which
      savings are anticipated to grow before retirement, the rate of return on the retirement account, and the
      planned monthly withdrawal post-retirement.  The account balance is plotted.
      """
title7 = "Retirement Planning Simulation"
text7 = """
      This builds on the retirement planning page by assuming random returns on
      the retirement account.  The user inputs the expected return and risk (standard deviation) of the returns.  The 
      probability distribution of the ending account balance is shown and is plotted.
      """
title8 = "Inflation and Real Returns"
text8 = """
      Historical U.S. inflation rates are downloaded from the web and plotted.  Based 
      on an assumed constant nominal rate of return (input by the user), the cumulative nominal and real (constant dollar)
      returns are calculated and plotted, based on the historical U.S. inflation rates.
      """
name = "borrowing-saving-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4, title5, title6, title7, title8
]
texts = [
    text1, text2, text3, text4, text5, text6, text7, text8,
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

