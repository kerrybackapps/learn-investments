from pandas_datareader import DataReader as pdr

# inflation
inflation = pdr("CPIAUCSL", "fred", start="1929-12-01")
inflation = inflation.resample("Y").last().iloc[:-1]
inflation.index = [x.year for x in inflation.index]
inflation.columns = ['Inflation']
inflation = inflation.pct_change().dropna()
