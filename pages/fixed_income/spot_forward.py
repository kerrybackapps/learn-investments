import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.formatting import Layout, largefig, style_header, myinput, style_editable
from pages.fixed_income.spot_forward_figtbl import figtbl


title = "Spot and forward rates"
chapter = "Fixed Income"
chapter_url = "fixed-income"
urls = None
runtitle = None
name = 'spot-forward'

text = """ 
    Spot and forward rates are computed to match the bond data that is entered.  Spot rates are yields of hypothetical
    zero-coupon bonds.  Coupon bonds can be viewed as portfolios of zero-coupon bonds, so spot rates determine prices
    and yields of coupon bonds.  Spot rates are computed to match as closely as possible 
    the yields of coupon (or zero-coupon) bonds entered and so that the implied forward rates vary smoothly 
    over time.  Yields, spot rates, and forward rates
    are computed with semi-annual compounding (each is twice a semi-annual rate) and for simplicity it
    is assumed that all bonds have maturities that are an integer number of half years.  Forward rates $f_i$ for each
    six-month period are defined by the equations $(1+f_1/2)(1+f_2/2) \cdots (1+f_n/2) = (1+s_n/2)^n$, 
    for $n=1, 2, \ldots$, where $s_n$ is
    the spot rate for a maturity of $n/2$ years.  Forward rates are the rates that could be locked in for 
    forward loans by trading
    the hypothetical zero-coupon bonds.   There are many different ways to compute spot rates to satisfy the criteria
    of closely matching bond data and producing smooth variation of spot and forward rates over time.  This page just 
    provides one example, though all such methods should give very similar results.
    """

Num = myinput(id=name+"num", value=5)

Bonds = DataTable(
    id=name + 'bonds',
    columns=[
        {"name": "Maturity", "id": name+"maturity", "editable": True},
        {"name": "Coupon (%)", "id": name+"coupon", "editable": True, "type": "numeric"},
        {"name": "Yield (%)", "id": name+"yld", "editable": True, "type": "numeric"},
    ],
    data=[
        {name+"maturity": 2, name+"coupon": 4, name+"yld": 2},
        {name+"maturity": 4, name+"coupon":  4, name+"yld": 3},
        {name+"maturity": 6, name+"coupon":  4, name+"yld": 4},
        {name+"maturity": 8, name+"coupon":  4, name+"yld": 5},
        {name+"maturity": 10, name+"coupon":  4, name+"yld": 6},
        ],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

fig = dcc.Graph(id=name+"fig")

label1 = dbc.Label("Enter number of bonds")
label2 = dbc.Label("Enter bond data")
left = dbc.Col([label1, Num, html.Br(), label2, Bonds], xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col(fig, xs=12, sm=12, md=8, lg=8, className="mb-2")
body = dbc.Container(dbc.Row([left, right], align="top", className="gx-1"), fluid=True, className="px-1")

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
    Output(name+"bonds", "data"),
    Output(name+"fig", "figure"),
    Input(name+"num", "value"),
    Input(name+"bonds", "data_timestamp"),
    State(name+"bonds", "data")
)
def call(num, time, rows):
    return figtbl(name, num, rows)
