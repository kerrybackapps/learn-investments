import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import FormatTemplate
from pages.formatting import Slider, Layout, text_style
from pages.borrowing_saving.amortization_schedules_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

title = "Amortization schedule"
runtitle = "Amortization Schedule"
chapter = "Borrowing and Saving"
chapter_url = "borrowing-saving"
urls = {"Python notebook": None}
text = """ A payoff is calculated at each date during the lifetime of a loan.  The payoff is 
              calculated at each date before the loan payment is made, so it includes the
              payment amount.  The schedule
              that relates the payoff to the date is called the amortization schedule.  If 'annual
              payments' is selected, it is assumed that there is a single payment each year, occurring
              at the end of each year.  If 'monthly payments' is selected, then the monthly rate used to
              calculate the payment and the amortization is the annual rate divided by 12. The
              figure on the left shows how much of each payment is interest and how much goes towards
              retirement of principal. """
name = "amortization-schedules"

inputs = [name + "input" + str(i) for i in range(5)]
slider1 = Slider(
    "Principal",
    mn=0,
    mx=1000000,
    step=1000,
    value=400000,
    tick=200000,
    name=inputs[0],
    kind="kdol",
)
slider2 = Slider(
    "Annual Rate", mn=0, mx=12, step=0.01, value=4.5, tick=3, kind="pct", name=inputs[1]
)
slider3 = Slider(
    "Number of Years", mn=0, mx=30, step=1, value=15, tick=5, name=inputs[2], kind=None
)
slider4 = Slider(
    "Balloon",
    mn=0,
    mx=1000000,
    step=1000,
    value=0,
    tick=200000,
    name=inputs[3],
    kind="kdol",
)

radio = dcc.RadioItems(
    options=[
        {"value": "Monthly", "label": "Monthly"},
        {"value": "Annual", "label": "Annual"},
    ],
    value="Monthly",
    inline=True,
    id=inputs[4],
    labelStyle={"display": "block"},
)

left = dbc.Col(dbc.Label("Payment Frequency", html_for=inputs[4]), xs=6)
right = dbc.Col(radio, xs=6)
radio = dbc.Row([left, right], align="top")

graph = dcc.Graph(id=name + "fig")
graph2 = dcc.Graph(id=name + "fig2")

payment = html.Div(id=name + "payment", style=text_style)
paymentLabel = dbc.Col(dbc.Label("Payment", html_for=name + "payment"), xs=6)
payment = dbc.Row([paymentLabel, dbc.Col(payment, xs=6)])

col1 = dbc.Col([slider3, html.Br(), radio], xs=4)
col2 = dbc.Col([slider1, slider4], xs=4)
col3 = dbc.Col([slider2, html.Br(), payment], xs=4)
row1 = dbc.Row([col1, col2, col3], align="top")

left = dbc.Col(graph2, xs=6)
right = dbc.Col(graph, xs=6)
row2 = dbc.Row([left, right])
body = html.Div([row1, html.Br(), row2])

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
    Output(name + "fig2", "figure"),
    Output(name + "payment", "children"),
]
inputs = [Input(i, "value") for i in inputs]
lst = outputs + inputs


@callback(*lst)
def call(*args):
    return figtbl(*args)
