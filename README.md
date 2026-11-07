# Datheon Python Programming Internship

Python projects I built for the Datheon Python Programming Internship (Oct-Nov 2026).

## Task 2: Stock Portfolio Tracker (`task2_portfolio/`)
Takes stock tickers, buy prices and share counts from the user, checks each ticker against an S&P 500 list, fetches live prices using yfinance, and prints profit/loss for each stock and for the whole portfolio. Each run is saved to `portfolio_summary.csv`.

Run: `pip install yfinance`, then `python portfolio.py`

## Task 3: File Organizer (`task3_organizer/`)
Sorts the files in a folder into Documents, Images, Videos, Audio, Archives, Code and Others. It has a dry-run mode to preview changes, renames files when the name already exists (like `notes (1).txt`), handles permission errors, and writes a log to `organizer.log`.

Run: `python organizer.py`

## Task 4: Rule-Based Chatbot (`task4_chatbot/`)
A customer support chatbot for a shop. It loads intents from `faq.json`, matches keywords with regex, can answer more than one question in a single message, and gives a fallback reply when it doesn't understand. Type `bye`, `exit` or `quit` to leave.

Run: `python chatbot.py`

## Requirements
Python 3. Task 2 also needs `yfinance`.