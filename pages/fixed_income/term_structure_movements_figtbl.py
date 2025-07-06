from pages.data.yield_changes import yield_changes


def figtbl(dates):
    start = str(dates[0]) + "-01"
    stop = str(dates[1]) + "-12"
    df = yield_changes.loc[start:stop]

    tbl1 = df.describe().round(2).iloc[1:3]
    tbl1 = tbl1.rename(index={"std": "std dev"}).reset_index()
    tbl1.columns = [
        "statistic",
        "1-Year",
        "2-Year",
        "3-Year",
        "5-Year",
        "10-Year",
        "30-Year",
    ]

    tbl2 = df.corr().applymap("{0:.02f}".format)
    tbl2.index = tbl1.columns[1:]
    tbl2 = tbl2.reset_index()
    tbl2.columns = [""] + tbl1.columns.to_list()[1:]
    return tbl1, tbl2
