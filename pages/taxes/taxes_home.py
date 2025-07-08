from pages.formatting import Layout, Overview

title = "Overview: Funds and taxes"
runtitle = None
chapter = "Funds and Taxes"
chapter_url = "topics"

urls = {"Python notebook": None}
text = """
    This section covers performance evaluation of mutual funds and the tax implications of different
    investment accounts and asset locations. The pages examine market timing ability, factor models
    for performance evaluation, and optimal asset location strategies considering tax effects.
    The pages are described below, and links to the pages are provided in the navigation bar above 
    and on the drop-down menu at the top right of each page.
    """

title1 = "Marginal and Effective Tax Rates"
text1 = """
    Calculate marginal and effective tax rates for different income levels and filing statuses.
    Uses current U.S. tax brackets to show how progressive taxation affects different income levels
    and demonstrates the difference between marginal and effective tax rates.
    """

title2 = "Tax-Advantaged Savings Vehicles"
text2 = """
    Compare the after-tax values of investments in different account types including brokerage accounts,
    traditional 401(k)s, Roth IRAs, and non-deductible IRAs. Shows how tax treatment affects long-term
    wealth accumulation under different tax rate scenarios.
    """

title3 = "Asset Location with Taxes"
text3 = """
    Analyze optimal asset location strategies for portfolios containing stocks and bonds across
    different account types (brokerage, 401(k), Roth IRA). Shows how tax characteristics of different
    assets should influence their placement in tax-advantaged vs. taxable accounts.
    """

title4 = "Comparison of Asset Locations with Taxes"
text4 = """
    Compare multiple asset location strategies side-by-side to determine optimal allocation
    across account types. Allows detailed analysis of how different portfolio allocations
    affect after-tax wealth under various tax scenarios.
    """

name = "taxes-home"

import dash_bootstrap_components as dbc
from dash import html

titles = [
    title1, title2, title3, title4
]
texts = [
    text1, text2, text3, text4
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

