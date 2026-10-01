import yfinance as yf
import pandas as pd
import numpy as np
from dates import ramadan_window

TICKERS = {
    "Turkey": "XU100.IS",
    "Malaysia": "^KLSE",
    "Indonesia": "^JKSE",
}

N_SIMS = 5000


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


def ramadan_windows(prices):
    rows = []
    for y in range(1400, 1448):
        start, end = ramadan_window(y)
        start, end = pd.Timestamp(start), pd.Timestamp(end)
        if start <= prices.index[0] or end >= prices.index[-1]:
            continue
        buy = float(prices[prices.index < start].iloc[-1])
        sell = float(prices[prices.index <= end].iloc[-1])
        n_days = int(((prices.index >= start) & (prices.index <= end)).sum())
        rows.append((start, n_days, sell / buy - 1))
    return pd.DataFrame(rows, columns=["start", "days", "ret"])


def simulate(values, days, rng):
    """Average return of random windows with the same lengths, repeated N_SIMS times."""
    per_window = []
    for n in days:
        i = rng.integers(0, len(values) - n - 1, size=N_SIMS)
        per_window.append(values[i + n] / values[i] - 1)
    return np.mean(per_window, axis=0)


PERIODS = {
    "1989-2007": lambda p: p[p.index <= "2007-12-31"],
    "2008-now": lambda p: p[p.index >= "2008-01-01"],
}


def in_period(df, name):
    if name == "1989-2007":
        return df[df["start"].dt.year <= 2007]
    return df[df["start"].dt.year >= 2008]


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    rows = []
    pooled = {name: {"ram": [], "sims": []} for name in PERIODS}

    for market, ticker in TICKERS.items():
        try:
            prices = get_prices(ticker)
            wins = ramadan_windows(prices)
        except Exception as e:
            print(market, ticker, "failed:", e)
            continue

        for name, cut in PERIODS.items():
            sub_prices = cut(prices)
            sub_wins = in_period(wins, name)
            if len(sub_wins) < 5 or len(sub_prices) < 250:
                print(market, name, "- not enough data, skipped")
                continue

            sims = simulate(sub_prices.values, sub_wins["days"], rng)
            ram_avg = sub_wins["ret"].mean()
            pooled[name]["ram"].append(ram_avg)
            pooled[name]["sims"].append(sims)

            rows.append({
                "market": market,
                "period": name,
                "windows": len(sub_wins),
                "ramadan_avg_%": round(ram_avg * 100, 2),
                "random_avg_%": round(sims.mean() * 100, 2),
                "share_random_beats": round((sims >= ram_avg).mean(), 3),
            })

    for name, d in pooled.items():
        if d["ram"]:
            ram = np.mean(d["ram"])
            sims = np.mean(d["sims"], axis=0)
            rows.append({
                "market": "POOLED (equal weight)",
                "period": name,
                "windows": "-",
                "ramadan_avg_%": round(ram * 100, 2),
                "random_avg_%": round(sims.mean() * 100, 2),
                "share_random_beats": round((sims >= ram).mean(), 3),
            })

    print(pd.DataFrame(rows).to_string(index=False))