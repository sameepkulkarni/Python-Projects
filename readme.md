# Gold Swing High-Low Based Strategy (5-Minute Timeframe)

Hi,  
Welcome to my project based on recent swing highs and lows from 5-minute Gold price data. The strategy aims to generate trading signals based on failed swing points followed by rapid pullbacks.

---

## 📌 Core Logic

The trading logic revolves around:
- Detecting minor swing highs/lows using a lookback and lookforward window, **eliminating look-ahead bias**.
- Generating entry signals using the **liquidity grab and run** concept:
  - **Long Entry:** Current candle’s low < last swing low **and** the candle is bullish (green).
  - **Short Entry:** Current candle’s high > last swing high **and** the candle is bearish (red).
  > ✅ *Tested removing the green/red confirmation — performance dropped significantly, so the logic was dropped.*

- **Scaling In**:
  - When a new swing low forms while in a long position, re-entry occurs with an updated stop loss at the recent swing.
  - However, this scaling logic sometimes leads to **low MFE values**, which needs further refinement.

- **Stop Loss Logic**:
  - A stop loss is set using a **candle height multiplier**, to accommodate volatile scenarios.
  - Volatility-based ML testing is planned for dynamic tuning.

- **Take Profit**:  
  - Not yet implemented. This is under active development.

---

## 🧠 Key Files & Modules

### 🔧 `swing_detection.py`
Detects minor swing highs and lows using a user-defined window of candles. It avoids look-ahead bias by checking both forward and backward candles. The script was used to generate 10 CSV files covering the relevant period.

### 🧪 Backtesting Notebooks
- `5min_initial_backtest.ipynb` — Backtests a continuous in-trade scenario.
- `5min_2nd_refinement.ipynb` — Uses nominal candle lows as stop loss.
- `scaling_included.ipynb` — Implements position scaling based on new swing points.

### 📊 `visualization.ipynb`
Displays performance heatmaps across varying swing windows and stop loss multipliers.

### 📁 `backtester_csv.py`
Contains `SwingBacktesterWithScaling` class, the core backtesting engine used in the notebooks.

---

## 📄 Other Notes

- `refinement approaches.txt` — Contains a list of potential improvements and testing ideas for the strategy.
- Currently working on integrating **major swing highs/lows** into the detection algorithm.
- **News times are not yet filtered out** — this is a planned refinement.
- A key challenge is **data availability**. The current dataset spans 2 years of 5-minute Gold data only.

---

## 🚧 Work in Progress

This project is in active development. Summary of refinement steps:

- ✅ SL refinement (basic) done.
- ✅ SL based on `x * (Open - Low.shift(1))` added to allow price room — helped improve PnL.
- ❌ TP refinement (static) was tried — dropped due to poor RR. Will use SL trailing instead.
- 🧪 SL trailing partially implemented — under refinement.
- ❌ Entry without confirmation candle tested — **dropped** due to poor performance.
- ❌ Entry refinement using volatility, structure breaks, and recency — not done.
- ❌ TP based on structure break or swing logic — not done.
- ❌ Opposite entry on SL trigger tested — dropped due to increased losses.
- 🧪 MAE/MFE analysis is ongoing.
- ❌ News session filtering — not done.
- ❌ ML-based entry/exit refinement and trade reduction — not yet implemented.
- ✅ `detect_swing()` refined twice — **needs to be revisited** again as it's core to signal generation.
- ❌ Lookback vs Lookforward asymmetry in swing detection — interesting test case, yet to be done.

---

Thanks for checking it out!
