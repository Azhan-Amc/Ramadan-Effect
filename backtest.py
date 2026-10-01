import yfinance as yf
import pandas as pd
import numpy as np
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
    rows.append((y, start.date(), end.date(), buy, sell, sell / buy - 1))

result = pd.DataFrame(rows, columns=["hijri_year", "start", "end", "buy", "sell", "return"])
print(result)
print("Average return per Ramadan window:", result["return"].mean())

# ---- random-window test ----
np.random.seed(42)
values = prices.values

lengths = []
for y in result["hijri_year"]:
    s, e = ramadan_window(y)
    s, e = pd.Timestamp(s), pd.Timestamp(e)
    lengths.append(((prices.index >= s) & (prices.index <= e)).sum())

ramadan_avg = result["return"].mean()

sim_avgs = []
for _ in range(5000):
    rets = []
    for n in lengths:
        i = np.random.randint(0, len(values) - n - 1)
        rets.append(values[i + n] / values[i] - 1)
    sim_avgs.append(np.mean(rets))

sim_avgs = np.array(sim_avgs)
print("Ramadan average:", round(ramadan_avg * 100, 2), "%")
print("Random windows average:", round(sim_avgs.mean() * 100, 2), "%")
print("Share of random runs that beat Ramadan:", (sim_avgs >= ramadan_avg).mean())