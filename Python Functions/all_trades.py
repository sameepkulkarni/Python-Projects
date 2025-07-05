import os
import pandas as pd
import glob
import re
import time
import concurrent.futures
from backtester_csv_2_entry import SwingBacktesterWithScalingEntryRefined
# from backtester_csv import SwingBacktesterWithScaling
# SL multipliers to test
sl_multipliers = [1, 1.5, 2, 2.5, 2.75,3, 3.25, 3.5, 3.75, 4]

def run_backtest_for_sl(sl_mult, df_path, window, output_dir):
    try:
        df = pd.read_csv(df_path, index_col='timestamp', parse_dates=True)
        bt = SwingBacktesterWithScalingEntryRefined(data=df, swing_window=window, sl_multiplier=sl_mult)
        # bt = SwingBacktesterWithScaling(data=df, swing_window=window, sl_multiplier=sl_mult)
        bt.run_backtest()
        bt.calculate_mae_mfe()
        bt_df = bt.bt
        if not bt_df.empty:
            output_file = os.path.join(output_dir, f'All_Trades_Window_{window}_SL_{sl_mult}.csv')
            bt_df.to_csv(output_file, index=False)
    except Exception as e:
        print(f"Error processing window {window}, SL {sl_mult}: {e}")

def main():
    # Start timer
    start_time = time.time()

    # Folder paths
    csv_folder = r'C:\Users\A\epat\Algo Project\Python-Projects\swing_csvs'
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'all_trades_entry_on_either_two_candles'))
    os.makedirs(output_dir, exist_ok=True)

    # CSVs sorted
    csv_files = sorted(glob.glob(os.path.join(csv_folder, "swings_window_*.csv")))

    for csv_file in csv_files:
        match = re.search(r'Window_(\d+)', os.path.basename(csv_file))
        window = int(match.group(1)) if match else -1
        print(f"\n📁 Processing window = {window}")

        # Run each SL in parallel
        with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()-1) as executor:
            futures = [
                executor.submit(run_backtest_for_sl, sl_mult, csv_file, window, output_dir)
                for sl_mult in sl_multipliers
            ]
            concurrent.futures.wait(futures)

    elapsed = (time.time() - start_time) / 60
    print(f"\n✅ All backtests completed in {elapsed:.2f} minutes.")

# ✅ Windows multiprocessing safe block
if __name__ == '__main__':
    main()
