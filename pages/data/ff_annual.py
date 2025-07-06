from pandas_datareader import DataReader as pdr

ff3_annual = pdr('F-F_Research_Data_Factors','famafrench', start=1900)[1]/100

'''
ff5 = pdr('F-F_Research_Data_5_Factors_2x3','famafrench', start=1900)[0]/100
Mom = pdr('F-F_Momentum_Factor','famafrench', start=1900)[0]/100
ST_Rev = pdr('F-F_ST_Reversal_Factor','famafrench', start=1900)[0]/100
LT_Rev = pdr('F-F_LT_Reversal_Factor','famafrench', start=1900)[0]/100
ff48 = pdr("48_Industry_Portfolios", "famafrench", start=1900)[0]/100
'''
