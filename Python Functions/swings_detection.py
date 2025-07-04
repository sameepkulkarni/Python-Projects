import pandas as pd

def detect_swing(df, type='high', window=5):
    """
    Detect swing highs or lows in price data.
    
    Parameters:
    - df: DataFrame with columns 'h' for high, 'l' for low
    - type: 'high' or 'low'
    - window: number of bars before and after to check for a swing
    
    Adds a new column: 'swings_high' or 'swings_low' (boolean)
    """
    if type == 'high':
        price_col = 'h'
    elif type == 'low':
        price_col = 'l'
    else:
        raise ValueError("type must be 'high' or 'low'")

    swings = []
    
    for i in range(window, len(df) - window):
        current = df[price_col].iloc[i]
        before = df[price_col].iloc[i - window:i].values
        after = df[price_col].iloc[i + 1:i + window + 1].values
        
        if type == 'high':
            swings.append(current > before.max() and current > after.max())
        else:
            swings.append(current < before.min() and current < after.min())

    # Padding
    swings = [False] * window + swings + [False] * window
    df[f'swings_{type}'] = swings
    
    print("swings_" + type + " with window=" + str(window) + " added to DataFrame")
    return df
