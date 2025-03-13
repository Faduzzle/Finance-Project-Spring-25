import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define a dictionary mapping sectors to lists of ETFs from various providers.
sector_etfs = {
    'Financials': ['XLF', 'VFH', 'IYF'],
    'Technology': ['XLK', 'VGT', 'IYW'],
    'Consumer Discretionary': ['XLY', 'VCR', 'IYC'],
    'Consumer Staples': ['XLP', 'VDC', 'IYK'],
    'Industrials': ['XLI', 'VIS', 'IYJ'],    # Replace 'VIS' if necessary with a valid ETF ticker.
    'Energy': ['XLE', 'VDE', 'IYE'],
    'Health Care': ['XLV', 'VHT', 'IYH'],
    'Materials': ['XLB', 'VAW', 'IYM'],
    'Utilities': ['XLU', 'VPU', 'IDU'],
    'Real Estate': ['XLRE', 'VNQ', 'IYR']
}

# Create a sorted list of all unique ETFs needed.
all_etfs = sorted({etf for etfs in sector_etfs.values() for etf in etfs})

# Download historical adjusted close prices for all ETFs using yfinance.
# You can adjust the start and end dates as required.
data = yf.download(all_etfs, start="2020-01-01", end="2023-01-01")
prices = data['Adj Close']

# Calculate daily percentage returns and drop the first row of NaN values.
returns = prices.pct_change().dropna()

# Initialize a DataFrame to store composite (average) sector returns.
sector_returns = pd.DataFrame(index=returns.index)

# For each sector, compute the average daily return across the ETFs available.
for sector, etf_list in sector_etfs.items():
    # Only include ETFs that were successfully downloaded.
    available_etfs = [etf for etf in etf_list if etf in returns.columns]
    sector_returns[sector] = returns[available_etfs].mean(axis=1)

# Convert the daily returns into a sector index.
# The index is calculated by compounding the returns and rebasing to 100.
sector_indices = (1 + sector_returns).cumprod() * 100

# Display the first few rows of the sector indices.
print(sector_indices.head())

# Plot the sector indices for visual inspection.
plt.figure(figsize=(12, 6))
for sector in sector_indices.columns:
    plt.plot(sector_indices.index, sector_indices[sector], label=sector)
plt.title("Sector Indices Based on Composite ETF Returns")
plt.xlabel("Date")
plt.ylabel("Index Value")
plt.legend()
plt.show()
