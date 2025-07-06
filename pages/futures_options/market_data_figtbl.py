import yfinance as yf
from datetime import datetime, timezone

# convert datetime to now minus datetime
def timesince(x):
    x = datetime.now(timezone.utc) - x
    total_seconds = int(x.total_seconds())
    days, remainder = divmod(total_seconds, 24 * 60 * 60)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return "{} days, {} hrs, {} mins, {} secs".format(days, hours, minutes, seconds)


def price_maturities(ticker):
    tick = yf.Ticker(ticker.upper())
    close = tick.history().iloc[-1].Close
    string = "Last {} price was ${:.2f}.".format(ticker.upper(), close)
    return string, list(tick.options)


def figtbl(ticker, kind, maturity):
    tick = yf.Ticker(ticker)
    df = (
        tick.option_chain(maturity).calls
        if kind == "call"
        else tick.option_chain(maturity).puts
    )
    df["Time Since Last Trade"] = df.lastTradeDate.map(timesince)
    cols = [
        "strike",
        "bid",
        "ask",
        "lastPrice",
        "change",
        "percentChange",
        "Time Since Last Trade",
        "volume",
        "openInterest",
        "impliedVolatility",
    ]
    df = df[cols].copy()
    df["impliedVolatility"] = df["impliedVolatility"].map("{:.1%}".format)
    df["change"] = df["change"].round(2)
    df["percentChange"] = (df["percentChange"]/100).map("{:.1%}".format)
    df.columns = [
        "Strike",
        "Bid",
        "Ask",
        "Last Price",
        "Change",
        "% Change",
        "Time Since Last Trade",
        "Volume",
        "Open Interest",
        "Implied Volatility",
    ]
    return df
