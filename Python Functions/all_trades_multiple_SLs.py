import os
import pandas as pd
import glob
import re
import time
import concurrent.futures
# from backtester_csv_2_entry import SwingBacktesterWithScalingEntryRefined
from backtester_csv import SwingBacktesterWithScaling

# Set SL once
sl_multiplier =[3]

def run_backtest_for_window(csv_file, sl_mult, output_dir):
    try:
        match = re.search(r'Window_(\d+)', os.path.basename(csv_file))
        window = int(match.group(1)) if match else -1
        df = pd.read_csv(csv_file, index_col='timestamp', parse_dates=True)
        # bt = SwingBacktesterWithScalingEntryRefined(data=df, swing_window=window, sl_multiplier=sl_mult)
        bt = SwingBacktesterWithScaling(data=df, swing_window=window, sl_multiplier=sl_mult)
        bt.run_backtest()
        bt.calculate_mae_mfe()
        bt_df = bt.bt
        if not bt_df.empty:
            output_file = os.path.join(output_dir, f'All_Trades_Window_{window}_SL_{sl_mult}.csv')
            bt_df.to_csv(output_file, index=False)
        print(f"✅ Done: Window {window}")
    except Exception as e:
        print(f"❌ Error processing {csv_file}: {e}")

def main():
    start_time = time.time()

    # Paths
    csv_folder = r'C:\Users\A\epat\Algo Project\Python-Projects\swing_csvs'
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'all_trades'))
    os.makedirs(output_dir, exist_ok=True)
    for sl_mult in sl_multiplier:  
    # Get all window files
        csv_files = sorted(glob.glob(os.path.join(csv_folder, "swings_window_*.csv")))
    
        print(f"🔄 Running SL={sl_multiplier} on {len(csv_files)} windows...")

        # Parallelize over files (windows)
        with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
            futures = [
                executor.submit(run_backtest_for_window, csv_file, sl_mult, output_dir)
                for csv_file in csv_files
            ]
            concurrent.futures.wait(futures)

        elapsed = (time.time() - start_time) / 60
        print(f"\n✅ All backtests completed in {elapsed:.2f} minutes.")

if __name__ == '__main__':
    main()
