import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate
from pages.portfolios.optimal_sb_figtbl import figtbl
from pages.formatting import (
    Layout,
    ricegrey,
    style_data,
    style_data_conditional,
    Slider,
    style_header,
)

percentage = FormatTemplate.percentage(1)
from datetime import date

today = date.today().year - 1

title = "Optimal portfolios of stocks, bonds, and gold"
runtitle = "Stocks and Bonds"
chapter = "Portfolios"
chapter_url = "portfolios"
urls = {"Python notebook": None}

text = """ 
    Optimal portfolios are calculated, using historical
    returns to estimate the expected returns, standard deviations, and correlations, for investors
    with various levels of risk aversion.  Saving and borrowing are
    allowed, at possibly different rates, and short sales can be allowed.  The estimates of expected 
    returns, standard deviations, and correlations
    are based on annual nominal returns over the date range specified.  The  gold return is the 
    percent change in the London fixing, which is obtained 
    from [Nasdaq Data Link](https://data.nasdaq.com/data/LBMA/GOLD-gold-price-london-fixing). The other
    return data is provided by 
    [Aswath Damodaran](https://pages.stern.nyu.edu/~adamodar/).  
           
   
    When the savings and borrowing rates are low enough compared to expected asset returns, there are two tangency portfolios,
    one at the savings rate and one at the borrowing rate, and the efficient frontier consists of three
    regions: (1) a savings region in which the risky asset portfolio is the savings-rate tangency portfolio, (2) a 
    fully invested region in which there is no borrowing or saving and the risky asset portfolio is a combination of the
    two tangency portfolios, and (3) a borrowing region in which the risky asset portfolio is the borrowing-rate
    tangency portfolio.  The first and third regions are indicated by the two blue line segments in the figure, and 
    the second region is the segment of the green curve that connects them.  The two tangency portfolios are
    indicated by green dots.  
    
    A positive value
    in the risk-free row in the table means that funds are saved at the savings rate; a negative value means that funds
    are borrowed at the borrowing rate.  The hover data for the blue curve
    shows the level of risk aversion for which each portfolio is optimal.  At high levels of risk aversion, the optimal portfolio is in the first region; at 
    intermediate levels, it is in the second region; and at low levels, it is in the third region.  The total
    allocation to risky assets is higher for lower risk aversion. 
    
    An interesting exercise is to compare the optimal portfolios over the separate date ranges 1968-2000 
    and 2000-2022.  In the former period, the correlation between Treasuries and the S&P 500 was 
    approximately +40\%.  In the latter period, it was -65%.
    
    The calculations here tell us which portfolios would have been 
    optimal in the past,
    but the past is an imperfect guide to the future.  In particular, it is hazardous to estimate 
    expected returns using sample mean returns over short or even moderately long time horizons.  
    """

name = "optimal-sb"

# Input components
inputs = [name + "input" + str(i) for i in range(4)]
# Date range slider
slider = dcc.RangeSlider(
    id=inputs[0],
    min=1968,
    max=today,
    step=1,
    value=[1968, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Select date range", html_for=name + "slider"), slider])
# Saving and Borrowing Rates sliders
slider1 = Slider(
    "Savings rate", mn=0, mx=5, step=0.1, value=2, tick=1, kind="pct", name=inputs[1]
)
slider2 = Slider(
    "Excess of borrowing over savings rate",
    mn=0,
    mx=5,
    step=0.1,
    value=3,
    tick=1,
    kind="pct",
    name=inputs[2],
)
radio = dcc.RadioItems(
    options=[
        {"value": "s", "label": "Yes"},
        {"value": "ns", "label": "No"},
     ],
    value="ns",
    id=inputs[3],
)


# Output components
# Graph
graph = dcc.Graph(id=name + "fig")
# Table

cols = ["Risk Aversion", "10", "8", "6", "4", "2"]
columns = [dict(name=c, id=name + c) for c in cols]
Ports = DataTable(
    id=name + "ports",
    columns=columns,
    style_header=style_header,
    #style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)

cols = ["", "S&P 500", "Gold", "Corporates", "Treasuries"]
columns = [dict(name=c, id=name + c) for c in cols]
Corr = DataTable(
    id=name + "corrs",
    columns=columns,
    style_header=style_header,
    style_data=style_data,
    style_data_conditional=style_data_conditional,
)

badge = html.H5(dbc.Badge("Results", className="ms-1"))
badge = dbc.Col(badge, width={"size": 4, "offset": 5})
badge = dbc.Row(badge)

# Layout

cola = dbc.Col(html.Div("Allow short sales"), width=dict(size=3, offset=4))
colb = dbc.Col(radio, md=1)
radio = dbc.Row([cola, colb], align="end")

left = dbc.Col(slider, md=4)
middle = dbc.Col(slider1, md=4)
right = dbc.Col(slider2, md=4)
row1 = dbc.Row([left, middle, right], align="center")

label1 = dbc.Label("Correlation Matrix")
label2 = dbc.Label("Optimal Portfolios")
left = dbc.Col([label1, Corr, html.Br(), label2, Ports], md=6)
right = dbc.Col(graph, md=6)
row2 = dbc.Row([left, right], align="top")

body = html.Div([row1, html.Hr(), radio, html.Hr(), html.Br(), row2])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

lst = [
    Output(name + "fig", "figure"),
    Output(name + "ports", "data"),
    Output(name + "corrs", "data"),
] + [Input(i, "value") for i in inputs]


@callback(*lst)
def call(*args):
    return figtbl(name, *args)