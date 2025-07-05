# Gold Swing High-Low Based Strategy (5-Minute Timeframe)

Hi,  
Welcome to my project based on recent swing highs and lows from 5-minute Gold price data. The strategy aims to generate trading signals based on failed swing points followed by rapid pullbacks.

---

## 📌 Core Logic

The trading logic revolves around:

### 🟩 Swing Detection
- Detects minor swing highs/lows using a lookback and lookforward window, **eliminating look-ahead bias**.

### 🟩 Entry Logic (Refined)
- Strategy uses the **liquidity grab and run** concept to identify entries.
- Two valid signal types are used:
  1. **Same-Candle Entry**: The current candle both hunts liquidity (breaks the previous swing) and closes with confirmation (e.g., green for long).
  2. **Two-Candle Entry**: The **previous candle** breaks the swing, and the **current candle** confirms the reversal.
  
> ✅ Removing confirmation candle was tested — led to worse results, so the logic was dropped.

> ❌ **Twice-sized entries for same-candle signals** were tested but resulted in **worse outcomes than single-size entries**, so the larger size was dropped.

- **Long Entry Example**:
  - Candle low < previous swing low **AND** current candle closes bullish.
- **Short Entry Example**:
  - Candle high > previous swing high **AND** current candle closes bearish.

---

### 🟩 Scaling In
- If a new swing appears in favor of an ongoing trade, the position is scaled in, and SL is adjusted to the latest swing.
- This approach needs refinement due to low MFE issues.

---

### 🟩 Stop Loss Logic
- Uses a **stop loss multiplier** on candle height to give price room in volatile scenarios.
- Custom SL approach using: `x * (open - low.shift(1))` is implemented and showed improved results.

---

### 🟩 Take Profit
- Currently not implemented.
- Focus is on trailing SL or dynamic exit using structure changes or reversals.

---

## 🧠 Key Files & Modules

### 🔧 `swing_detection.py`
Detects minor swing highs and lows using a configurable window. Avoids look-ahead bias by considering both backward and forward candles. Used to generate CSVs for swing points.

### 🧪 Backtesting Notebooks
- `5min_initial_backtest.ipynb` — Continuous in-trade backtesting.
- `5min_2nd_refinement.ipynb` — SL refinement with nominal candle low.
- `scaling_included.ipynb` — Implements scaling based on new swing signals.

### 📊 `visualization.ipynb`
Plots strategy performance across different swing windows and stoploss multipliers.

### 📁 `backtester_csv.py`
Contains `SwingBacktesterWithScaling` class — main backtesting engine.

---
## 📁 Project Structure

Here’s an overview of the key folders in this repository:

### 📂 `Raw Data`
- Contains the original OHLC data of Gold on a **5-minute timeframe**.
- Used as the base input for all swing detection and backtesting.

### 📂 `swing_csvs`
- Contains CSV files where **minor swing highs/lows** are detected and added to the raw data.
- Generated using different **lookback/lookforward window sizes** via `swing_detection.py`.

### 📂 `all_trades`
- Contains trade data from all test cases using various **window sizes** and **stop loss multipliers**.
- Entry signals use **same-candle confirmation** (liquidity hunt and close in same candle).

### 📂 `all_trades_entry_on_either_two_candles`
- Contains trade logs where entries are allowed if:
  - The current candle does the liquidity grab and confirms, OR
  - The previous candle grabs liquidity and the current confirms.

### 📂 `all_trades_no_candle_confirmation`
- Contains trade data where **no green/red candle confirmation** was required for entries.
- This logic was **tested and later dropped** due to negative performance impact.

### 📂 `all_trades_two_candle_entry_with_two_lots_on_one_candle`
- Contains results where **two-lot size was used** if the signal appeared within **a single candle**.
- This variation was **dropped** after testing due to worse performance compared to single-size entries.

---
## 📄 Other Notes

- `refinement approaches.txt` — Log of refinements, failed ideas, and future plans.
- Major swing logic (not just minor) yet to be integrated.
- News sessions not excluded yet — planned as a key filter.
- Data source is limited — currently only 2 years of 5-minute Gold data.

---

## 🚧 Work in Progress

| Task | Status | Notes |
|------|--------|-------|
| SL refinement | ✅ | Basic and multiplier-based SL tested |
| TP refinement | ❌ | Static TP dropped, trailing SL preferred |
| Entry refinement | ✅ | Same & previous candle-based liquidity grab + confirmation logic added |
| Entry without confirmation | ❌ | Dropped due to poor results |
| **Same-candle double lot size** | ❌ | Dropped — performed worse than single-size entries |
| SL trailing | 🧪 | Partial implementation |
| Opposite entry after SL | ❌ | Dropped — increased losses |
| MAE/MFE tracking | 🧪 | In progress |
| Exclude news trades | ❌ | Not implemented |
| ML-based filtering | ❌ | Planned |
| Swing detection revisit | 🧪 | Refined twice, needs deeper testing |
| Asymmetric lookback/lookforward | ❌ | Interesting area — not yet tested |

---

Thanks for checking it out!
