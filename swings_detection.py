import pandas as pd

def detect_swing(df, type, window=5):
    """
    Detect swing highs in price data
    window: number of bars to look before and after (default=5)
    """
    swings = []
    
    # Loop through the data
    for i in range(window, len(df) - window):
        # Get the current swing
        current_swing = df['h'].iloc[i]
        
        # Get the window of bars before and after
        before_window = df['h'].iloc[i-window:i]
        after_window = df['h'].iloc[i+1:i+window+1]
        
        if type == 'high':
            # Check if current swing is greater than all bars before and after
            if all(current_swing > before_window) and all(current_swing > after_window):
                swings.append(True)
            else:
                swings.append(False)
        
        elif type == 'low':
            if all(current_swing < before_window) and all(current_swing < after_window):
                swings.append(True)
            else:
                swings.append(False)
    
    # Pad the results with False for the bars at the start and end
    swings = [False] * window + swings + [False] * window
    
    df['swings_{}'.format(type)] = swings
    print('swings_{}'.format(type) +'with window {}'.format(window) + ' added to dataframe')
    print(df.head())