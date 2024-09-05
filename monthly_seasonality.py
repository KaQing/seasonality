
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ticker = "SI=F"
timeframe = 15 #years


# Calculate the start date as today minus 3 years
end_date = datetime.today()
start_date = end_date - timedelta(days=timeframe*365)

# Format the dates as strings
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")   

# Download the monthly data
df = yf.download(ticker, start=start_date_str, end=end_date_str, interval='1mo')
df["1M Change"] = ((df["Close"] / df["Open"]) - 1) * 100

# Create new column for Months
df["Month"] = df.index.strftime('%m')

# Group by month
grouped_by_month = df.groupby(df["Month"])
aggregated_mean = grouped_by_month.agg("mean")

# Sort values by month
df = df.sort_values(by="Month")

# Get median values for the color map
median_values = df.groupby('Month')['1M Change'].median().reset_index()
median_values.sort_values(by='1M Change', inplace=True)

# Calculate the color map
colors = sns.color_palette("RdYlGn", n_colors=len(median_values))
color_map = {month: colors[i] for i, month in enumerate(median_values['Month'])}

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(15, 6),  sharex=True)

# Create a sns lineplot for the mean values with the confidence interval
sns.lineplot(x='Month', y='1M Change', data=df, ax=ax1)

# Annotate mean values
for index, row in aggregated_mean.iterrows():
    ax1.text(index, row['1M Change'], f'{row["1M Change"]:.2f}', 
            horizontalalignment='center', verticalalignment='bottom', 
            color='black', fontsize=10)

# Create a boxplot chart
sns.boxplot(x='Month', y='1M Change', data=df, palette=color_map, ax=ax2)

# Annotate median values
median_values.sort_values(by='Month', inplace=True)
for i, median in enumerate(median_values['1M Change']):
    ax2.text(i, median, f'{median:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=10, color='blue', weight='bold')

# Plot the chart with titles
ax1.set_title(f"Mean monthly percentage change for {ticker}")
plt.title(f"Median monthly percentage change for {ticker}")
plt.show()
