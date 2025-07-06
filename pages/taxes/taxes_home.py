import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable, FormatTemplate
from pages.formatting import (
    Slider,
    Layout,
    blue,
    style_header,
    style_data,
    style_data_conditional,
)
from pages.bonds.clean_dirty_figtbl import figtbl

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(1)

title = "Bonds"
runtitle = None
chapter = "Fixed Income"
chapter_url = "fixed-income"

urls = {"Python notebook": None}
text = """
             THome of Bonds
       """

name = "bonds-home"
body = None

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

