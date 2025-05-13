import yfinance as yf


# Step 3: Get stock prices
def get_stock_prices(symbols, k):
    stock_data = ""

    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1h")
        latest_prices = hist['Close'].tail(k)
        prices_list = latest_prices.tolist()
        stock_data += f"Recent {k} prices for {symbol}: {prices_list}\n\n"

    return stock_data