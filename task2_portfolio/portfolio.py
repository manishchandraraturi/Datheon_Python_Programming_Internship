import csv
import os
from datetime import datetime

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


def get_current_price(symbol):
    # yfinance uses '-' instead of '.' (BRK.B -> BRK-B)
    symbol = symbol.replace(".", "-")
    try:
        data = yf.Ticker(symbol).history(period="5d")
        return float(data["Close"].iloc[-1])
    except Exception:
        return None


def calculate(holdings, tickers):
    # works out invested, current value and gain/loss for each stock
    rows = []
    for symbol, info in holdings.items():
        price = get_current_price(symbol)
        if price is None:
            print(symbol, ": could not fetch price, skipping")
            continue
        invested = info["buy_price"] * info["shares"]
        value = price * info["shares"]
        gain = value - invested
        percent = gain / invested * 100
        rows.append({
            "symbol": symbol,
            "company": tickers[symbol],
            "shares": info["shares"],
            "buy_price": info["buy_price"],
            "price": price,
            "invested": invested,
            "value": value,
            "gain": gain,
            "percent": percent,
        })
    return rows


def print_report(rows):
    print()
    print(f"{'Ticker':<8}{'Shares':>7}{'Buy':>10}{'Now':>10}{'Invested':>12}{'Value':>12}{'P/L':>12}{'P/L %':>9}")
    print("-" * 80)
    for r in rows:
        print(f"{r['symbol']:<8}{r['shares']:>7}{r['buy_price']:>10.2f}{r['price']:>10.2f}"
              f"{r['invested']:>12.2f}{r['value']:>12.2f}{r['gain']:>12.2f}{r['percent']:>8.2f}%")
    print("-" * 80)

    total_invested = sum(r["invested"] for r in rows)
    total_value = sum(r["value"] for r in rows)
    total_gain = total_value - total_invested
    total_percent = total_gain / total_invested * 100
    print(f"Total invested : {total_invested:.2f}")
    print(f"Current value  : {total_value:.2f}")
    print(f"Total P/L      : {total_gain:.2f} ({total_percent:.2f}%)")
    return total_invested, total_value, total_gain, total_percent


def save_summary(rows, totals, filename="portfolio_summary.csv"):
    # adds this run to the csv, writes the header only the first time
    new_file = not os.path.exists(filename)
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["Date", "Ticker", "Company", "Shares", "Buy Price",
                             "Current Price", "Invested", "Current Value",
                             "Gain/Loss", "Gain/Loss %"])
        for r in rows:
            writer.writerow([date, r["symbol"], r["company"], r["shares"],
                             round(r["buy_price"], 2), round(r["price"], 2),
                             round(r["invested"], 2), round(r["value"], 2),
                             round(r["gain"], 2), round(r["percent"], 2)])
        writer.writerow([date, "TOTAL", "", "", "", "",
                         round(totals[0], 2), round(totals[1], 2),
                         round(totals[2], 2), round(totals[3], 2)])
    print("\nSaved to", filename)


def main():
    tickers = load_tickers("sp500_tickers.csv")
    holdings = get_holdings(tickers)
    if not holdings:
        print("No stocks entered")
        return
    rows = calculate(holdings, tickers)
    if not rows:
        print("No prices could be fetched, try again later")
        return
    totals = print_report(rows)
    save_summary(rows, totals)


main()