import pandas as pd
from swings_detection import detect_swing  # ensure this function is saved in swings_detection.py

# Load your dataset
df_base = pd.read_csv("gold_data_5_minutes_completed.csv", parse_dates=['timestamp'])
df_base.set_index('timestamp', inplace=True)

# Window sizes to apply
window_sizes = [1, 2,3,4,5,6,7,8,9,10]

# Create ExcelWriter
output_file = "swing_detection_outputs.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    for window in window_sizes:
        df = df_base.copy()
        detect_swing(df, type='high', window=window)
        detect_swing(df, type='low', window=window)

        # Optionally keep only relevant columns
        output_df = df[['o', 'h', 'l', 'c', f'swings_high', f'swings_low']]

        # Write to Excel sheet
        sheet_name = f"Window_{window}"
        print(output_df['swings_high'].value_counts())
        print(output_df['swings_low'].value_counts())

        output_df.to_excel(writer, sheet_name=sheet_name)
        print(f'Sheet created for  window size = {window}')
print(f"✅ Excel file '{output_file}' created with sheets for window sizes {window_sizes}")
