# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:02:49 2022

@author: kerry
"""
import numpy as np
import pandas as pd
import base64
import io
import plotly.graph_objects as go
import plotly.express as px
import datapane as dp
from pandas_datareader import DataReader as pdr
import statsmodels.api as sm
from pages.data.ff_monthly import ff5, Mom, ST_Rev, LT_Rev
from pages.formatting import smallfig
from scipy.stats import ttest_1samp as ttest

facts = pd.concat((ff5, Mom, ST_Rev, LT_Rev), axis=1).dropna()
factors = facts.drop(columns='RF').columns.to_list()

def boxplot(contribs):

    fig = go.Figure()
    for source in contribs.columns:
        trace = go.Box(y=contribs[source], name=source)
        fig.add_trace(trace)

    fig.update_yaxes(tickformat='.0%', title='Monthly Return')
    fig.update_xaxes(title="Sources of Return")
    return smallfig(fig)

def cumplot(contribs, skip=None):

    cum = (1 + contribs).cumprod()
    cum = cum.reset_index()
    cum.Date = cum.Date.astype(str)

    fig = go.Figure()
    cols = [x for x in cum.columns if x!='Date']
    if skip:
        cols = [x for x in cols if x not in skip]
    for source in cols:
        trace = go.Scatter(x=cum.Date, y=cum[source],
                           hovertemplate=source + ": %{y:.2f}<extra></extra>",
                           name=source)
        fig.add_trace(trace)

    fig.update_yaxes(title='Compound Return')
    fig.update_xaxes(title="Date")
    fig.update_layout(hovermode='x unified')
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return smallfig(fig, showlegend=True)


def figtbl(benchmark, contents, filename, modified):

    # RETURNS DATA

    if contents is not None:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        else:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        df.columns = ["Date", "Ret"]
        df["Date"] = pd.to_datetime(df["Date"]).dt.to_period("M")
        df = df.set_index("Date")

        if benchmark=="Market Index":
            benchmark = "Mkt"
            df = pd.concat((df, facts), axis=1).dropna()
            df['Ret-RF'] = df.Ret - df.RF
            df['Mkt'] = df['Mkt-RF'] + df.RF
            bm = 'Mkt-RF'
        else:
            benchmark = benchmark.split(' ')[0].upper()
            bench = pdr(benchmark, "yahoo", start=1970)
            bench = bench['Adj Close'].resample('M').last().pct_change().dropna()
            bench.name = benchmark
            bench.index = bench.index.to_period('M')
            df = pd.concat((df, facts, bench), axis=1).dropna()
            df['Ret-RF'] = df.Ret - df.RF
            bm = benchmark + '-RF'
            df[bm] = df[benchmark] - df.RF

        factors[0] = bm
        sources = factors.copy()
        sources[0] = benchmark

        # RAW

        xrets = 100 * 100 * (df['Ret'] - df[benchmark])
        raw_mn = xrets.mean()
        raw_sd = xrets.std()
        raw_info = raw_mn / raw_sd
        raw_t, raw_p = ttest(xrets, 0)

        tbl = pd.DataFrame(index=[0], columns=['mean', 'std err', 't stat', 'p value', 'info ratio'])
        for stat, col in zip([raw_mn, raw_mn / raw_t, raw_t, raw_p], ['mean', 'std err', 't stat', 'p value']):
            tbl[col] = f'{stat:.2f}'
        tbl['info ratio'] = f'{raw_info:.2%}'
        raw_tbl = tbl.style.hide()


        contribs = pd.DataFrame(dtype=float, index=df.index, columns=['Active', 'Benchmark'])
        contribs['Benchmark'] = df[benchmark]
        contribs['Active'] = df['Ret'] - contribs['Benchmark']
        raw_box = boxplot(contribs)
        raw_cum = cumplot(contribs)

        # CAPM

        result = sm.OLS(df['Ret-RF'], sm.add_constant(df[bm])).fit()
        capm_r2 = result.rsquared

        tbl = (result.summary2().tables[1])
        tbl = tbl[tbl.columns[:-2]]
        tbl.columns = ['coef', 'std err', 't stat', 'p value']
        tbl.index = ['alpha', bm]
        tbl.loc['alpha', 'coef'] = 100 * 100 * tbl.loc['alpha', 'coef']
        tbl.loc['alpha', 'std err'] = 100 * 100 * tbl.loc['alpha', 'std err']
        tbl = tbl.round(2)
        tbl['info ratio'] = ''
        info = result.params['const'] / np.sqrt(result.mse_resid)
        tbl.loc['alpha', 'info ratio'] = f'{info:.2%}'
        capm_tbl = tbl

        contribs = pd.DataFrame(dtype=float, index=df.index, columns=['Active', 'Benchmark'])
        contribs['Benchmark'] = df[bm] * result.params[bm] + df['RF']
        contribs['Active'] = df['Ret'] - contribs['Benchmark']
        capm_box = boxplot(contribs)
        capm_cum = cumplot(contribs)


        df2 = df.copy()
        df2 = df2. reset_index()
        df2['Date'] = df2.Date.astype(str)

        fig = px.scatter(
        df2,
        x=bm,
        y="Ret-RF",
        trendline="ols",
        hover_data={x: False for x in df.columns.to_list()},
        hover_name="Date",
        )
        fig.layout.xaxis["title"] = "Monthly Benchmark Excess Return"
        fig.layout.yaxis["title"] = "Monthly Excess Return"
        fig.update_traces(
            marker=dict(size=12, line=dict(width=2, color="DarkSlateGrey")),
            selector=dict(mode="markers"),
        )
        fig.update_yaxes(tickformat=".0%")
        fig.update_xaxes(tickformat=".0%")
        fig.layout.template = "plotly_dark"
        capm_reg = fig

        # FAMA-FRENCH

        result = sm.OLS(df['Ret-RF'], sm.add_constant(df[factors])).fit()
        ff_r2 = result.rsquared

        tbl = (result.summary2().tables[1])
        tbl = tbl[tbl.columns[:-2]]
        tbl.columns = ['coef', 'std err', 't stat', 'p value']
        tbl.index = ['alpha'] + factors
        tbl.loc['alpha','coef'] = 100 * 100 * tbl.loc['alpha','coef']
        tbl.loc['alpha', 'std err'] = 100 * 100 * tbl.loc['alpha','std err']
        tbl = tbl.round(2)
        tbl['info ratio'] = ''
        info = result.params['const'] / np.sqrt(result.mse_resid)
        tbl.loc['alpha', 'info ratio'] = f'{info:.2%}'
        ff_tbl = tbl

        contribs = pd.DataFrame(dtype=float, index=df.index, columns=['Active']+sources)
        contribs[benchmark] = df[bm] * result.params[bm] + df['RF']
        for col in contribs.columns:
            if col not in ['Active', benchmark]:
                contribs[col] = df[col] * result.params[col]
        contribs['Active'] = df['Ret'] - contribs[sources].sum(axis=1)
        ff_box = boxplot(contribs)
        ff_cum = cumplot(contribs, skip=[benchmark])

        df = df.reset_index()
        df.Date = df.Date.astype(str)
        df = df[['Date', 'Ret'] + sources + ['RF']]

        raw_text = f""" 
        On this tab, the active return is defined to be the return minus the benchmark return.  The 
        standard deviation of the active return is called the tracking error, and the ratio of the
        mean active return to the tracking error is an information ratio.
        The mean active return and the standard error are expressed here in basis points per month, 
        and the information ratio is in percent per month. 
        """

        capm_text1 = f"""
        On this tab, the active return is defined to be the return in excess of the beta-adjusted
        benchmark return.  The beta-adjusted benchmark is the portfolio with a weight of 
        beta on the benchmark
        and one minus beta on the risk-free asset.  In the regression, the dependent variable 
        is the excess return over the risk-free
        rate, and the independent variable is the excess return of the benchmark over the risk-free
        rate.  With these definitions, the active return is
        the intercept (alpha) in the regression plus the residual risk.  The mean active return
        is the alpha, the tracking error is the standard deviation of the active return, and the
        information ratio is the ratio of the alpha to the tracking error.    The alpha and its 
        standard error
        are expressed here in basis points per month.  The information ratio is in percent
        per month.  The regression R-squared is {capm_r2:.1%}."""

        capm_text2 = """
        The figures show the sources of return.  The benchmark source is
        the return of the beta-adjusted benchmark.  The active source
        is the remaining part of the excess return (alpha plus residual risk).
        """

        ff_text1 = f"""
        On this tab, a beta-adjusted benchmark is computed using a multiple regression
        beta.  To compute the active return, we start with the return minus the beta-adjusted
        benchmark return.  We then adjust for other known sources of return (factors) by 
        subtracting the beta for the factor multiplied by the factor.  The remaining return is
        the active return, and it equals the intercept (alpha) plus the residual risk in the
        regression.  The mean active return is the alpha, the standard deviation of the active
        return is a tracking error, and the ratio of the alpha to the tracking error is an
        information ratio.  The alpha and its standard error
        are expressed here in basis points per month.  The information ratio is in percent
        per month.   The regression R-squared is {ff_r2:.1%}.
        """

        ff_text2 = """
        The figures show the sources of returns.  The benchmark source is the
        beta-adjusted benchmark return.  The factor sources are betas times
        factor returns.  The active return is the remaining part of the excess return
        (alpha plus residual risk).  The factors are size (SMB), value (HML), 
        profitability (RMW), investment (CMA), momentum (Mom), short-term 
        reversal (ST_Rev), 
        and long-term reversal (LT_Rev).  To improve the scale, the beta-adjusted benchmark
        return is not shown on the compound return plot.
        """

        report = dp.Report(
            dp.Page(title="Simple benchmark",
            blocks=[
                dp.Group(
                   dp.Group(raw_text, raw_tbl, columns=1),
                    raw_box,
                    raw_cum,
                    columns=3
                )
            ]
            ),
            dp.Page(
                title="Beta-adjusted benchmark",
                blocks=[dp.Group(
                    dp.Group(
                          dp.Text(capm_text1),
                            capm_tbl),
                    capm_reg, columns=2
                ),
                    dp.Text(capm_text2),
                    dp.Group(capm_box, capm_cum, columns=2)
                        ]
            ),
            dp.Page(
                title="Multi-factor analysis",
                blocks=[dp.Group(
                    dp.Group(
                        dp.Text(ff_text1),
                        ff_tbl),
                    dp.Group(
                        dp.Text(ff_text2),
                        ff_cum),
                        columns=2
                ),
                    dp.Group(ff_box)
                ]
            ),
            dp.Page(title='Data', blocks=[df])
        )

        fn = 'attribution.html'
        report.save('./tmp/' + fn)

        return fn
