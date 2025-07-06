# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.factor_investing.quintiles_figtbl import figtbl, keys
from pages.formatting import Layout, style_data, style_header, style_data_conditional, lightblue
from datetime import date

today = date.today().year - 1
from dash.dash_table import DataTable, FormatTemplate

percentage = FormatTemplate.percentage(1)

title = "Sorts on characteristics"
runtitle = None
chapter = "Factors"
chapter_url = "factor-investing"

urls = None

text = """ 
    The plots show returns from investing in various portfolios.
    The data comes from 
    [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).  Definitions
    of the characteristics and details of the portfolio constructions can be found there.  Except for the
    short-term reversal, momentum, and long-term reversal characteristics, stocks are sorted
    into five groups each month based on NYSE quintile breakpoints and are value weighted
    within groups. The short-term reversal, momentum, and long-term reversal characteristics 
    are called Prior_1_0, Prior_12_2, and Prior_60_13 in French's data library and are the
    returns over the most recent month, the prior year excluding the most recent month, 
    and the prior five years excluding the most recent year, respectively.  For these characteristics, 
    stocks are sorted into ten groups each month based on NYSE decile
    breakpoints and are value weighted within groups, and then adjacent deciles are equal weighted to
    form quintiles.
    """

name = "quintiles"

drop = dcc.Dropdown(
    keys,
    placeholder="Select a characteristic",
    id=name + "drop",
    style={"backgroundColor": lightblue}
)
drop = html.Div([dbc.Label("Characteristic", html_for=name + "drop"), drop])

slider = dcc.RangeSlider(
    id=name + "slider",
    min=1926,
    max=today,
    step=1,
    value=[1980, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider = html.Div([dbc.Label("Date Range", html_for=name + "slider"), slider])

graph_std = dcc.Graph(id=name + "fig1")
graph_log = dcc.Graph(id=name + "fig2")
graph_box = dcc.Graph(id=name + "fig3")

columns = [dict(name="Statistic", id=name + "Statistic")]
columns += [
    dict(name=c, id=name + c, type="numeric", format=percentage)
    for c in ["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]
]
tbl = DataTable(
    id=name + "tbl",
    columns=columns,
    style_header=style_header,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)
tbl = dcc.Loading(id=name + "loading", children=tbl, type="circle")


left = dbc.Col([drop, html.Br(), slider], md=6)
right = dbc.Col(tbl, md=6)
row1 = dbc.Row([left, right], align="center")

left = dbc.Col(graph_std, md=4)
middle = dbc.Col(graph_log, md=4)
right = dbc.Col(graph_box, md=4)
row2 = dbc.Row([left, middle, right], align="center")

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
outputs = [Output(name + f, "figure") for f in ["fig1", "fig2", "fig3"]] + [
    Output(name + "tbl", "data")
]
inputs = [Input(name + "drop", "value"), Input(name + "slider", "value")]
lst = outputs + inputs


@callback(*lst, prevent_initial_call=True)

# this callback assigns column names that match the names in DataTable
def call(*args):
    fig1, fig2, fig3, tbl = figtbl(*args)
    tbl.columns = [name + c for c in tbl.columns]
    return fig1, fig2, fig3, tbl.to_dict("records")
