# EA-Bot
EA that can open and manage trades based on the MACD and MA50 indicators, as well as a more advanced scalping strategy that includes a trailing stop loss. 

- We started by importing the necessary libraries, including MetaTrader 5, Talib, Tensorflow, Numpy, and Matplotlib.
- We connected to the MetaTrader 5 terminal using the mt5.initialize() method.
- We defined the necessary variables for the MACD and MA50 indicators, such as the symbol, timeframe, and indicator periods.
- We used Talib to calculate the MACD and MA50 values for the specified symbol and timeframe.
- We defined a function to check for a MACD and MA50 crossover.
- We used the crossover() function to check for a crossover and open a long trade if a crossover is detected.
- We added a stop loss and take profit to the trade order, as well as a unique magic number and comment to help identify the trade.
- We disconnected from the MetaTrader 5 terminal using the mt5.shutdown() method.
- We encountered an error when running the code, which was due to the missing Talib module. We resolved this issue by installing Talib and importing it correctly.
- We added a trailing stop loss to the trade order to help limit potential losses and improve risk management.
- We created a scalping method using the MACD and MA50 indicators, which involves opening and closing trades quickly to take advantage of small price movements.
- We added the scalping method to the existing EA to create a more comprehensive trading system.
Overall, we have created a basic EA that can open and manage trades based on the MACD and MA50 indicators, as well as a more advanced scalping strategy that includes a trailing stop loss.
