Hi
Welcome to my project based on recent swing high and lows on 5 minute timeframe of gold.
It generates signal based on failed swing price and rapid pullback.

I have used swing_detection.py in order to find swing prices within a specified window of candles before and after the selected candle. As I have included the lookforward and lookback window too, it does not give me look ahead bias.

I used the function to create 10 csv files from the raw data which gave me the minor swing high and lows in the given time period.

I used liquidity grab and run concept to define an entry point in my strategy.
 if this candle's low < last swing low price and this candle is green, we go long and vice versa for short 
 (This is yet to be tested without the green candle confirmation)

 When a swing low is made, we scale in with the new stop loss as the recent swing low (This is generating low MFE values, it needs to be refined as well.)

 Currently there is no take profit level as of now. I am working on that.

I have made a class named SwingBacktesterWithScaling in backtester_csv.py to backtest my strategy and return summary of it in scaling_included.ipynb jupyter notebook.

I have included visualization.ipynb which shows performance of my strategy across different windows and stoploss multipliers 

The news timings need to be excluded from the strategy.

I am still refining the main function of my strategy, i.e., swing_detection.py and will try to incoporate major swing high and lows too before jumping to ML side for this strategy.

One of the core problems is that I could not find a big dataset for free, this is only 2 year gold data in 5 minutes timeframe.
