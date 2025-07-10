# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 08:52:29 2022

@author: kerry
"""
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_iconify import DashIconify
from pages.urls import *
import plotly.io as pio
import pandas as pd
import numpy as np

##############################################
#
# COLORS
#
#############################################

plotly_template = pio.templates["simple_white"]
colors = plotly_template.layout.colorway
blue = colors[0]
red = colors[1]
green = colors[2]
purple = colors[3]
orange = colors[4]
teal = colors[5]
pink = colors[6]
lime = colors[7]
magenta = colors[8]
yellow = colors[9]

medblue = "#93CCFD"
white = "#fff"
black = "#000"
danger = "#ff0039"
light = "#f8f9fa"
dark = "#373a3c"
primary = "#2780e3"
secondary = "#373a3c"
riceblue = "#00205B"
ricegrey = "#C1C6C8"
gray400 = "#ced4da"
gray600 = "#868e96"
gray700 = "#495057"
gray100 = "#f8f9fa"
gray300 = "#dee2e6"
gray500 = "#adb5bd"
gray200 = "#e9ecef"
gray400 = "#ced4da"
lightblue = "#E6F4FF"

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': white,
    'backgroundColor': primary
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': white,
    'color': primary,
    'fontWeight': 'bold',
    'padding': '6px'
}

text_style = {"color": primary, "font-weight": "bold", "background-color": white} # {"color": riceblue, 'font-weight': 'bold', 'background-color': ricegrey}

def myinput(id, value=None, placeholder=""):
    if value:
        return dbc.Input(id=id, type="numeric", placeholder=placeholder, value=value, style={"backgroundColor": lightblue})
    else:
        return dbc.Input(id=id, type="text", placeholder=placeholder, style={"backgroundColor": lightblue})

###################################################
#
# DATA TABLE STYLING
#
###################################################

style_header = {
    "backgroundColor": gray700,
    "fontWeight": "bold",
    "color": white,
}

style_header_dark = {
    "backgroundColor": gray700,
    "fontWeight": "bold",
    "color": white,
}

def mybadge(txt) :
    return html.H4(dbc.Badge(txt, className="ms-1", color=primary, text_color=white))

style_data = {"backgroundColor": gray200}
style_editable = {"backgroundColor": lightblue}
style_light = style_data
style_dark = {"backgroundColor": gray200}

css_no_header = [{"selector": "tr:first-child", "rule": "display: none"}]


style_data_conditional = [
    {"if": {"row_index": "odd"}, "backgroundColor": gray200,},
    {"if": {"row_index": "even"}, "backgroundColor": gray400},
]

#############################################################
#
# FIGURE STYLING
#
#############################################################

def largefig(fig, showlegend=False):
    fig.layout.template = "simple_white"
    fig.update_layout(margin=dict(l=25, r=25, t=40, b=25))
    fig.update_xaxes(title_font_size=16, showgrid=True)
    fig.update_yaxes(title_font_size=16, showgrid=True)
    fig.update_layout(font_size=14)
    fig.update_layout(showlegend=showlegend)
    return fig


def smallfig(fig, showlegend=False):
    fig.layout.template = "simple_white"
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=25))
    fig.update_xaxes(title_font_size=14, showgrid=True)
    fig.update_yaxes(title_font_size=14, showgrid=True)
    fig.update_layout(font_size=12)
    fig.update_layout(showlegend=showlegend)
    return fig

#####################################################
#
# SLIDER STYLING
#
#####################################################

def marks(a, b, c):
    marks = [i if i != int(i) else int(i) for i in np.arange(a, b + c, c)]
    labels = [str(x) if x != int(x) else str(int(x)) for x in marks]
    return dict(zip(marks, labels))


def pctmarks(a, b, c):
    marks = range(a, b + c, c)
    labels = [str(x) + "%" for x in marks]
    return dict(zip(marks, labels))


def dolmarks(a, b, c):
    marks = range(a, b + c, c)
    labels = ["$" + "{:,}".format(x) for x in marks]
    return dict(zip(marks, labels))


def kdolmarks(a, b, c):
    marks = range(a, b + c, c)
    labels = ["$" + "{:,}".format(int(x / 1000)) + "k" for x in marks]
    return dict(zip(marks, labels))


dct = dict(pct=pctmarks, dol=dolmarks, kdol=kdolmarks)


def Slider(text, mn, mx, step, value, tick, name, kind=None):
    if kind == "tip":
        slider = dcc.Slider(
            mn,
            mx,
            step,
            id=name,
            value=value,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
        )
    else:
        markfn = marks if not kind else dct[kind]
        slider = dcc.Slider(
            mn,
            mx,
            step,
            id=name,
            value=value,
            marks=markfn(mn, mx, tick),
            tooltip={"placement": "bottom", "always_visible": False},
        )
    return html.Div([dbc.Label(text, html_for=name), slider])

#############################################################
#
# NAVIGATION BARS FOR HOME PAGE (SECTIONS)
# URLS ARE CHAPTER URLS
#
#############################################################

def navbar_home(urls, name, dropdownLabel):
    return dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(titleDict[url], href=urlDict[url[1:]][0])
                    for url in urls
                ],
                nav=True,
                in_navbar=True,
                label=dropdownLabel,
            ),
        ],
        brand=name,
        brand_href=None,
        color=primary,
        dark=True,
    )

#############################################################
#
# DICTIONARY TO GET ALL PAGE URLS FOR A CHAPTER
# FROM THE CHAPTER URL/NAME.  USE THIS TO PASS URLS
# TO NAVBAR FOR EACH PAGE
#
#############################################################

urlDict = {"borrowing-saving": borrowing_saving_urls}
urlDict["risk"] = risk_urls
urlDict["portfolios"] = portfolios_urls
urlDict["capm"] = capm_urls
# urlDict["performance-evaluation"] = performance_evaluation_urls
# urlDict["taxes"] = taxes_urls
urlDict["futures-options"] = futures_options_urls
urlDict["fixed-income"] = fixed_income_urls
urlDict["factor-investing"] = factor_investing_urls
urlDict["topics"] = topics_urls

#######################################################
#
# POPOVER MENU
#
#######################################################

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

chapter_urls = [x[1: ] for x in all_chapter_urls]

name = dict(zip(labels, chapter_urls))

level1_items = [dbc.DropdownMenuItem(label, id="menu"+label, href=urlDict[name[label]][0]) for label in labels]
level2_items = [[dbc.DropdownMenuItem(titleDict[page], href=page) for page in urlDict[name[label]]] for label in labels]
popovers = [dbc.Popover(items, target="menu"+label, trigger="hover", body=True) for label, items in zip(labels, level2_items)]

#######################################################
#
# LIST OF ALL PAGE URLS
# USE THIS FOR NAVIGATION ARROWS ON EACH PAGE
#
#######################################################

allUrls = []
for lst in [
    borrowing_saving_urls,
    risk_urls,
    portfolios_urls,
    capm_urls,
    factor_investing_urls,
    topics_urls,
    futures_options_urls,
    fixed_income_urls,
]:
    allUrls += lst

#########################################################
#
# DICTIONARY THAT MAPS NUMBERS TO CHAPTER URLS
#
#########################################################

#nums = [str(i) for i in range(1,9)]
#DICT = dict(zip(all_chapter_urls, nums))

#########################################################
#
# DICTIONARY THAT MAPS PAGE TITLE TO ITS URL
# NEED THIS BECAUSE LAYOUT FUNCTION DIDN'T TAKE
# PAGE URL AS AN INPUT BUT NOW WE NEED IT
#
########################################################

titleDictReversed = {value: key for key, value in titleDict.items()}

########################################################
#
# LAYOUT FUNCTION TAKES THE FOLLOWING ARGUMENTS
# WITH EXAMPLES
#
#     title = "Optimal portfolios of stocks and bonds"
#     runtitle = None (legacy argument)
#     chapter = "Portfolios"
#     chapter_url = "portfolios"
#     urls = None (legacy argument)
#     text = ""
#     body = html.Div()
#
# THE LAYOUT FUNCTION CREATES THE TOP RIBBON OF
# NAVIGATION ELEMENTS AND THE NAVIGATION BAR THAT
# CONTAINS THE PAGE NAME AND LINKS TO OTHER PAGES IN
# THE CHAPTER AND THEN ADDS THE TEXT AND BODY
#
# RUNTITLE IS NO LONGER USED.  IT WAS PART OF BREADCRUMBS.
# URLS IS NO LONGER USED.  IT IS EASIER TO MAINTAIN THE
# LINKS TO PYTHON NOTEBOOKS AND EXCEL WORKBOOKS
# IN A CENTRALIZED FASHION.
#
# FOR NOW, READ NOTEBOOK AND WORKBOOK LINKS FROM FILES
# EVENTUALLY, HARD CODE IT
#
#########################################################

linksExcel = pd.read_excel("assets/links.xlsx", header=None)
linksExcel.columns = ['page', 'link']
linksExcel = linksExcel.dropna()
pagesExcel = linksExcel.page.to_list()
linksExcel = linksExcel.set_index('page').to_dict()['link']

linksPython = pd.read_excel("assets/linksPython.xlsx", header=None)
linksPython.columns = ['page', 'link']
linksPython = linksPython.dropna()
pagesPython = linksPython.page.to_list()
linksPython = linksPython.set_index('page').to_dict()['link']

small_wds = "a at of and or with for on".split()
large_wds = "CAPM French Two-Way".split()
def mycap(s):
    s = s.split()
    s = [x if x in small_wds + large_wds else x.capitalize() for x in s]
    return ' '.join(s)


def Layout(title, runtitle, chapter, chapter_url, urls, text, body):
    chapter = ("Funds and Taxes" if chapter == "Topics" else (
                   "Sorts and Factors" if chapter == "Factors" else (
                       "Time Value of Money" if chapter == "Borrowing and Saving" else chapter
                       )
                   )
               )
    iconcolor = primary  # ricegrey
    backcolor = medblue # "#93CCFD" # "#a2e8f5" # white  # riceblue

    ##################################################
    #
    # DROPDOWN TO OTHER CHAPTERS
    # USES EMOJI AS ICON
    #
    ##################################################

    children = [
        dbc.DropdownMenuItem(label, id = "menu1" + label, href=homepages[label])     #urlDict[label[1:]][0])
        for label in labels
    ]

    def lst(chapter):
        item1 = dbc.DropdownMenuItem("Overview", href=homepages[chapter])
        pages = urlDict[name[chapter]]
        return [item1] + [dbc.DropdownMenuItem(titleDict[page], href=page) for page in pages[1:]]

    level2_items = [lst(label) for label in labels]
    popovers = [dbc.Popover(items, target="menu1" + label, trigger="hover", body=True) for label, items in
                zip(labels, level2_items)]

    dropdown = dbc.DropdownMenu(
        label="🗐",
        children=children,
        toggle_style={"color": white, "background": primary, "outline": primary},
    )

    dropdown = dbc.Col(
        [
            dbc.Container(
                [dropdown] + popovers,
                id="nav-dropdown",
                fluid=True,
                className="px-0"
            ),
        ],
        width={"size":1, "offset":2},
        className="d-flex justify-content-end"
    )

    ##################################################
    #
    # LINK TO HOME
    #
    ##################################################

    homeicon = "dashicons:admin-home"  # 'ci:home-alt-fill' # 'bxs:home' # 'ant-design:home-outlined'
    home = dbc.Col(
        [
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink(
                            DashIconify(icon=homeicon, width=36, height=36),
                            href="../",
                            style={"color": iconcolor},
                        ),
                        id="nav-home"
                    ),
                ],
                justified=True
            ),
        ],
        width={"size":2, "offset":0}
    )

    ##################################################
    #
    # NAVIGATION ARROWS
    #
    ##################################################

    u = titleDictReversed[title]
    indx = allUrls.index(u)
    if indx == 0:
        lefturl = "/"
        righturl = allUrls[1]
    elif indx == len(allUrls) - 1:
        lefturl = allUrls[-2]
        righturl = "/"
    else:
        lefturl = allUrls[indx - 1]
        righturl = allUrls[indx + 1]

    lefticon = "bi:arrow-left-circle-fill"  # 'bi:arrow-left-circle'
    righticon = "bi:arrow-right-circle-fill"  # 'bi:arrow-right-circle'
    leftarrow = dbc.NavItem(
        dbc.NavLink(
            DashIconify(icon=lefticon, width=20, height=20),
            href=lefturl,
            style={"color": iconcolor},
        ),
        id="nav-left"
    )
    rightarrow = dbc.NavItem(
        dbc.NavLink(
            DashIconify(icon=righticon, width=20, height=20),
            href=righturl,
            style={"color": iconcolor},
        ),
        id="nav-right"
    )
 
    ##################################################
    #
    # NAVIGATION TO PYTHON NOTEBOOK
    #
    ##################################################

    iconPython = "logos:python" # "mdi:language-python"  # 'teenyicons:python-solid' #'vscode-icons:folder-type-python' tabler:brand-python' #
    iconPython = DashIconify(icon=iconPython, width=30, height=30)
    python = dbc.NavLink(
        iconPython,
        href=f"https://colab.research.google.com/github/learn-investments/notebooks/blob/main/{chapter.lower()}/{title.lower()}.ipynb",
        # style={"color": iconcolor},
        target="_blank",
        id=chapter+title+"colablink"
    )
    python = dbc.Nav(
        [
            dbc.NavItem(
                python,
                id="nav-python"
            ),
            dbc.Popover(
                "Python Code",
                target="nav-python",
                trigger="hover",
                body=True,
                placement="bottom"
            ),
        ],
        justified=True
    )
 
    #####################################################
    #
    # CREATE TOP RIBBON
    #
    #####################################################

    pages = urlDict[name[chapter]]
    if title == titleDict[pages[0]]:
        arrows = dbc.Col(
            dbc.Nav(
                [
                    leftarrow,
                    rightarrow,
                ],
                justified=True
            ),
            width={"size": 6, "offset": 1}
        )
    else:
        arrows = dbc.Col(
            dbc.Nav(
                [
                    leftarrow,
                    python,
                    rightarrow,
                ],
                justified=True
            ),
            width={"size": 6, "offset": 1}
        )

    cols = [home, arrows, dropdown]

    toprow = dbc.Row(cols, align="center", className="mx-0")
    toprow = dbc.Card(toprow, style={"background-color": "#F3E5CF"}) #"#F3E8CF"}) # gray400})

    ##########################################################
    #
    # CREATE  WITH TITLE AND LINKS
    # TO OTHER PAGES IN CHAPTER
    #
    ##########################################################
    
    #ltrs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']
    pages = urlDict[chapter_url]
    #navindx = pages.index(u)
    #navindx = ltrs[navindx]
    nav = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[dbc.DropdownMenuItem("Overview", href=homepages[chapter])] + [
                    dbc.DropdownMenuItem(titleDict[page], href=page) # ltr + ". " + titleDict[page], href=page)
                    for page in pages[1:]
                ],
                nav=True,
                in_navbar=True,
                label=chapter,
            ),
        ],
        brand= mycap(title), 
        brand_href=None,
        color="primary",
        dark=True,
        fluid=True,
    )

    nav = dbc.Row(dbc.Col(nav, width={"size": 8, "offset": 2}), className="mx-0")

    top = html.Div(
        [
            toprow,
            html.Br(),
            nav,
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        dcc.Markdown(text, mathjax=True, style={"font-size": 18, "color": "#000"}), #, "font-weight": "bold"}),
                    ),
                    width={"size": 10, "offset": 1}
                )
            ),
            html.Hr(),
         ],
        style={"background-color": "#BCE1F5"} # "#33BEFF"}
    )

    return dbc.Container([top, body], fluid=True, className="px-0")

def Overview(titles, texts):
    cards = []
    for ttle, txt in zip(titles, texts):
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5(ttle, className="card-subtitle"),
                    html.P(txt, className="card-text")
                ]
            ),
        )
        cards.append(card)

    body = dbc.Row(
        dbc.Col(
            cards,
            width={"size": 10, "offset": 1},
            style={"backgroundColor": "#BCE1F5"}  # "#2780e3"}
        ),
    )
    return body