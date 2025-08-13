# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable
from pages.risk.forecasting_rmse_mad_figtbl import figtbl
from pages.formatting import (
    Slider,
    Layout,
    ricegrey,
    style_header,
    style_data_conditional,
)

title = "Forecasting cumulative versus average returns"
chapter = "Risk and Return"
chapter_url = "risk"
runtitle = None
urls = None
name = "forecasting_rmse_mad"

text = """ 
    5,000 return histories and subsequent future return realizations are simulated assuming each period's return is normally distributed.  This page considers
    the suitability of arithmetic or geometric average returns to form predictors of various future outcomes.  The compounded geometric average return is better suited for forecasting the future compound realized return.  The arithmetic average return is better suited for forecasting the expected per period return, that is, the average realized return.  The geometric average return is better suited for forecasting the ex post realized geometric return.
    
    This page examines predicting the future from past returns.
    A past history of $n$ returns $r_1, \\ldots, r_{n}$ is simulated from the same 
    distribution as future returns $r_{n+1}, \\ldots, r_{n+n}$, so there are the same number of returns in the past and future periods.  Consider using either the past 
    arithmetic average return 
    $$\\bar{r}_{\\text{arithmetic}}= (1/n)\sum_{i=1}^{n} r_i$$ or the past
    geometric average return $\\bar{r}_{\\text{geometric}}= \prod_{i=1}^{n} (1+r_i)^{1/n}-1$ to
    form a predictor.  
    
    To evaluate the predictors, 5,000 of these hypothetical past and future periods are simulated.  For each simulated time-series, we calculate forecast errors, defined as the  realized future outcome minus the predictor formed using the past return realizations.  The distributions of the forecast errors are plotted on the right.  The tables on the left report the root mean square error, the mean absolute forecast error, and the median absolute forecast error for each predictor.
    
    The 1st outcome we are interested in forecasting is the future cumulative return:  $$\prod_{i=1}^{n} (1+r_{n+i})^{1/n}$$. 
    We consider a predictor formed using the arithmetic return, $$(1+ \\bar{r}_{\\text{arithmetic}})^{n}$$, and one formed using the geometric average return, $$(1+ \\bar{r}_{\\text{geometric}})^{n}$$. 
    
    The 2nd outcome we are interested in forecasting is the future arithmetic average return: $$(1/n)\sum_{i=1}^{n} r_{n+i}$$.  The two predictors are the arithmetic average return $$\\bar{r}_{\\text{arithmetic}}$$ and the geometric average return $$\\bar{r}_{\\text{geometric}}$$.
    
    
    The 3nd outcome we are interested in forecasting is the future geometric average return: $$\prod_{i=1}^{n} (1+r_{n+i})^{1/n}-1$$.  The two predictors are the arithmetic average return $$\\bar{r}_{\\text{arithmetic}}$$ and the geometric average return $$\\bar{r}_{\\text{geometric}}$$.
    """

text1 = dcc.Markdown(
    """ 
    The best estimate of the cumulative future return is the compounded past geometric average return, based on all three criteria in the table.  The distributions of forecast errors show that the median forecast error is about equal to zero when using the geometric average predictor, so the future cumulative return is greater than the forecast as often as it is below the forecast.  On the other hand, the past arithmetic average predictor is greater than the realized future cumulative return more often than not (the median forecast errors are negative). 
    """,
    style={"color": "black", "background-color": ricegrey}
)
text2 = dcc.Markdown(
    """ 
    The best estimate of the future arithmetic average return is the past arithmetic average return, based on all three criteria in the table.  The distributions of forecast errors show that the median forecast error is about equal to zero if the forecast is the arithmetic average return, so the future average return is greater than the forecast as often as it is below the forecast.  On the other hand, the past geometric average is less than the realized future arithmetic average return more often than not (the median forecast errors are positive).
    """,
    style={"color": "black", "background-color": ricegrey}
)
text3 = dcc.Markdown(
    """ 
    The best estimate of the future geometric average return is the past geometric average return, based on all three criteria in the table.  The distributions of forecast errors show that the median forecast error is about equal to zero if the forecast is the geometric average return, so the future geometric average return is greater than the forecast as often as it is below the forecast.  On the other hand, the past arithmetic average predictor is greater than the realized future geometric average return more often than not (the median forecast errors are negative).
    """,
    style={"color": "black", "background-color": ricegrey}
)

