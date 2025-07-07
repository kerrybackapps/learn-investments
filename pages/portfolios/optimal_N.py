import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable, FormatTemplate
from pages.portfolios.optimal_N_figtbl import figtbl
from pages.formatting import (
    Layout,
    text_style,
    style_data,
    style_data_conditional,
    Slider,
    style_header,
    style_editable,
    lightblue
)

percentage = FormatTemplate.percentage(1)

title = "Optimal portfolios with more assets"
runtitle = None
chapter = "Portfolios"
chapter_url = "portfolios"
urls = None

text = """ 
    Optimal portfolios are calculated for various levels of
    risk aversion.  Saving and borrowing are
    allowed, at possibly different rates, and short sales can be allowed.  We model 
    risk aversion as a penalty on variance
    in a standard formulation: a portfolio is optimal if it maximizes 
    'expected return - (1/2) x risk aversion x variance.' Risk aversion is a number that
    is usually assumed to be between 2 and 10. 
    
    Choose the number of assets, and edit the means, standard deviations, and 
    correlations in the tables.  All numbers should be entered as percents.  Enter correlations 
    only on the lower left part of the correlation table - the corresponding
    entries on the upper right will automatically update.  
       
    When the savings and borrowing rates are low enough compared to expected asset returns, there are two tangency portfolios,
    one at the savings rate and one at the borrowing rate, and the efficient frontier consists of three
    regions: (1) a savings region in which the risky asset portfolio is the savings-rate tangency portfolio, (2) a 
    fully invested region in which there is no borrowing or saving and the risky asset portfolio is a combination of the
    two tangency portfolios, and (3) a borrowing region in which the risky asset portfolio is the borrowing-rate
    tangency portfolio.  The first and third regions are indicated by the two blue line segments in the figure, 
    and the second region is the segment of the green curve that connects them.  The two tangency portfolios are
    indicated by green dots.  
    
    A positive value
    in the risk-free row in the table means that funds are saved at the savings rate; a negative value means that funds
    are borrowed at the borrowing rate.  The hover data 
    shows the level of risk aversion for which each portfolio is optimal.  At high levels of risk aversion, the optimal portfolio is in the first region; at 
    intermediate levels, it is in the second region; and at low levels, it is in the third region.  The total
    allocation to risky assets is higher for lower risk aversion.  
    
    It is possible to enter correlations that
    are not physically possible.  Whether this has happened is shown below. 
    """

name = "optimal-N"

slider1 = Slider(
    "Savings rate", mn=0, mx=5, step=0.1, value=2, tick=1, kind="pct", name=name+"rs"
)
slider2 = Slider(
    "Excess of borrowing over savings rate",
    mn=0,
    mx=5,
    step=0.1,
    value=3,
    tick=1,
    kind="pct",
    name=name+"extra",
)

Num = dcc.Dropdown(
    [i for i in range(2,9)],
    placeholder="Number of assets",
    value=3,
    id=name + "number",
    style={"backgroundColor": lightblue}
)

Radio = dcc.RadioItems(
    options=["Yes", "No"],
    value = "No", id=name+"radio", labelStyle={"display": "inline"}
)

Assets = DataTable(
    id=name + "list",
    columns=[{"name": "", "id": name+"l",}],
    style_header=style_header,
    style_data=style_header,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
    data=[{name + "l": "Asset "+str(i+1)} for i in range(3)]
)

Means = DataTable(
    id=name + "means",
    columns=[{"name": "Means", "id": name + "m", "editable": True}],
    data=[{name+"m": 10+2*i} for i in range(3)],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
)

Stdevs = DataTable(
    id=name + 'stdevs',
    columns = [{"name": "Std Devs", "id": name + "s", "editable": True}],
    data = [{name + "s": 15+5*i} for i in range(3)],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
)

Corrs = DataTable(
    id=name + 'corrs',
    columns = [{"name": "Asset " + str(i+1), "id": name+"asset"+str(i), "editable":True} for i in range(3)],
    data = [{name+"asset"+str(j): 100 if j==i else 0 for j in range(3)} for i in range(3)],
    style_header=style_header,
    style_data=style_editable,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
)

cols = ["Risk Aver", "10", "8", "6", "4", "2"]
columns = [dict(name=c, id=name + c, type="numeric", format=percentage) for c in cols]
tbl = DataTable(
    id=name + "tbl",
    columns=columns,
    style_data=style_data,
    style_header=style_header,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
)

graph = dcc.Graph(id=name + "fig")

