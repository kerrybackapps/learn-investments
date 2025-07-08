import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    mybadge,
    style_header,
    style_data_conditional,
    css_no_header,
    ricegrey,
    gray200,
    Slider,
    text_style,
    lightblue,
    style_editable
)
from pages.fixed_income.embedded_option_figtbl import figtbl


title = "Option adjusted spreads"
chapter = "Fixed Income"
chapter_url = "fixed-income"
urls = None
runtitle = None
name = 'oas'

text = """ 
    A tree is generated for the annualized short rate as on the "Interest Rate Trees" page.  At the bottom of this page,
    the tree is used in conjunction with inputs regarding a bond with an embedded option to compute the option
    adjusted spread (OAS) of the bond.  It is assumed that all bonds pay coupons semi-annually.
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
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
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
        {name+"maturity": 2, name+"coupon": 2, name+"yld": 2},
        {name+"maturity": 3, name+"coupon": 2, name+"yld": 2.25},
        {name+"maturity": 4, name+"coupon": 2, name+"yld": 2.4},
        {name+"maturity": 5, name+"coupon": 2, name+"yld": 2.5},
        {name+"maturity": 6, name+"coupon": 2, name+"yld": 2.6},
        ],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)

rateTree = dcc.Graph(id=name+"ratetree")

label1 = dbc.Label("Enter parameters")
label2 = dbc.Label("Enter bond data")
left = dbc.Col([
    label1,
    Params
    ], xs=12, sm=12, md=3, lg=3, className="mb-2"
)

mid = dbc.Col([label2, Bonds], xs=12, sm=12, md=3, lg=3, className="mb-2")
right = dbc.Col(rateTree, xs=12, sm=12, md=6, lg=6, className="mb-2")
toprow = dbc.Row([left, mid, right], align="top", className="gx-1")

badge = mybadge("Calculating Option-Adjusted Spread")
badge = dbc.Col(badge, width={"size": 2}, className="offset-md-5")
badge = dbc.Row(badge)

text2 = """
    A puttable bond should be put back to the company whenever its market price falls to the put price (strike), and
    a callable bond should be called by the company whenever its market price rises to the call price.  We can value 
    puttable and callable bonds from an interest rate tree by computing the expected 
    discounted value at each node and replacing that value by the option strike whenever exercise is optimal.  The
    interest rate trees we consider are the short rate tree at the top of the page plus a constant spread.  The spread
    that implies a bond value equal to the market price of the bond is called the option adjusted spread.  Input the
    bond parameters and its market price in the table to the right.  The market price must be lower than the strike for
    a callable bond, and it must be higher than the strike for a puttable bond; otherwise, the bond would have already
    been called or put.  Notice that the ordering of the bond prices on the y axes in the figures below is reversed,
    because bond prices are lower when interest rates are higher.
    """

text2 = html.Div(dcc.Markdown(text2, mathjax=True), style={"background-color": gray200})

OASParams = DataTable(
    id=name + 'oasparams',
    columns=[
        {"name": "oascol1", "id": name+"oascol1"},
        {"name": "oascol2", "id": name+"oascol2", "editable": True, "type": "numeric"},
    ],
    data=[
        {name+"oascol1": "Corporate bond coupon rate (%)", name+"oascol2": 5},
        {name+"oascol1": "Corporate bond maturity (# periods)", name+"oascol2": 10},
        {name+"oascol1": "Option type (1 for call, 2 for put)", name+"oascol2": 2},
        {name+"oascol1": "Call or put strike price", name+"oascol2": 100},
        {name+"oascol1": "Market price of corporate bond", name+"oascol2": 102},
        ],
    css=css_no_header,
    style_cell_conditional=[
        {
            'if': {'column_id': name+"oascol1"},
            'textAlign': 'left',
            'backgroundColor': gray200,
        },
        {
            'if': {'column_id': name+"oascol2"},
            'backgroundColor': lightblue,
        },
    ],
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)


OASTree = dcc.Graph(name+"oastree")
BondTree = dcc.Graph(name+"bondtree")
OptionTree = dcc.Graph(name+"optiontree")

OAStext = html.Div("Option-adjusted spread")
OASresult = html.Div(id=name+"oas", style=text_style)

col1 = dbc.Col(OAStext, xs=12, sm=6, md=6, lg=6, className="mb-2")
col2 = dbc.Col(OASresult, xs=12, sm=6, md=6, lg=6, className="mb-2")
row = dbc.Row([col1, col2], className="gx-1")
col1 = dbc.Col(text2, xs=12, sm=12, md=8, lg=8, className="mb-2")
col2 = dbc.Col([OASParams, html.Br(), row], xs=12, sm=12, md=4, lg=4, className="mb-2")
midrow = dbc.Row([col1, col2], align="center", className="gx-1")

cola = dbc.Col(OASTree, xs=12, sm=12, md=4, lg=4, className="mb-2")
colb = dbc.Col(BondTree, xs=12, sm=12, md=4, lg=4, className="mb-2")
colc = dbc.Col(OptionTree, xs=12, sm=12, md=4, lg=4, className="mb-2")
bottomrow = dbc.Row([cola, colb, colc], align="top", className="gx-1")

body = dbc.Container([toprow, html.Hr(), badge, html.Br(), midrow, html.Hr(), bottomrow], fluid=True, className="px-1")
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
    Output(name+"oasparams", "data"),
    Output(name+"ratetree", "figure"),
    Output(name+"oastree", "figure"),
    Output(name+"bondtree", "figure"),
    Output(name+"optiontree", "figure"),
    Output(name+"oas", "children"),
    Input(name+"params", "data_timestamp"),
    Input(name+"bonds", "data_timestamp"),
    Input(name+"oasparams", "data_timestamp"),
    State(name+"params", "data"),
    State(name+"bonds", "data"),
    State(name+"oasparams", "data"),
)
def call(time1, time2, time3, params, rows, oasparams):
    return figtbl(name, params, rows, oasparams)
