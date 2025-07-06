from pandas_datareader import DataReader as pdr

files = ["DGS" + x for x in ["1", "2", "3", "5", "10", "30"]]
yield_changes = 100 * pdr(files, "fred", start=1920).dropna()
yield_changes = yield_changes.resample("M").last().diff()
yield_changes.index = yield_changes.index.to_period('M').astype(str)
yield_changes = yield_changes.dropna()
yield_changes.columns = [int(x[3:]) for x in yield_changes.columns]

