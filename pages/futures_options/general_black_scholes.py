import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback
from dash.dash_table import DataTable
from pages.formatting import (
    Layout,
    style_data,
    css_no_header,
    style_data_conditional,
    Slider,
    lightblue,
    myinput
)
from pages.futures_options.general_black_scholes_figtbl import figtbl

title = "General Black-Scholes formula"
runtitle = None
chapter = "Futures and Options"
chapter_url = "futures-options"
urls = None
text = """
    There is a general version of the Black-Scholes formula that includes extensions of the original formula
    by Merton (to random interest rates), Black (to futures options), and Margrabe (to exchange options).  A single
    formula covers both calls and puts.  Consider an exchange option, which is an option to exchange one asset
    for another.  Suppose it is European, and let $T$ denote the years to maturity.  Let $P_1$ denote the 
    present value of the asset that will be received if the option is exercised, and let $P_2$ denote the present
    value of the asset that will be delivered if the option is exercised.  Let $\\sigma$ denote the volatility of
    the ratio of present values (either $P_1$ to $P_2$ or the reverse - the volatility of the ratio is the same
    either way), and assume it is 
    constant.  Define
    $a = (\\log (P_1/P_2) + 0.5\\sigma^2T)/\\sqrt{\\sigma^2T}$ and 
    $b = a - \\sigma\\sqrt{T}$.  The value of the option is
    $P_1N(a) - P_2N(b)$, where $N$ denotes the standard normal distribution function.  
    
    This includes the original Black-Scholes call option formula by taking (i) $P_1 = e^{-qT}S$, which is the cost of
    enough shares to accumulate to a single share at the option maturity via reinvestment of dividends and hence is
    the present value of the asset to be received, (ii) $P_2 = e^{-rT}K$, which is the present value of the strike
    price, and (iii) $\\sigma =$ volatility of the underlying price, which in this case is the volatility 
    of $P_1/P_2$.  The general formula includes
    the put formula by taking $P_1=e^{-rT}K$ and $P_2 = e^{-qT}S$.  It includes random interest rates by taking
    $P_2$ (for a call) or $P_1$ (for a put) to be the price of a zero coupon bond maturing at $T$ that ha a 
    face value of $K$.  Note that, 
    with random interest rates, the volatility
    should be the volatility of the ratio of the underlying asset price to the zero-coupon bond price.  The formula
    includes options on futures by taking $P_1$ (for a call) or $P_2$ (for a put) to be the price of a discount bond
    multiplied by the futures price.  This is the present value of getting the market futures price at $T$, because
    combining the bond with a long futures that is marked to market produces cash at $T$ equal to the market 
    futures price at $T$.
    """
        

name = "general-black-scholes"

inputs = [name + "input" + str(i) for i in range(4)]

inpt1 = myinput(id=inputs[0], placeholder="Enter price", value=50)
inpt2 = myinput(id=inputs[1], placeholder="Enter price", value=50)
inpt3 = myinput(id=inputs[2], placeholder="Enter volatility as percent", value=30)
inpt4 = myinput(id=inputs[3], placeholder="Enter maturity in years", value=1)

tbl = DataTable(
    id=name + "tbl",
    css=css_no_header,
    style_data=style_data,
    style_as_list_view=True,
    style_data_conditional=style_data_conditional,
    style_table={'overflowX': 'auto', 'width': '100%', 'maxWidth': '100%'},
)

label1 = dbc.Label('Enter present value of asset to be received')
label2 = dbc.Label('Enter present value of asset to be delivered')
label3 = dbc.Label('Enter volatility > 0 in percent')
label4 = dbc.Label('Enter time to maturity > 0 in years')
left = dbc.Col([label1, inpt1, html.Br(), label2, inpt2], xs=12, sm=12, md=4, lg=4, className="mb-2")
mid = dbc.Col([label3, inpt3, html.Br(), label4, inpt4], xs=12, sm=12, md=4, lg=4, className="mb-2")
right = dbc.Col(tbl, xs=12, sm=12, md=4, lg=4, className="mb-2")
row = dbc.Row([left, mid, right], align='top', className="gx-1")

body = dbc.Container([row], fluid=True, className="px-1")

layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)
lst = [Output(name + 'tbl', "data")] + [Input(i, "value") for i in inputs]

@callback(*lst)
def call(*args):
    return figtbl(*args)
