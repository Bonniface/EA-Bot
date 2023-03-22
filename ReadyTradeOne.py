import MetaTrader5 as mt5
import time
import pandas as pd
import ta.trend
import ta.momentum

# Set up the MACD parameters
macd_fast = 12
macd_slow = 26
macd_signal = 9

# Set up the RSI parameters
rsi_period = 14
rsi_buy_threshold = 30
rsi_sell_threshold = 70

# Set up the MA 50 parameters
ma_period = 50

# Set up the trade parameters
stop_loss_pips = 10
trailing_stop_pips = 10
take_profit_pips = 20


# Define function to retrieve tickers from market watch
def get_tickers():
    market_watch = mt5.market_watch()
    if market_watch is None:
        print("Failed to get market watch")
        return []
    else:
        tickers = [x for x in market_watch if x.name.endswith("USD")]
        print(f"Tickers: {tickers}")
        return tickers

# Retrieve tickers from market watch
tickers = get_tickers()

# Loop through tickers and check for trading signals
for ticker in tickers:
    # Retrieve latest tick data
    rates = mt5.copy_rates_from_pos(ticker.name, mt5.TIMEFRAME_M1, 0, 1)
    if rates is None:
        print(f"Failed to get tick data for {ticker.name}")
        continue


# Connect to the MetaTrader 5 terminal
mt5.initialize()

# Set up the trading account
account = 67643048
password = 'password'
server = 'MetaQuotes-Demo'
login = mt5.login(account, password=password, server=server)

# Main loop for the scalping EA
while True:
    # Loop through the tickers
    for ticker in tickers:
        # Get the latest tick data
        rates = pd.DataFrame(mt5.copy_rates_from_pos(ticker.name, mt5.TIMEFRAME_M1, 0, 1))
        rates = rates.rename(columns={'time': 'date'})
        rates['date'] = pd.to_datetime(rates['date'], unit='s')
        rates = rates.set_index('date')

        # Check if we have enough data
        if len(rates) < max(macd_slow, ma_period):
            continue

        # Calculate the MACD, MA 50 and RSI indicators
        macd = ta.trend.MACD(rates['close'], window_fast=macd_fast, window_slow=macd_slow, window_sign=macd_signal).macd()
        ma = ta.trend.SMAIndicator(rates['close'], window=ma_period).sma_indicator()
        rsi = ta.momentum.RSIIndicator(rates['close'], window=rsi_period).rsi()

    # Check if we have a buy signal
    if macd[-1] > 0 and rsi[-1] < rsi_buy_threshold and rates['close'][-1] > ma[-1]:
        # Place a buy order
        lot_size = round(0.01 * (1 + 0.5 * (2 * random() - 1)), 2) # random lot size between 0.01 and 0.015
        buy_price = mt5.symbol_info_tick(ticker.name).ask
        stop_loss = buy_price - (stop_loss_pips * mt5.symbol_info(ticker.name).point)
        trailing_stop = trailing_stop_pips * mt5.symbol_info(ticker.name).point
        take_profit = 0
        request = {
            'action': mt5.TRADE_ACTION_PENDING,
            'symbol': ticker.name,
            'volume': lot_size,
            'type': mt5.ORDER_TYPE_BUY_STOP,
            'price': buy_price + trailing_stop,
            'sl': stop_loss,
            'tp': take_profit,
            'magic': 123456,
            'comment': 'Scalping EA buy',
            'deviation': 10,
            'type_time': mt5.ORDER_TIME_GTC,
        }
        result = mt5.order_send(request)
        print(f'Buy {ticker.name} at {buy_price}. Result: {result}')

