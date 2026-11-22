# Did the Ramadan Effect Survive Its Own Discovery?

**Do stock markets in Muslim-majority countries still earn unusually high returns during Ramadan, now that the effect is published and known?**

## Paper

Chowdhry, Mohammad Azhan (2026). *Did the Ramadan Effect Survive Its Own Discovery? Out-of-Sample Evidence from Turkey, Malaysia, Indonesia and the United States, 1990–2026.* Islamic Investment Research Working Paper No. 2026-02. https://doi.org/10.5281/zenodo.24328963

- IIR page: https://islamicinvestmentresearch.com/paper.html?n=2026-02
- Original study tested here: Białkowski, Etebari and Wisniewski (2012), "Fast profits: Investor sentiment and stock returns during Ramadan", *Journal of Banking & Finance*. SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1470048

## Main finding

The original study found that, in 14 Muslim-majority markets from 1989 to 2007, Ramadan returns were much higher and less volatile than the rest of the year. Its sample ends in 2007, so almost two decades of later data have never been checked.

| Period | Markets | Ramadan windows (avg) | Random windows (avg) | One-sided p-value |
| --- | --- | --- | --- | --- |
| 1989–2007 (original sample) | Turkey, Malaysia, Indonesia, pooled | **5.27%** | 1.69% | 0.025 |
| 2008–2026 (after publication) | Turkey, Malaysia, Indonesia, pooled | **−0.06%** | 0.82% | 0.867 |
| 1994–2026 (control) | United States (SPY) | 0.81% | 0.94% | 0.57 |

- **The effect reproduces in the original period.** Ramadan windows beat random windows of the same length, as the original study reported.
- **It disappeared afterwards.** From 2008 on, Ramadan underperformed its random benchmark in every market tested.
- **The US control shows nothing**, as expected for a market where Ramadan should not matter.
- **Conclusion:** the Ramadan effect is an anomaly that vanished after its sample period. It should not be traded, and it does not justify a seasonal tilt in a Shariah-compliant equity portfolio.

## Method

- **Rule:** buy the index at the last close before Ramadan begins, sell at the last close of Ramadan (the day before Eid al-Fitr).
- **Ramadan dates:** converted from the Hijri calendar with `hijri-converter` (`dates.py`).
- **Benchmark:** each market's Ramadan returns are compared with 5,000 sets of random windows of the same lengths, drawn from the same market and period. The p-value is the share of random sets whose average return is at least the Ramadan average (one-sided, non-parametric).
- **Pooling:** the three markets are combined with equal weight.
- **Split:** 1989–2007 matches the original study's sample; 2008–2026 is the out-of-sample period.
- **Random seed:** 42, so the random windows are the same on every run.

## Data

Daily closing levels from Yahoo Finance, downloaded with `yfinance`:

| Market | Ticker |
| --- | --- |
| Turkey | `XU100.IS` (BIST 100) |
| Malaysia | `^KLSE` (FTSE Bursa Malaysia KLCI) |
| Indonesia | `^JKSE` (Jakarta Composite) |
| United States (control) | `SPY` |

Prices are downloaded when the scripts run and are not stored in this repository.

## How to run

```
pip install -r requirements.txt
python split.py       # main result: 1989-2007 vs 2008-2026, per market and pooled
python backtest.py    # US control (SPY)
python markets.py     # full-period result for each market
python dates.py       # prints the Ramadan start and end dates used
```

Yahoo Finance revises past data from time to time, so a new download can differ slightly from the figures above.

## Files

| File | What it does |
| --- | --- |
| `dates.py` | Converts each Hijri year's Ramadan to Gregorian start and end dates |
| `split.py` | The main test: each market and the pooled average, split into 1989–2007 and 2008–2026 |
| `backtest.py` | The same test on SPY, as a control |
| `markets.py` | The test over each market's full history. It also tries Saudi Arabia (`^TASI.SR`), which is not part of the paper's sample |
| `requirements.txt` | Package versions used |

## Limitations

- The indices are price indices: dividends are not included, and returns are before trading costs.
- An index cannot be bought directly; a real trade would use an index fund or ETF, with tracking error and costs.
- Ramadan dates follow the calculated Umm al-Qura calendar. In countries that start Ramadan by moon sighting, the actual start can differ by a day.
- The test covers three of the original study's 14 markets, so it checks part of the original sample, not all of it.
- Free Yahoo Finance data for the early 1990s may be less reliable than recent data.

## Use of AI

The author chose the research question, made all methodological decisions and ran the analysis. Code and text were drafted with the assistance of an AI model (Claude, Anthropic) and reviewed by the author.