slider1 = dbc.Col(slider1, xs=12, sm=12, md=4, lg=4, className="mb-2")
slider2 = dbc.Col(slider2, xs=12, sm=12, md=4, lg=4, className="mb-2")
col1 = dbc.Col(html.Div("Allow short sales"), xs=12, sm=6, md=2, lg=2, className="mb-2")
col2 = dbc.Col(Radio, xs=12, sm=6, md=2, lg=2, className="mb-2")
row1 = dbc.Row([slider1, slider2, col1, col2], align="center", className="gx-1")

"""
badge = html.H5(dbc.Badge("Asset Data", className="ms-1"))
badge = dbc.Col(badge, width={"size": 4, "offset": 5})
badge1 = dbc.Row(badge)

badge = html.H5(dbc.Badge("Results", className="ms-1"))
badge = dbc.Col(badge, width={"size": 4, "offset": 5})
badge2 = dbc.Row(badge)
"""



num = dbc.Row(dbc.Col([dbc.Label("Number of assets"), Num], xs=12, sm=6, md=2, lg=2, className="mb-2"), className="gx-1")

col0 = dbc.Col(Assets, xs=12, sm=6, md=1, lg=1, className="mb-2")
col1 = dbc.Col(Means, xs=12, sm=6, md=1, lg=1, className="mb-2")
col2 = dbc.Col(Stdevs, xs=12, sm=6, md=1, lg=1, className="mb-2")
col3 = dbc.Col([html.Label("Enter correlations in percent"), Corrs], xs=12, sm=12, md=9, lg=9, className="mb-2")
data = dbc.Row([col0, col1, col2, col3], align="end", className="gx-1")

col1 = dbc.Col(
    html.Div('Correlations are physically possible and assets are not linearly related?'),
    xs=12, sm=12, md=6, lg=6, className="mb-2"
)
col2 = dbc.Col(
    html.Div(id=name+'PDCov', style=text_style),
    xs=12, sm=6, md=1, lg=1, className="mb-2"
)
pdrow = dbc.Row([col1, col2], className="gx-1")

tbl = dbc.Col([dbc.Label("Optimal Portfolios"), tbl], xs=12, sm=12, md=5, lg=5, className="mb-2")
graph = dbc.Col(graph, xs=12, sm=12, md=7, lg=7, className="mb-2")
row3 = dbc.Row([tbl, graph], align="top", className="gx-1")

body = dbc.Container([num, data, html.Br(), pdrow, html.Hr(),
                 row1, html.Br(), row3
                 ], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

outputs = [Output(name+"means", "data"), Output(name+"stdevs", "data")]
outputs += [Output(name+"corrs", "columns"), Output(name+"corrs", "data")]
outputs += [Output(name+"fig", "figure"), Output(name+"PDCov","children"), Output(name+"tbl", "data")]
outputs += [Output(name+"list", "data")]

inputs = [Input(name + "number", "value"), Input(name + "radio", "value")]
inputs += [Input(name + "rs", "value"), Input(name + "extra", "value")]
inputs += [Input(name+"means", "data_timestamp"), State(name+"means", "data")]
inputs += [Input(name+"stdevs", "data_timestamp"), State(name+"stdevs", "data")]
inputs += [Input(name+"corrs", "data_timestamp"), State(name+"corrs", "columns"), State(name+"corrs", "data")]
inputs += [Input(name+"list", "data")]

lst = outputs + inputs

@callback(*lst)
def call(N, radio, rs, extra, mtime, mrows, stime, srows, ctime, ccols, crows, lrows) :
    M = len(mrows)
    if N != M :
        lrows = [{name+"l": "Asset "+str(i+1)} for i in range(N)]
        mrows = [{name+"m": 8+i} for i in range(N)]
        srows = [{name+"s": 20+3*i} for i in range(N)]
        ccols = [{"name": "Asset " + str(i+1), "id": name + "asset" + str(i), "editable": True} for i in range(N)]
        crows = [{name + "asset" + str(j): 100 if j == i else 0 for j in range(N)} for i in range(N)]
    for i in range(N):
        crows[i][name+"asset"+str(i)] = 100
        for j in range(N):
            crows[i][name+"asset"+str(j)] = crows[j][name+"asset"+str(i)]
    means = [float(row[name+"m"]) for row in mrows]
    stdevs = [float(row[name+"s"]) for row in srows]
    corrs = [[float(row[name+"asset"+str(j)]) for j in range(N)] for row in crows]
    fig, pdcov, tbl = figtbl(name, means, stdevs, corrs, radio, rs, extra)
    return mrows, srows, ccols, crows, fig, pdcov, tbl, lrows