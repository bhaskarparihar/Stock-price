import sys
from tools import get_stock_price, search_stock_ticker

def test_ticker_search():
    print("=== Testing Ticker Search ===")
    companies = ["Apple", "Microsoft", "Google", "Tesla"]
    for company in companies:
        print(f"Searching ticker for: {company}")
        try:
            # Using the tool's underlying function or invoke it
            # In LangChain, we can invoke a tool using .invoke() or just call the function directly.
            # Since @tool wraps the function, we can use search_stock_ticker.invoke() or call the function itself.
            result = search_stock_ticker.invoke(company)
            print(f"Result:\n{result}\n")
        except Exception as e:
            print(f"Error: {e}\n")

def test_price_fetching():
    print("=== Testing Price Fetching ===")
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
    for ticker in tickers:
        print(f"Fetching price for ticker: {ticker}")
        try:
            result = get_stock_price.invoke(ticker)
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    print("Starting Tools Verification (No API Keys needed)...")
    test_ticker_search()
    test_price_fetching()
    print("Verification complete.")
