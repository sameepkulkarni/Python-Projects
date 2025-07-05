import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from swings_detection import detect_swing
import warnings
warnings.filterwarnings('ignore')
class SwingBacktesterWithScalingEntryRefined:
    def __init__(self, data, swing_window=1, sl_multiplier=2):
        self.swing_window = swing_window
        self.sl_multiplier = sl_multiplier
        self.data = data.copy()
        self.bt = None
        self.results = []
        self.process_all()

    def set_swing_window(self, window):
        self.swing_window = window
        self.process_all()


    def process_all(self):
        self.detect_swings()
        self.calculate_structural_breaks()
        self.calculate_liquidity_grabs()
        self.generate_entry_signals()

    def detect_swings(self):
        self.data['swings_high_price'] = np.where(self.data['swings_high'], self.data['h'], np.nan)
        self.data['swings_low_price'] = np.where(self.data['swings_low'], self.data['l'], np.nan)
        self.data['swings_high_price'] = self.data['swings_high_price'].ffill()
        self.data['swings_low_price'] = self.data['swings_low_price'].ffill()
        self.data.dropna(inplace=True)

    def calculate_structural_breaks(self):
        conditions = [
            self.data['swings_high_price'].shift(1) < self.data['c'],
            self.data['swings_low_price'].shift(1) > self.data['c']
        ]
        choices = ['Bullish', 'Bearish']
        self.data['structural_break'] = np.select(conditions, choices, default=None)

    def calculate_liquidity_grabs(self):
        liquidity_grab_conditions = [
            (self.data['l'] < self.data['swings_low_price'].shift(1)) & (self.data['c'] > self.data['swings_low_price'].shift(1)),
            (self.data['h'] > self.data['swings_high_price'].shift(1)) & (self.data['c'] < self.data['swings_high_price'].shift(1))
        ]
        liquidity_grab_choices = ['Bearish_Grab', 'Bullish_Grab']
        self.data['liquidity_grab'] = np.select(liquidity_grab_conditions, liquidity_grab_choices, default=None)
    def generate_entry_signals(self):
        self.data['entry_signal'] = 0  # default to no signal

        # Case 1: Previous candle liquidity grab + directional close
        prev_bullish = (self.data['liquidity_grab'].shift(1) == 'Bullish_Grab') & (self.data['c'] > self.data['o'])
        prev_bearish = (self.data['liquidity_grab'].shift(1) == 'Bearish_Grab') & (self.data['c'] < self.data['o'])

        # Case 2: Current candle liquidity grab + directional close
        curr_bullish = (self.data['liquidity_grab'] == 'Bullish_Grab') & (self.data['c'] > self.data['o'])
        curr_bearish = (self.data['liquidity_grab'] == 'Bearish_Grab') & (self.data['c'] < self.data['o'])

        # Combine both
        self.data.loc[prev_bullish | curr_bullish, 'entry_signal'] = 1
        self.data.loc[prev_bearish | curr_bearish, 'entry_signal'] = -1

    def run_backtest(self):
        results = []
        in_position = False
        position = 0
        bullish_entry_prices = []
        bullish_entry_times = []
        breaish_entry_prices = []
        breaish_entry_times = []
        bullish_SL_price = None
        bearish_SL_price = None
        data = self.data
         # You can adjust this buffer as needed

        for i in range(1,len(data)):
            signal = data['entry_signal'].iloc[i]
            open_price = data['o'].iloc[i]
            high = data['h'].iloc[i]
            low = data['l'].iloc[i]
            time_now = data.index[i]
            if i>=self.swing_window-1:
                swing_low = data['swings_low'].iloc[i-self.swing_window-1]
                recent_swing_low = data['l'].iloc[i-self.swing_window-1] if swing_low else None
                swing_high = data['swings_high'].iloc[i-self.swing_window]
                recent_swing_high = data['h'].iloc[i-self.swing_window] if swing_high else None
            if signal == 1:
                entry_candle_height = abs(open_price - low)
            elif signal == -1:
                entry_candle_height = abs(high - open_price)
            else:
                entry_candle_height = None
            # Entry
            if not in_position:
                if signal == 1:
                    position = 1
                    bullish_entry_prices = [open_price]
                    bullish_entry_times = [time_now]
                    # Set initial SL below the current candle's low
                    bullish_SL_price = open_price - (entry_candle_height * self.sl_multiplier)
                    in_position = True
                elif signal == -1:
                    position = -1
                    bearish_entry_prices = [open_price]
                    bearish_entry_times = [time_now]
                    # Set initial SL above the current candle's high
                    bearish_SL_price = open_price + (entry_candle_height * self.sl_multiplier)
                    in_position = True
            # Scaling in
            elif in_position:
                if position == 1:
                    
                    # If new swing low, scale in
                    if swing_low:
                        bullish_entry_prices.append(open_price)
                        bullish_entry_times.append(time_now)
                        # Update SL to just below the new swing low
                        bullish_SL_price = recent_swing_low 

                    # Check for stop loss hit
                    if low <= bullish_SL_price and signal != -1:
                        bullish_avg_entry_price = sum(bullish_entry_prices) / len(bullish_entry_prices)
                        bullish_exit_price = bullish_SL_price
                        bullish_exit_time = time_now
                        pnl = (bullish_exit_price - bullish_avg_entry_price) * len(bullish_entry_prices)
                        results.append({
                            'Entry Time': bullish_entry_times[0],
                            'Exit Time': bullish_exit_time,
                            'Direction': 'Long',
                            'Entry Price': bullish_avg_entry_price,
                            'Exit Price': bullish_exit_price,
                            'PnL': pnl,
                            'Exit Reason': 'SL Hit',
                            'SL Price': bullish_SL_price,
                            'Units': len(bullish_entry_prices)
                        })
                        in_position = False
                        position = 0
                        bullish_entry_prices = []
                        bullish_entry_times = []
                        bullish_SL_price = None
                    if signal == -1:
                        bullish_avg_entry_price = sum(bullish_entry_prices) / len(bullish_entry_prices)
                        bullish_exit_price = bullish_SL_price
                        bullish_exit_time = time_now
                        pnl = (bullish_exit_price - bullish_avg_entry_price) * len(bullish_entry_prices)
                        results.append({
                            'Entry Time': bullish_entry_times[0],
                            'Exit Time': bullish_exit_time,
                            'Direction': 'Long',
                            'Entry Price': bullish_avg_entry_price,
                            'Exit Price': bullish_exit_price,
                            'PnL': pnl,
                            'Exit Reason': 'Bearish Trade Reversal',
                            'SL Price': bullish_SL_price,
                            'Units': len(bullish_entry_prices)
                        })
                        
                        position = -1
                        bearish_entry_prices = [open_price]
                        bearish_entry_times = [time_now]
                        # Set initial SL above the current candle's high
                        bearish_SL_price = open_price + (entry_candle_height * self.sl_multiplier)
                        in_position = True
                        

            # Scaling in
                elif position == -1:
                # If new swing high, scale in
                    if swing_high:
                        bearish_entry_prices.append(open_price)
                        bearish_entry_times.append(time_now)
                        # Update SL to just above the new swing high
                        bearish_SL_price = recent_swing_high 

                    # Check for stop loss hit
                    if high >= bearish_SL_price and signal != 1:
                        bearish_avg_entry_price = sum(bearish_entry_prices) / len(bearish_entry_prices)
                        bearish_exit_price = bearish_SL_price
                        bearish_exit_time = time_now
                        pnl = (bearish_avg_entry_price - bearish_exit_price) * len(bearish_entry_prices)
                        results.append({
                            'Entry Time': bearish_entry_times[0],
                            'Exit Time': bearish_exit_time,
                            'Direction': 'Short',
                            'Entry Price': bearish_avg_entry_price,
                            'Exit Price': bearish_exit_price,
                            'PnL': pnl,
                            'Exit Reason': 'SL Hit',
                            'SL Price': bearish_SL_price,
                            'Units': len(bearish_entry_prices)
                        })
                        in_position = False
                        position = 0
                        bearish_entry_prices = []
                        bearish_entry_times = []
                        bearish_SL_price = None
                    if signal ==1:
                        bearish_avg_entry_price = sum(bearish_entry_prices) / len(bearish_entry_prices)
                        bearish_exit_price = bearish_SL_price
                        bearish_exit_time = time_now
                        pnl = (bearish_avg_entry_price - bearish_exit_price) * len(bearish_entry_prices)
                        results.append({
                            'Entry Time': bearish_entry_times[0],
                            'Exit Time': bearish_exit_time,
                            'Direction': 'Short',
                            'Entry Price': bearish_avg_entry_price,
                            'Exit Price': bearish_exit_price,
                            'PnL': pnl,
                            'Exit Reason': 'Bullish Trade Reversal',
                            'SL Price': bearish_SL_price,
                            'Units': len(bearish_entry_prices)
                        })
                        position = 1
                        bullish_entry_prices = [open_price]
                        bullish_entry_times = [time_now]
                        # Set initial SL below the current candle's low
                        bullish_SL_price = open_price - (entry_candle_height * self.sl_multiplier)
                        in_position = True
                        
            # (You can add similar logic for short trades and scaling in on new swing highs.)

        self.results = results
        self.bt = pd.DataFrame(results)
        print(f"✅ Total trades generated: {len(self.bt)}")

        if not self.bt.empty:
            self.bt['Cumulative PnL'] = self.bt['PnL'].cumsum()
            self.bt['Entry Time'] = pd.to_datetime(self.bt['Entry Time'])
            self.bt['Exit Time'] = pd.to_datetime(self.bt['Exit Time'])
            self.bt['Duration'] = (self.bt['Exit Time'] - self.bt['Entry Time']).dt.total_seconds() / 60

    def calculate_mae_mfe(self):
        if self.bt is None or self.bt.empty:
            print("Run backtest first.")
            return
        mae_list = []
        mfe_list = []
        for idx, row in self.bt.iterrows():
            entry_time = row['Entry Time']
            exit_time = row['Exit Time']
            entry_price = row['Entry Price']
            direction = 1 if row['Direction'] == 'Long' else -1
            trade_data = self.data.loc[entry_time:exit_time]
            if direction == 1:
                min_low = trade_data['l'].min()
                max_high = trade_data['h'].max()
                mae = min_low - entry_price
                mfe = max_high - entry_price
            else:
                max_high = trade_data['h'].max()
                min_low = trade_data['l'].min()
                mae = entry_price - max_high
                mfe = entry_price - min_low
            mae_list.append(mae * direction)
            mfe_list.append(mfe * direction)
        self.bt['MAE'] = mae_list
        self.bt['MFE'] = mfe_list

    def summary_stats(self):
        if self.bt is None or self.bt.empty:
            print("Run backtest first.")
            return
        bt = self.bt
        print("\n📊 Summary Statistics:")
        print(f"Total Trades:       {len(bt)}")
        print(f"Winning Trades:     {(bt['PnL'] > 0).sum()}")
        print(f"Losing Trades:      {(bt['PnL'] < 0).sum()}")
        print(f"Max Winning Trade: {bt.loc[bt['PnL'] > 0, 'PnL'].max():.2f}")
        print(f"Max Losing Trade: {bt.loc[bt['PnL'] < 0, 'PnL'].min():.2f}")
        print(f"Win Rate:           {((bt['PnL'] > 0).mean() * 100):.2f}%")
        print(f"Total PnL:          {bt['PnL'].sum():.2f}")
        print(f"Average PnL:        {bt['PnL'].mean():.2f}")
        print(f"Max Drawdown:       {(bt['Cumulative PnL'].cummax() - bt['Cumulative PnL']).max():.2f}")
        avg_win = bt.loc[bt['PnL'] > 0, 'PnL'].mean()
        avg_loss = bt.loc[bt['PnL'] < 0, 'PnL'].mean()
        print(f"Winning PnL:     {bt.loc[bt['PnL'] > 0, 'PnL'].sum():.2f}")
        print(f"Losing PnL:      {bt.loc[bt['PnL'] < 0, 'PnL'].sum():.2f}")
        rr = abs(avg_win) / abs(avg_loss) if avg_loss != 0 else float('inf')
        print(f"Winning Trades average PnL: {avg_win:.2f}")
        print(f"Losing Trades average PnL: {avg_loss:.2f}")
        print(f"Risk-Reward Ratio: {rr:.2f}")
        if 'MAE' in bt.columns and 'MFE' in bt.columns:
            print("\n📉 Maximum Adverse Excursion (MAE) Stats:")
            print(f"Average MAE:           {bt['MAE'].mean():.2f}")
            print(f"Max MAE (worst pain):  {bt['MAE'].min():.2f}")
            print("\n📈 Maximum Favorable Excursion (MFE) Stats:")
            print(f"Average MFE:           {bt['MFE'].mean():.2f}")
            print(f"Max MFE (best opportunity): {bt['MFE'].max():.2f}")
            bt['Efficiency (%)'] = (bt['PnL'] / bt['MFE']) * 100
            efficiency_mean = bt['Efficiency (%)'].mean()
            print(f"\n⚙️  Average Trade Efficiency: {efficiency_mean:.2f}%")

    def plot_cumulative_pnl(self):
        if self.bt is None or self.bt.empty:
            print("Run backtest first.")
            return
        bt_plot = self.bt.set_index('Exit Time')
        bt_plot['Cumulative PnL'].plot(title='Continuous Position Backtest', figsize=(12, 4))
        plt.xlabel("Time")
        plt.ylabel("Cumulative PnL")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.show() 