from pandas_datareader import DataReader as pdr

dgs = pdr("DGS10", "fred", start=1920)
dgs3mo = pdr("DGS3mo", "fred", start=1920)
