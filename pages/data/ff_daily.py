from pandas_datareader import DataReader as pdr

# TEMPORARY: Ken French Data Library access is currently unavailable
# This variable will be None if the data cannot be accessed
try:
    ff3_daily = pdr('F-F_Research_Data_Factors_daily','famafrench', start=1900)[0]/100
except Exception as e:
    print(f"Warning: Unable to access Ken French Data Library: {e}")
    ff3_daily = None

