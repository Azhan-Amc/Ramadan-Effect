import yfinance as yf
import pandas as pd
import numpy as np
from dates import ramadan_window

TICKERS = {
    "Turkey": "XU100.IS",
    "Malaysia": "^KLSE",
    "Indonesia": "^JKSE",
    "Saudi Arabia": "^TASI.SR",
}


def get_prices(ticker):
    data = yf.download(ticker, start="1985-01-01", auto_adjust=True, progress=False)
    close = data["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close = close.dropna()
    close = close[close > 0]
    if close.index.tz is not None:
        close.index = close.index.tz_localize(None)
    return close.astype(float)


def run_test(ticker, n_sims=5000):
    prices = get_prices(ticker)
    if len(prices) < 500:
        return None  # not enough data

    rows = []
    for y in range(1400, 1448):
        start, end = ramadan_window(y)
        start, end = pd.Timestamp(start), pd.Timestamp(end)
        if start <= prices.index[0] or end >= prices.index[-1]:
            continue
        buy = float(prices[prices.index < start].iloc[-1])
        sell = float(prices[prices.index <= end].iloc[-1])
        n_days = int(((prices.index >= start) & (prices.index <= end)).sum())
        rows.append((y, n_days, sell / buy - 1))

    df = pd.DataFrame(rows, columns=["year", "days", "ret"])
    if len(df) < 5:
        return None

    values = prices.values
    np.random.seed(42)
    sims = []
    for _ in range(n_sims):
        rets = []
        for n in df["days"]:
            i = np.random.randint(0, len(values) - n - 1)
            rets.append(values[i + n] / values[i] - 1)
        sims.append(np.mean(rets))
    sims = np.array(sims)

    ram_avg = df["ret"].mean()
    return {
        "windows": len(df),
        "first_year": prices.index[0].year,
        "ramadan_avg_%": round(ram_avg * 100, 2),
        "random_avg_%": round(sims.mean() * 100, 2),
        "share_random_beats": round((sims >= ram_avg).mean(), 3),
        "pct_positive": round((df["ret"] > 0).mean() * 100, 1),
    }


if __name__ == "__main__":
    out = []
    for name, ticker in TICKERS.items():
        try:
            res = run_test(ticker)
        except Exception as e:
            print(name, ticker, "failed:", e)
            continue
        if res is None:
            print(name, ticker, "- not enough data, skipped")
            continue
        res["market"] = name
        res["ticker"] = ticker
        out.append(res)

    if out:
        print(pd.DataFrame(out).to_string(index=False))
         
