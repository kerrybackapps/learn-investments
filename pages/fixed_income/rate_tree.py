import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.formatting import (
    mybadge,
    Layout,
    style_header,
    gray200,
    css_no_header,
    style_editable,
    Slider,
    text_style,
    lightblue
)
from pages.fixed_income.rate_tree_figtbl import figtbl


title = "Interest rate trees"
chapter = "Fixed Income"
chapter_url = "fixed-income"
urls = None
runtitle = None
name = 'rate-tree'

text = """ 
    A tree is generated for the annualized short rate.  The annualized short 
    rate is the rate $r$ such that the price of a zero-coupon
    bond with face value of 100 maturing at the end of 
    a single period is $100 / (1+r/n)$ where $n$ is the number of periods in
    a year.  The change in the annualized short rate from one period to the next is assumed to be 
    $a_t \pm \sigma\sqrt{\\Delta t}$ where $\sigma$ is the volatility that is input, $\\Delta t = 1/n$ is the length
    of a period in years, and $a_t$ is a number determined by
    the bond data that is input.  The bond data is used to compute spot and forward rates as on the Spot and Forward
    Rates page, except that here the compounding frequency for spot and forward rates is the number of periods in a
    year, which can be more than two.  It is still assumed that all bonds
    pay coupons semi-annually.  The numbers $a_t$ are chosen so that the model fits the spot and 
    forward rates.  What this means
    and how it is done is explained in 'Valuing a Zero-Coupon Bond' at the bottom of the page.  This model is called
    the Ho-Lee model.
    """

Params = DataTable(
    id=name + 'params',
    columns=[
        {"name": "col1", "id": name+"col1"},
        {"name": "col2", "id": name+"col2", "editable": True, "type": "numeric"},
    ],
    data=[
        {name+"col1": "Volatility (bp per year)", name+"col2": 50},
        {name+"col1": "Periods per year (even number)", name+"col2": 2},
        {name+"col1": "Number of bonds (integer)", name+"col2": 6}
        ],
    css=css_no_header,
    style_cell_conditional=[
        {
            'if': {'column_id': name+"col1"},
            'textAlign': 'left',
            'backgroundColor': gray200,
        },
        {
            'if': {'column_id': name+"col2"},
            'backgroundColor': lightblue,
        },
    ],
)

Bonds = DataTable(
    id=name + 'bonds',
    columns=[
        {"name": "Maturity", "id": name+"maturity", "editable": True},
        {"name": "Coupon (%)", "id": name+"coupon", "editable": True, "type": "numeric"},
        {"name": "Yield (%)", "id": name+"yld", "editable": True, "type": "numeric"},
    ],
    data=[
        {name+"maturity": 1, name+"coupon": 2, name+"yld": 1.5},
        {name+"maturity": 2, name+"coupon":  2, name+"yld": 2},
        {name+"maturity": 3, name+"coupon":  2, name+"yld": 2.25},
        {name+"maturity": 4, name+"coupon":  2, name+"yld": 2.4},
        {name+"maturity": 5, name+"coupon":  2, name+"yld": 2.5},
        {name+"maturity": 6, name+"coupon":  2, name+"yld": 2.6},
        ],
    style_header=style_header,
    style_data=style_editable,
)

fig = dcc.Graph(id=name+"fig")

label1 = dbc.Label("Enter parameters")
label2 = dbc.Label("Enter bond data")
left = dbc.Col([
    label1,
    Params
    ], md=3
)

mid = dbc.Col([label2, Bonds], md=3)
right = dbc.Col(fig, md=6)
row = dbc.Row([left, mid, right], align="top")

badge = mybadge("Valuing a Zero-Coupon Bond")
badge = dbc.Col(badge, width={"size": 2, "offset": 5})
badge = dbc.Row(badge)

text2 = """
    The figure below is of a zero-coupon bond with face value of 100 dollars valued
    using the short rate tree.  At each node, the value
    of the bond is computed by using the short rate $r$ at that node and computing $[(1/2)P_1 + (1/2)P_2] / (1+r/n)$
    where $P_1$ and $P_2$ are the bond prices at the two successor nodes and $n$ is the number of 
    periods in a year.  We apply this calculation by starting at the end of the tree with a price of $100 and working
    backwards.  Notice that the ordering of
    values on the y-axis is reversed - bond prices are lower when interest rates are higher.  The maturity of the bond
    cannot exceed (number of periods in the interest rate tree + 1) / (number of periods in a year).  
    
    The zero-coupon bond price determines the spot rate for that maturity.  The numbers $a_t$ mentioned above regarding
    the short rate tree are determined by the condition that, for all maturities,
    the spot rate calculated from the short rate tree as described here equals the spot
    rate calculated from the bond data.
    """

text2 = html.Div(dcc.Markdown(text2, mathjax=True), style={"background-color": gray200})


slider = Slider(
    "Maturity of zero-coupon bond", mn=0, mx=30, step=0.5, value=5, tick=None, kind="tip", name=name+"maturity"
)
slider = dbc.Col(slider, width=dict(size=4, offset=1))

fig = dcc.Graph(name+"example")

priceresult = html.Div(id=name+"price", style=text_style)
rateresult = html.Div(id=name+"rate", style=text_style)
pricetext = html.Div("Date-0 bond price")
ratetext = html.Div("Spot rate")
col1 = dbc.Col([pricetext, html.Br(), ratetext], width=dict(size=2, offset=2))
col2 = dbc.Col([priceresult, html.Br(), rateresult], md=2)
row2 = dbc.Row([slider, col1, col2], align="center")



body = html.Div([row, html.Hr(), badge, html.Br(), text2, html.Br(), row2, html.Br(), fig])
layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

@callback(
    Output(name+"params", "data"),
    Output(name+"bonds", "data"),
    Output(name+"fig", "figure"),
    Output(name+"example", "figure"),
    Output(name+"price", "children"),
    Output(name+"rate", "children"),
    Input(name+"maturity", "value"),
    Input(name+"params", "data_timestamp"),
    Input(name+"bonds", "data_timestamp"),
    State(name+"params", "data"),
    State(name+"bonds", "data")
)
def call(zerom, time1, time2, params, rows):
    return figtbl(name, zerom, params, rows)
