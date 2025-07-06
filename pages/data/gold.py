import quandl
quandl.ApiConfig.api_key = "f-5zoU2G4zzHaUtkJ7BY"


d = quandl.get("LBMA/GOLD")['USD (AM)']
gold = d.resample('Y').last().iloc[:-1]
gold.index = [x.year for x in gold.index]
gold.loc[1967] = d.iloc[0]
gold = gold.sort_index().pct_change().dropna()
gold.name = 'Gold'
