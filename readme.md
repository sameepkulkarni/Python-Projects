# Gold Swing High-Low Based Strategy (5-Minute Timeframe)

Hi,  
Welcome to my project based on recent swing highs and lows from 5-minute Gold price data. The strategy aims to generate trading signals based on failed swing points followed by rapid pullbacks.

---

## 📌 Core Logic

The trading logic revolves around:
- Detecting minor swing highs/lows using a lookback and lookforward window, **eliminating look-ahead bias**.
- Generating entry signals using the **liquidity grab and run** concept:
  - **Long Entry:** Current candle’s low < last swing low AND the candle is bullish (green).
  - **Short Entry:** Current candle’s high > last swing high AND the candle is bearish (red).
  > *(Testing without the green/red candle confirmation is pending.)*

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

This project is in active development and evolving. Upcoming goals:
- Add major swing logic
- Improve scaling mechanism
- Integrate take-profit logic
- Conduct volatility-aware ML tuning
- Exclude high-impact news periods

---

Thanks for checking it out!
