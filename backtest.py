import yfinance as yf
import pandas as pd
from dates import ramadan_window

prices = yf.download("SPY", start="1993-01-01", auto_adjust=True)["Close"].squeeze()

rows = []
for y in range(1414, 1448):
    start, end = ramadan_window(y)
    start, end = pd.Timestamp(start), pd.Timestamp(end)

    before = prices[prices.index < start]
    during = prices[prices.index <= end]
    if before.empty:
        continue
    
    buy = before.iloc[-1]
    sell = during.iloc[-1]
    rows.append((y, start.date(), end.date(), buy, sell, sell/buy -1))

result = pd.DataFrame(rows, columns=["hijri_year", "start", "end", "buy", "sell", "return"])
print(result)
print("Average return per Ramadan window:", result["return"].mean())
