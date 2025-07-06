import pandas as pd

# real = pd.read_csv('https://www.dropbox.com/s/5t4xmx7ixcqx7ss/real_sbb.csv?dl=1', index_col=['Year'])
# nominal = pd.read_csv('https://www.dropbox.com/s/hgwte6swx57jqcv/nominal_sbb.csv?dl=1', index_col=['Year'])
real = pd.read_csv("assets/real_sbb.csv", index_col=["Year"])
nominal = pd.read_csv("assets/nominal_sbb.csv", index_col=["Year"])
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
