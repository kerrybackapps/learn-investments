# -*- coding: utf-8 -*-
    
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages.urls import *
from config import riceblue, gray300, gray100 as background, medblue
from pages.formatting import titleDict, all_chapter_urls, urlDict
import warnings
from pages.register_pages import register_all

warnings.simplefilter(action="ignore", category=FutureWarning)

layout = register_all()

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP], # [dbc.themes.CYBORG],
    meta_tags=[
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }
]
)
server = app.server

app.layout = html.Div(
    [dcc.Location(
        id="url", 
        refresh=False
    ), 
    html.Div(id="page-content")]
)

labels = [titleDict[x] for x in all_chapter_urls]
labels = [str(i+1) + ". " + label for i, label in enumerate(labels)]


urls = [
    borrowing_saving_urls[0],
    risk_urls[0],
    portfolios_urls[0],
    capm_urls[0],
    factor_investing_urls[0],
    topics_urls[0],
    futures_options_urls[0],
    fixed_income_urls[0]
]

labels = [
    "Time Value of Money",
    "Risk and Return",
    "Portfolios",
    "Capital Asset Pricing Model",
    "Sorts and Factors",
    "Funds and Taxes",
    "Futures and Options",
    "Fixed Income"
]



nav = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(label, id="menu"+label, href=homepages[label]) # href=url, style={"color": riceblue})
                    for label, url in zip(labels, urls)
                ],
                nav=True,
                in_navbar=True,
                label="",
            ),
        ],
        brand="Enter",
        brand_href=urls[0],
        brand_style={"color": riceblue, "font-size": 24},
        color=medblue, #,"white", #background # medblue # "#93CCFD",
        # dark=True,
        fluid=True,
        style={"background-color": "rgba(255, 255, 255, 0.5)"}
)

chapter_urls = [x[1: ] for x in all_chapter_urls]

name = dict(zip(labels, chapter_urls))


def lst(chapter):
    item1 = dbc.DropdownMenuItem("Overview", href=homepages[chapter])
    pages = urlDict[name[chapter]]
    return [item1] + [dbc.DropdownMenuItem(titleDict[page], href=page) for page in pages[1:]]


level2_items = [lst(label) for label in labels]

popovers = [dbc.Popover(items, target="menu"+label, trigger="hover", body=True) for label, items in zip(labels, level2_items)]

nav2 = dbc.Col(
        dbc.Container([nav]+popovers),
        width={"size": 4, "offset": 4}
)
nav2 = dbc.Row(nav2)


row2 = dbc.Row(
    [
        dbc.Col(
            [html.H1("Learn Investments @ Rice Business", style={"color": "white", "font-weight": "bold"}),
             html.H5("Winner of the 2023 Financial Management Association Innovation in Teaching Award",
             style={"color": "white"})
             ],
            width={"size": 11, "offset": 1}
        ),
    ],

    align="end"
)

div1 = html.Div(
    [
        row2,
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        nav2,
        html.Br(),
        html.Br(),
        html.Br(),
    ],
    style={
        "background-image": "url(/assets/mcnair.jpg)",
        "background-repeat": "no-repeat",
        "background-size": "cover",
        "background-position": "right",
    },
)

us = dbc.Col(
    [
        html.H5(
            dcc.Markdown(
                """
                Welcome to the site for learning and teaching investments and related topics, including
                options and futures, fixed income, portfolio management, and introductory finance.  Created at
                the [Jones Graduate School
                of Business](https://business.rice.edu/) at [Rice University](https://www.rice.edu/).
                
                This website contains over 80 pages in 8 different sections.  Each section includes an
                overview that describes the pages in that section.  The pages present
                interactive tables and figures to illustrate investment concepts.  Many pages pull data
                from online sources, and all pages allow user control of inputs - for example, entering stock tickers
                or option parameters.  Hovering the cursor over
                the plots will bring up information about the data plotted.  
                
                We also provide the python code that generates the figures and tables.  Each page 
                contains a link to a Jupyter notebook that opens on [Google Colab](https://colab.google/) and 
                can be run there without installing any software.  This is an extra feature.  The 
                interactive web elements are "point and click" and do not require any
                knowledge of python.
                
                We 
                welcome all users, and we welcome [comments and suggestions](mailto:kerryback@gmail.com).
                """
            )
        ),
    ],
    style={"backgroundColor": background},
    width={"size":10, "offset":1}
)

footnote = dbc.Col(
    html.H6(
                            """
                            The image is of McNair Hall, the home of the 
                            Jones Graduate School of Business at Rice University.
                            """
            ),
    width={"size": 9, "offset": 1}
)

credits = dbc.Col(
                    [
                        dbc.Button(
                            "About",
                            id="hover-target",
                            color=gray300, 
                            className="me-1",
                            n_clicks=0,
                        ),
                        dbc.Popover(
                            """ 
                            This is a python Dash app.  It was written and is maintained by JGSB finance professors
                            Kerry Back and Kevin Crotty.
                            """,
                            target="hover-target",
                            body=True,
                            trigger="hover",
                        )
                    ],
                    style={"backgroundColor": gray300},
                    width={"size":1}
)


us = html.Div(
    [
        us,
        dbc.Row([footnote, credits], align="end")
    ]
)

div2 = html.Div(
    [
        html.Br(),
        us,
        html.Br(),
    ],
    style={"background-color": background, "font-size": "large"}
)

index_layout = [div1, div2]


@callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    print("Requested pathname:", pathname, flush=True)
    normalized = pathname.rstrip("/") if pathname != "/" else "/"
    if normalized in layout:
        return layout[normalized]
    else:
        return index_layout
