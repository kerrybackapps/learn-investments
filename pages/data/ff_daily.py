from pandas_datareader import DataReader as pdr

ff3_daily = pdr('F-F_Research_Data_Factors_daily','famafrench', start=1900)[0]/100

