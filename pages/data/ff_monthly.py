from pandas_datareader import DataReader as pdr

# TEMPORARY: Ken French Data Library access is currently unavailable
# These variables will be None if the data cannot be accessed
try:
    ff3 = pdr('F-F_Research_Data_Factors','famafrench', start=1900)[0]/100
    ff5 = pdr('F-F_Research_Data_5_Factors_2x3','famafrench', start=1900)[0]/100
    Mom = pdr('F-F_Momentum_Factor','famafrench', start=1900)[0]/100
    ST_Rev = pdr('F-F_ST_Reversal_Factor','famafrench', start=1900)[0]/100
    LT_Rev = pdr('F-F_LT_Reversal_Factor','famafrench', start=1900)[0]/100
    ff48 = pdr("48_Industry_Portfolios", "famafrench", start=1900)[0]/100
except Exception as e:
    print(f"Warning: Unable to access Ken French Data Library: {e}")
    ff3 = None
    ff5 = None
    Mom = None
    ST_Rev = None
    LT_Rev = None
    ff48 = None
