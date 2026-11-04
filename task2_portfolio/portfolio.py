import csv
import yfinance as yf


def load_tickers(filename):
    # reads the csv and returns {symbol: company name}
    tickers = {}
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickers[row["Symbol"]] = row["Security"]
    return tickers


def get_holdings(tickers):
    # asks the user for stocks until they type done
    holdings = {}
    while True:
        symbol = input("Ticker (or 'done'): ").strip().upper()
        if symbol == "DONE":
            break
        if symbol not in tickers:
            print("Not in the S&P 500 list, try again")
            continue
        try:
            buy_price = float(input("Buy price: "))
            shares = int(input("Shares: "))
        except ValueError:
            print("Enter numbers only")
            continue
        if buy_price <= 0 or shares <= 0:
            print("Values must be more than 0")
            continue
        holdings[symbol] = {"buy_price": buy_price, "shares": shares}
    return holdings


tickers = load_tickers("sp500_tickers.csv")
holdings = get_holdings(tickers)
def get_current_price(symbol):
    # yfinance uses '-' instead of '.' (BRK.B -> BRK-B)
    symbol = symbol.replace(".", "-")
    try:
        data = yf.Ticker(symbol).history(period="5d")
        return float(data["Close"].iloc[-1])
    except Exception:
        return None


for symbol in holdings:
    price = get_current_price(symbol)
    if price is None:
        print(symbol, ": could not fetch price")
    else:
        print(symbol, ": current price", round(price, 2))