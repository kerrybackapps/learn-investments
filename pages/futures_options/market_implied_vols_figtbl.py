import yfinance as yf
import plotly.graph_objects as go
from datetime import timedelta
from pages.formatting import largefig


def price_maturities(ticker):
    tick = yf.Ticker(ticker)
    close = tick.history().iloc[-1].Close
    string = f"Last {ticker.upper()} price was ${close:.2f}."
    return string, list(tick.options)


def figtbl(ticker, maturity):
    tick = yf.Ticker(ticker)
    calls = tick.option_chain(maturity).calls
    puts = tick.option_chain(maturity).puts

    now = max(calls.lastTradeDate.max(), puts.lastTradeDate.max())
    calls = calls[calls.lastTradeDate >= now - timedelta(hours=24)]
    puts = puts[puts.lastTradeDate >= now - timedelta(hours=24)]

    string = "call implied vol = %{y:.1%}<extra></extra>"
    trace1 = go.Scatter(x=calls.strike,
                        y=calls.impliedVolatility,
                        mode="lines+markers",
                        hovertemplate=string,
                        name="Call"
                        )

    string = "put implied vol = %{y:.1%}<extra></extra>"
    trace2 = go.Scatter(x=puts.strike,
                        y=puts.impliedVolatility,
                        mode="lines+markers",
                        hovertemplate=string,
                        name="Put"
                        )

    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_yaxes(title='Implied Volatility', tickformat=".0%")
    fig.update_xaxes(title="Strike", tickprefix="$")
    fig.update_layout(hovermode="x unified")
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.45))

    return largefig(fig, showlegend=True)

