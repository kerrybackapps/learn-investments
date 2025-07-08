import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from pages.taxes.marginal_tax_rates_figtbl import figtbl
from pages.formatting import (
    Layout,
    Slider,
    myinput,
    text_style
)

title       = "Marginal and effective tax rates"
runtitle    = None
chapter     = "Topics"
chapter_url = "topics"
urls        = None
text = """
        In a progressive tax system, higher levels of income are taxed at progressively higher rates.  Each tax rate is applied to income that falls between lower and upper limits; that is, 
        within a tax bracket.  Within a given tax bracket, each additional dollar earned is taxed at the rate for that tax bracket. The total **tax due** is the sum across all tax brackets of the bracket's tax rate multiplied by the amount of taxable income falling in the tax bracket. A tax-payer's **effective** tax rate is their total tax paid as a fraction of their taxable income. A tax-payer's **marginal** tax rate is the tax rate that would apply to an incremental dollar earned above the tax-payer's total taxable income.  The calculations on this page use United States tax brackets and rates for income earned in 2023 (taxes due in 2024).
        """
name = "marginal-effective-tax-rates"


##### INPUTS
inputs = [name + "input" + str(i) for i in range(2)]

# slider = Slider(
#     "Taxable Income",
#     mn=1000,
#     mx=1000000,
#     step=1000,
#     value=50000,
#     tick=50000,
#     name=inputs[0],
#     kind=None,
# )
inpt1  = myinput(id=inputs[0], placeholder="Enter taxable income", value=50000)
label1 = "Enter taxable income"
radio = dcc.RadioItems(
    options=[
        {"value": "single", "label": "Single"},
        {"value": 'married filing jointly', "label": "Married filing jointly"},
        {"value": 'married filing separately', "label": "Married filing separately"},
        {"value": 'head of household', "label": "Head of household"},       
    ],
    value="single",
    inline=False,
    id=inputs[1],
    labelStyle={"display": "block"},
)

graph = dcc.Graph(id=name + "fig")


##### PAGE SETUP
# Radio button
left  = dbc.Col(dbc.Label("Filing status", html_for=inputs[1]), xs=6)
right = dbc.Col(radio, xs=6)
radio = dbc.Row([left, right], align="top")

# Total tax
tax_due = html.Div(id=name + "tax_due", style=text_style)
tax_dueLabel = dbc.Col(dbc.Label("Tax Due", html_for=name + "tax_due"), xs=6)
tax_due = dbc.Row([tax_dueLabel, dbc.Col(tax_due, xs=6)])

# Marginal rate
marginal = html.Div(id=name + "t_marginal", style=text_style)
marginalLabel = dbc.Col(dbc.Label("Marginal Rate", html_for=name + "t_marginal"), xs=6)
marginal = dbc.Row([marginalLabel, dbc.Col(marginal, xs=6)])

# Effective rate
effective = html.Div(id=name + "t_effective", style=text_style)
effectiveLabel = dbc.Col(dbc.Label("Effective Rate", html_for=name + "t_effective"), xs=6)
effective = dbc.Row([effectiveLabel, dbc.Col(effective, xs=6)])

col1 = dbc.Col([label1, inpt1, html.Br(), radio], xs=12, sm=12, md=6, lg=6, className="mb-2")
col2 = dbc.Col([tax_due, html.Br(), marginal,  html.Br(), effective], xs=12, sm=12, md=6, lg=6, className="mb-2")
row1 = dbc.Row([col1, col2], className="gx-1")

row2 = dbc.Row(dbc.Col(graph, xs=12, sm=12, md=12, lg=12, className="mb-2"), align="center", className="gx-1")

body = dbc.Container([row1, row2], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [
    Output(name + "fig", "figure"),
    Output(name + "tax_due", "children"),
    Output(name + "t_marginal", "children"),
    Output(name + "t_effective", "children"),
]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)
