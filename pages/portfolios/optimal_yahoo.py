from pages.portfolios.optimal_yahoo_figtbl import figtbl
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, callback, State
from dash.dash_table import DataTable, FormatTemplate
from pages.formatting import (
    Layout,
    css_no_header,
    style_header,
    style_data_conditional,
    Slider,
    style_data,
    text_style,
    style_editable,
    lightblue
)
import plotly.graph_objects as go
from datetime import date
from dash.exceptions import PreventUpdate
from dash import callback_context

percentage = FormatTemplate.percentage(1)
today = date.today().year

title = "Optimal portfolios of stocks or funds"
runtitle = None
chapter = "Portfolios"
chapter_url = "portfolios"
urls = None

text = """ 
    Monthly returns are computed for the specified tickers over the specified date range
    from adjusted closing prices 
    provided by Yahoo Finance.  The historical means, standard deviations,
    and correlations are used as estimates of population
    means, standard deviations
    and correlations, and optimal portfolios are computed for different levels of risk 
    aversion.  Saving and borrowing are
    allowed, at possibly different rates, and short sales can be allowed.  Interest rates should be specified 
    as annual rates.  The actual date range used is the largest within the specified range for which all tickers
    were traded.  It is stated below the date range slider.  The default tickers are
    
    * SPY = SPDR S&P 500 ETF
    * GLD = SPDR Gold Trust ETF
    * LQD = iShares iBoxx Investment Grade Corporate Bond ETF
    * IEF = iShares 7-10 Year Treasury Bond ETF
    
    The correlation matrix is shown at the
    bottom of the page.  The Optimal Portfolios table and the figure report annualized means and standard 
    deviations.  
    
    When the savings and borrowing rates are low enough compared to expected asset returns, there are two tangency portfolios,
    one at the savings rate and one at the borrowing rate, and the efficient frontier consists of three
    regions: (1) a savings region in which the risky asset portfolio is the savings-rate tangency portfolio, (2) a 
    fully invested region in which there is no borrowing or saving and the risky asset portfolio is a combination of the
    two tangency portfolios, and (3) a borrowing region in which the risky asset portfolio is the borrowing-rate
    tangency portfolio.  The first and third regions are indicated by the two blue line segments in the figure, 
    and the second region is the segment of the green curve that connects them.  The two tangency portfolios are
    indicated by green dots.  
    
    A positive value
    in the risk-free row in the Optimal Portfolios table means that funds are saved at the savings rate; a 
    negative value means that funds
    are borrowed at the borrowing rate.  The hover data for the blue curve
    shows the level of risk aversion for which each portfolio is optimal.   At high levels of risk aversion, the optimal portfolio is in the first region; at 
    intermediate levels, it is in the second region; and at low levels, it is in the third region.  The total
    allocation to risky assets is higher for lower risk aversion.  
       
    The calculations tell us which portfolios would have been 
    optimal in the past,
    but the past is an imperfect guide to the future.  In particular, it is hazardous to estimate 
    expected returns using sample mean returns over short or even moderately long time horizons.  
    """

text1 = """
    Run
    """

text2 = dcc.Markdown(
    """ 
    Specify how many tickers you wish to use, and edit the list of tickers.   
    """
)


name = "optimal-yahoo"

inputs = [name + "input" + str(i) for i in range(4)]
slider0 = dcc.RangeSlider(
    id=inputs[0],
    min=1970,
    max=today,
    step=1,
    value=[1990, today],
    marks=None,
    pushable=1,
    tooltip={"placement": "bottom", "always_visible": True},
)
slider0 = html.Div([dbc.Label("Select date range", html_for=inputs[0]), slider0])
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
Radio = dcc.RadioItems(
    options=[
        {"value": "s", "label": "Yes"},
        {"value": "ns", "label": "No"},

    ],
    value="ns",
    inline=True,
    id=inputs[3],
)

Drop = dcc.Dropdown(
    [i for i in range(2, 11)], placeholder="Number of assets", value=4, id=name+"Num", style={"backgroundColor": lightblue}
)

Tickers = DataTable(
    id=name + "tickers",
    columns=[{"name": "Tickers", "id": name+"t", "editable": True}],
    css = css_no_header,
    style_data=style_editable,
    data=[{name+"t": "spy"}, {name+"t": "gld"}, {name+"t": "lqd"}, {name+"t": "ief"}, ]
)
Tickers = dcc.Loading(Tickers, type="circle")

Btn = dbc.Button(
    text1,
    id=name + 'btn',
    n_clicks=0,
    color="primary",
    className="me-1",
)

# Interval component for debounce mechanism
ticker_interval = dcc.Interval(
    id=name + "-ticker-input-interval",
    interval=1000,  # 1 second delay
    n_intervals=0,
    max_intervals=1 # Fire once after reset
)

graph = dcc.Graph(id=name + "fig")
graph = dcc.Loading(id=name + "loading1", children=[graph], type="circle")

