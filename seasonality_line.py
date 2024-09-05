# -*- coding: utf-8 -*-


import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


# Set pandas display options to show all rows
pd.set_option('display.max_rows', None)  # None means unlimited rows


ticker = "btc-usd"
timeframe = 10 #years


# Calculate the dates for download
end_date = datetime.today()
start_date = end_date - timedelta(days=timeframe*365)

# Format the dates as strings
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")   

# Download the Daily data
df = yf.download(ticker, start=start_date_str, end=end_date_str, interval='1d')

# Calculate the multiplier column
df["multiplier"] = ((df["Close"] / df["Open"])) 

# Format the M-D column
df["M-D"] = df.index.strftime('%m-%d')  # Change index format to month-day

# Group by M-D and calculate the means of the associated multiplier values
grouped_df = df.groupby("M-D")["multiplier"].mean()
grouped_df = grouped_df.reset_index()

# Calculate the cumulative product
grouped_df["cumprod"] = grouped_df["multiplier"].cumprod()
print(grouped_df.head(100))

plt.plot(grouped_df["M-D"], grouped_df["cumprod"])
# Format the x-axis to show full month name and year
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%B'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
plt.xticks(rotation=90)
plt.show()
