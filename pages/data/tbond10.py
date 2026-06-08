from pandas_datareader import DataReader as pdr

try:
    dgs = pdr("DGS10", "fred", start=1920)
    dgs3mo = pdr("DGS3mo", "fred", start=1920)
except Exception as e:
    print(f"Warning: Unable to fetch Treasury yield data from FRED: {e}")
    dgs = None
    dgs3mo = None
