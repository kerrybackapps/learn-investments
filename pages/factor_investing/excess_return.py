from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from pages.factor_investing.excess_return_figtbl import figtbl, keys
from pages.formatting import Layout, style_data, style_header, style_data_conditional
from datetime import date

today = date.today().year - 1
from dash.dash_table import DataTable, FormatTemplate

percentage = FormatTemplate.percentage(1)

title = "Average excess returns against CAPM betas and alphas"
runtitle = "Average excess returns against CAPM betas and alphas"
chapter = "Factor Investing"
chapter_url = "factor-investing"

urls = {"Python notebook": None}
text = """
            TO DO
          """

name = "excess_return"

drop = dcc.Dropdown(keys, placeholder="Select a characteristic", id=name + "drop")
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