########## INPUTS
inputs = [name + "input" + str(i) for i in range(3)]
slider1 = Slider(
    "Expected return",
    mn=0,
    mx=12,
    step=1,
    value=6,
    tick=3,
    kind="pct",
    name=inputs[0],
)
slider2 = Slider(
    "Standard deviation",
    mn=0,
    mx=20,
    step=1,
    value=10,
    tick=5,
    kind="pct",
    name=inputs[1],
)

slider3 = Slider(
    "Years",
    mn=1,
    mx=40,
    step=1,
    value=20,
    tick=None,
    kind="tip",
    name=inputs[2],
)




########## OUTPUTS
graph1 = dcc.Graph(id=name + "fig1")
graph2 = dcc.Graph(id=name + "fig2")
graph3 = dcc.Graph(id=name + "fig3")
tbl1 = DataTable(
    id=name + "tbl1",
    columns=[
        {'name': c, 'id': name+c}
        for c in ["", "RMSE", "Mean Abs Dev", "Median Abs Dev"]
    ],
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_cell_conditional=[
        {
            'if': {'column_id': name},
            'textAlign': 'left'
        }
    ],
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl2 = DataTable(
    id=name + "tbl2",
    columns=[
        {'name': c, 'id': name+c}
        for c in ["", "RMSE", "Mean Abs Dev", "Median Abs Dev"]
    ],
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_cell_conditional=[
        {
            'if': {'column_id': name},
            'textAlign': 'left'
        }
    ],
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)
tbl3 = DataTable(
    id=name + "tbl3",
    columns=[
        {'name': c, 'id': name+c}
        for c in ["", "RMSE", "Mean Abs Dev", "Median Abs Dev"]
    ],
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_cell_conditional=[
        {
            'if': {'column_id': name},
            'textAlign': 'left'
        }
    ],
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'}
)





########## PAGE LAYOUT
btn = dbc.Button(
    "Click to Simulate",
    id=name + "button",
    n_clicks=0,
    color="primary",
    className="me-1",
    outline=True,
)
# btn = dbc.Row(btn)

# Top row - inputs
left0  = dbc.Col(btn, xs=12, sm=12, md=4, lg=4, className="mb-2")
right0 = dbc.Col([slider1, slider2,slider3], xs=12, sm=12, md=8, lg=8, className="mb-2")
row0 = dbc.Row([left0, right0], align='center', className="gx-1")

# 2nd row - cumulative return forecasting
left1  = dbc.Col(tbl1, xs=12, sm=12, md=6, lg=6, className="mb-2")
right1 = dbc.Col(graph1, xs=12, sm=12, md=6, lg=6, className="mb-2")
row1 = dbc.Row([left1,right1],align='center', className="gx-1")

# 3nd row - arithmetic average return forecasting
left2  = dbc.Col(tbl2, xs=12, sm=12, md=6, lg=6, className="mb-2")
right2 = dbc.Col(graph2, xs=12, sm=12, md=6, lg=6, className="mb-2")
row2 = dbc.Row([left2,right2],align='center', className="gx-1")

# 4th row - arithmetic average return forecasting
left3  = dbc.Col(tbl3, xs=12, sm=12, md=6, lg=6, className="mb-2")
right3 = dbc.Col(graph3, xs=12, sm=12, md=6, lg=6, className="mb-2")
row3 = dbc.Row([left3,right3],align='center', className="gx-1")

# Combine rows
# body = html.Div([btn, row0, html.Hr(), html.Br(), text1, row1, html.Br(), text2, row2, html.Br(), text3, row3])
body = dbc.Container([row0, html.Hr(), html.Br(), text1, row1, html.Br(), text2, row2, html.Br(), text3, row3], fluid=True, className="px-1")

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
    Output(name+"tbl1", "data"),
    Output(name+"tbl2", "data"),
    Output(name+"tbl3", "data"),
    Output(name+"fig1", "figure"),
    Output(name+"fig2", "figure"),
    Output(name+"fig3", "figure"),
    Input(name+"button", "n_clicks"),
    *[State(i, "value") for i in inputs]
)
def call(*args):
    return figtbl(name, *args)