cols = ["Risk Aver", "10", "8", "6", "4", "2"]
columns = [dict(name=c, id=name + c) for c in cols]
Ports = DataTable(
    id=name + "ports",
    columns=columns,
    style_header=style_header,
    #style_as_list_view=True,
    style_data_conditional=style_data_conditional,
)
Ports = dcc.Loading(id=name + "loading2", children=[Ports], type="circle")

Corr = DataTable(
    id=name + "corr",
    style_header=style_header,
    style_data_conditional=style_data_conditional,
)
Corr = dcc.Loading(id=name + "loading3", children=[Corr], type="circle")

mindate_label = html.Div("Actual date range:")
mindate = dcc.Loading(html.Div(id=name+"mindate", style=text_style), type="circle")
mindate_label = dbc.Col(mindate_label, md=6)
mindate = dbc.Col(mindate, md=6)
daterow = dbc.Row([mindate_label, mindate])

cola = dbc.Col(html.Div("Allow short sales"), md=6)
colb = dbc.Col(Radio, md=6)
Radio = dbc.Row([cola, colb], align="end")
middle = dbc.Col([slider1, slider2, html.Br(), Radio], md=4)

right = dbc.Col([slider0, html.Br(), daterow, html.Br(), html.Br(), Btn], md=4)


left = dbc.Col(
    [
    dbc.Label("Number of Tickers"),
    Drop,
    html.Br(),
    dbc.Label("Enter Tickers"),
    Tickers
    ],
    md=4
)


row = dbc.Row([left, middle, right], align="top")

left = dbc.Col([dbc.Label("Optimal Portfolios"), Ports], md=6)
right = dbc.Col(graph, md=6)
row2 = dbc.Row([left, right], align="top")

Corr = dbc.Row(dbc.Col([dbc.Label("Correlation Matrix"), Corr]))

body = html.Div([
    row,
    html.Hr(),
    row2,
    Corr,
    ticker_interval # Add interval to the layout
])
layout = Layout(
    title=title,
    runtitle=runtitle,
    chapter=chapter,
    chapter_url=chapter_url,
    urls=urls,
    text=text,
    body=body,
)

# Callback to reset the interval timer when ticker input changes
@callback(
    Output(name + "-ticker-input-interval", "n_intervals"),
    Input(name + "tickers", "data_timestamp"),
    prevent_initial_call=True
)
def reset_ticker_interval(_data_timestamp):
    return 0

# Main callback
@callback(
    Output(name + "mindate", "children"),
    Output(name + "fig", "figure"),
    Output(name + "ports", "data"),
    Output(name + "corr", "data"),
    Output(name + "tickers", "data"),
    [Input(i, "value") for i in inputs], # dates, rs, extra, radio from original inputs
    Input(name + "Num", "value"), # N
    Input(name + "-ticker-input-interval", "n_intervals"), # n_intervals from the new dcc.Interval
    State(name + "tickers", "data_timestamp"), # data_timestamp (as State)
    State(name + "tickers", "data"), # trows (ticker data)
    Input(name + 'btn', 'n_clicks') # n_clicks for the button
)
def call(dates, rs, extra, radio, N, n_intervals, data_timestamp, trows, n_clicks):
    # Determine which input triggered the callback
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Only proceed if the interval completed OR the button was clicked
    # and not on initial load or if data_timestamp is None (which can happen)
    if n_clicks == 0 and triggered_id != (name + "-ticker-input-interval"):
        if n_intervals == 0: # Interval was reset, or initial load
            raise PreventUpdate


    if data_timestamp is None and triggered_id == (name + "-ticker-input-interval"):
        # Interval fired but no actual ticker data change recently, prevent update
        raise PreventUpdate

    M = len(trows)
    if N > M:
        trows += [{name+"t": None} for i in range(N-M)]
        # Prevent update if only the number of tickers changed to be > M, but no actual ticker input yet
        # Or if the interval fired without a ticker change.
        if triggered_id == (name + "-ticker-input-interval") and not any(list(d.values())[0] for d in trows if d.get(name+"t")):
             raise PreventUpdate
        return None, go.Figure(), None, None, trows
    else:
        trows = trows[:N]
        tickers = [list(d.values())[0] for d in trows] # Ensure you get the ticker string
        
        # Check if all ticker values are non-empty
        if all(isinstance(t, str) and t.strip() for t in tickers):
            try:
                text_val, fig_val, ports_val, corrs_val = figtbl(name, dates, rs, extra, radio, tickers)
                return text_val, fig_val, ports_val, corrs_val, trows
            except Exception as e:
                print(f"Error in figtbl: {e}") # Log error
                # Potentially return an error message to the user through one of the outputs
                return "Error processing tickers.", go.Figure(), None, None, trows
        else:
            # If some tickers are empty or None, and the trigger was the interval, prevent update.
            # If the trigger was something else (like N changing), allow trows update.
            if triggered_id == (name + "-ticker-input-interval"):
                raise PreventUpdate
            return None, go.Figure(), None, None, trows
