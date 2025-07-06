import pandas as pd
import quandl
quandl.ApiConfig.api_key = "f-5zoU2G4zzHaUtkJ7BY"
from pandas_datareader import DataReader as pdr

# inflation
inflation = pdr("CPIAUCSL", "fred", start="1929-12-01")
inflation = inflation.resample("Y").last().iloc[:-1]
inflation.index = [x.year for x in inflation.index]
inflation.columns = ['Inflation']
inflation = inflation.pct_change().dropna()

# gold
d = quandl.get("LBMA/GOLD")['USD (AM)']
gold = d.resample('Y').last().iloc[:-1]
gold.index = [x.year for x in gold.index]
gold.loc[1967] = d.iloc[0]
gold = gold.sort_index().pct_change().dropna()
gold.name = 'Gold'

real = pd.read_csv('https://www.dropbox.com/s/5t4xmx7ixcqx7ss/real_sbb.csv?dl=1', index_col=['Year'])
nominal = pd.read_csv('https://www.dropbox.com/s/hgwte6swx57jqcv/nominal_sbb.csv?dl=1', index_col=['Year'])

ff3 = pdr('F-F_Research_Data_Factors','famafrench', start=1900)[0]/100
ff5 = pdr('F-F_Research_Data_5_Factors_2x3','famafrench', start=1900)[0]/100
Mom = pdr('F-F_Momentum_Factor','famafrench', start=1900)[0]/100
ST_Rev = pdr('F-F_ST_Reversal_Factor','famafrench', start=1900)[0]/100
LT_Rev = pdr('F-F_LT_Reversal_Factor','famafrench', start=1900)[0]/100
ff48 = pdr("48_Industry_Portfolios", "famafrench", start=1900)[0]/100

# code to read from Damodaran
'''
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
file = "http://www.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls"
sheet = "Returns by year"
df = pd.read_excel(file, sheet_name=sheet, skiprows=16, header=[0, 1])
col1 = ("Unnamed: 0_level_0", "Year")
indx = df[df[col1].isna()].index[0]
df = df.iloc[:indx].set_index(col1)
df.index.name = "Year"
df.dtype = "float"
df.index = [int(x) for x in df.index]

# this is for portfolios/optimal_sb and risk/sbb_real
real = df["Annual Real Returns on"].copy()
real = real[real.columns[1:5]]
real.columns = ["S&P 500", "TBills", "Treasuries", "Corporates"]

# this is for risk/sbb and risk/matrix-correlation
nominal = df["Annual Returns on Investments in"].copy()
nominal = nominal[nominal.columns[:4]]
nominal.columns = ["SP500", "TBills", "TBonds", "Corporates"]
'''
