# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""

from dash import dcc, html, Output, Input, callback, State
import dash_bootstrap_components as dbc
from pages.factor_investing.ghz_sorts_figtbl import figtbl, chars
from pages.formatting import Layout, style_data, style_header, style_data_conditional, lightblue
from datetime import date

today = date.today().year - 1
from dash.dash_table import DataTable, FormatTemplate

percentage = FormatTemplate.percentage(1)

title = "Sorts on other characteristics"
runtitle = None
chapter = "Factors"
chapter_url = "factor-investing"
urls = None

text = """ In a 
paper published in The Review of Financial Studies in 2017, Jeremiah Green, John Hand, and 
             Frank Zhang examine 102 stock characteristics that had been found in prior studies to have some
             predictive power for stock returns.  The full paper can be found 
             [here](https://academic.oup.com/rfs/article-abstract/30/12/4389/3091648)
             or [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2262374).  An abbreviated version
             containing the definitions of the characteristics and bibliographic information regarding the
             prior studies can be found 
             [here](https://www.dropbox.com/s/drcv0r1vmu56bla/ghz.pdf?dl=1).  This page computes and 
             displays returns from monthly quintile sorts
             on the characteristics, using all non-micro-cap U.S. stocks 
             (meaning stocks with market caps above the NYSE 20th percentile),
             from January 2000 to the present.  The number
             of stocks varies by month in the range of 1,500 to 2,700.  Stocks are sorted into quintiles each month
             and the equally weighted portfolio return is computed for each group each month.  The quintile returns
             will download as a csv file.  11 of the 102 characteristics are dummy variables or integer-valued and hence
             not suitable to use for sorting.  You can select any of the other 91 characteristics from the dropdown
             menu. 
             
             """

name = "ghz-sorts"

drop = dcc.Dropdown(chars, placeholder="Select a characteristic", id=name + "drop", style={"backgroundColor": lightblue})
# drop = html.Div([dbc.Label("Characteristic", html_for=name + "drop"), drop])
btn = dbc.Button(
    "Click to Run",
    id=name+'btn',
    n_clicks=0,
    color="primary",
    className="me-1",
)
download = html.Div([dcc.Download(id=name + "download")])


graph_std = dcc.Loading(
    id=name + "loading1", children=[dcc.Graph(id=name + "fig1")], type="circle"
)
graph_log = dcc.Loading(
    id=name + "loading2", children=[dcc.Graph(id=name + "fig2")], type="circle"
)
graph_box = dcc.Loading(
    id=name + "loading3", children=[dcc.Graph(id=name + "fig3")], type="circle"
)


columns = [dict(name="Statistic", id=name + "Statistic")]
columns += [
    dict(name=c, id=name + c, type="numeric", format=percentage)
    for c in ["Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20"]
]
tbl = DataTable(
    id=name + "tbl",
    columns=columns,
    style_header=style_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)
tbl = dcc.Loading(id=name + "loading4", children=[tbl], type="circle")

left = dbc.Col(drop, md=3)
middle = dbc.Col(btn, width={"size": 2, "offset": 1})
right = dbc.Col(tbl, md=6)
row1 = dbc.Row([left, middle, right], align="top")

left = dbc.Col(graph_std, md=4)
middle = dbc.Col(graph_log, md=4)
right = dbc.Col(graph_box, md=4)
row2 = dbc.Row([left, middle, right], align="center")

body = html.Div([row1, html.Br(), row2, download])

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
outputs = [Output(name + f, "figure") for f in ["fig1", "fig2", "fig3"]]
outputs += [Output(name + "tbl", "data")]
outputs += [Output(name + "download", "data")]
inputs = [State(name + "drop", "value"), Input(name+'btn', 'n_clicks')]
lst = outputs + inputs


@callback(*lst, prevent_initial_call=True)

# this callback assigns column names that match the names in DataTable
def call(*args):
    fig1, fig2, fig3, tbl, df = figtbl(*args)
    tbl.columns = [name + c for c in tbl.columns]
    return (
        fig1,
        fig2,
        fig3,
        tbl.to_dict("records"),
        dcc.send_data_frame(df.to_csv, "quintiles.csv"),
    )
