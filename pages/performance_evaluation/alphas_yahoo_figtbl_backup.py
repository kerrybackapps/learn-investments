import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from pandas_datareader import DataReader as pdr
from pages.formatting import largefig


# get monthly market excess return and risk-free rate starting in 1970 from French's data library
ff = pdr('F-F_Research_Data_Factors','famafrench',start=1970)[0]
#Convert FF data to decimal
for c in ff.columns:
    ff[c]= ff[c]/100


def data(ticker,dates):
    # date is a list of years
    ticker = ticker.upper()
    start_date = dates[0]
    stop_date  = dates[1]
        
    ret = pdr(ticker, 'yahoo', start=start_date, end=stop_date )
    ret = ret['Adj Close'].resample('M').last()
    ret = ret.pct_change()
    ret.index = ret.index.to_period('M')
    ret.name = 'ret'
    df = ff.join(ret, how="inner")
    df['ret'] -= df.RF
    df = df[['Mkt-RF', 'ret']].reset_index()
    df.columns = ['date', 'mkt', 'ret']
    df['date'] = df.date.astype(str)
    return df


def figtbl(ticker,dates):
    ticker = ticker.upper()
    df = data(ticker,dates)
    fig = px.scatter(
        df,
        x="mkt",
        y="ret",
        trendline="ols",
        hover_data=dict(ret=False, mkt=False, date=False),
        hover_name="date",
    )
    fig.layout.xaxis["title"] = "Market Excess Return"
    fig.layout.yaxis["title"] = ticker.upper() + " Excess Return"
    fig.update_traces(
        marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
        selector=dict(mode="markers"),
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_xaxes(tickformat=".0%")
    # fig.show()
    
    # run regression of excess return on market excess return and get beta
    result = sm.OLS(df.ret,sm.add_constant(df['mkt']),missing='drop').fit()
    alpha = result.params['const']*12 *100
    beta  = result.params['mkt']
    t_alpha      = result.tvalues['const']
    rsquared_adj = result.rsquared_adj
    
    alpha  =np.round(alpha,3)
    beta   =np.round(beta,3)
    t_alpha=np.round(t_alpha,3)
    rsquared_adj=np.round(rsquared_adj,3)
    
    indx = [
        ticker + " Alpha (Annual %)",
        "t-statistic of Alpha",
        "Beta",
        "Adj. R-Squared",
    ]
    tbl = pd.DataFrame(dtype=float, index=indx, columns=["values"])
    tbl.loc[ticker + " Alpha (Annual %)"] = alpha
    tbl.loc["t-statistic of Alpha"] = t_alpha
    tbl.loc["Beta"] = beta
    tbl.loc["Adj. R-Squared"] = rsquared_adj
    # print(tbl)
    tbl = tbl.reset_index().to_dict("records")

    return largefig(fig), tbl
