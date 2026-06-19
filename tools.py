import requests
import yfinance as yf
from langchain_core.tools import tool

@tool
def get_stock_price(ticker: str) -> str:
    """
    Retrieve the current or most recent stock price for a given stock ticker symbol.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL').
        
    Returns:
        str: A string indicating the current stock price and currency, or an error message.
    """
    ticker_clean = ticker.strip().upper()
    try:
        ticker_obj = yf.Ticker(ticker_clean)
        # Attempt to get price from fast_info
        info = ticker_obj.fast_info
        current_price = info.get('last_price')
        currency = info.get('currency', 'USD')
        
        # If fast_info doesn't return the price, fallback to historical data
        if current_price is None or current_price == 0:
            hist = ticker_obj.history(period="1d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
            else:
                # Try fallback via info dictionary if available
                # Note: info can be slow or fail, so we use it as last resort
                info_dict = ticker_obj.info
                current_price = info_dict.get('currentPrice') or info_dict.get('regularMarketPrice')
                currency = info_dict.get('currency', 'USD')
        
        if current_price is not None:
            return f"The current stock price for {ticker_clean} is {current_price:.2f} {currency}."
        else:
            return f"Error: Could not retrieve price data for ticker symbol '{ticker_clean}'."
            
    except Exception as e:
        return f"Error occurred while fetching stock price for '{ticker_clean}': {str(e)}"

@tool
def search_stock_ticker(query: str) -> str:
    """
    Search for a company's stock ticker symbol by its name or search query. Use this tool when you don't know the exact ticker symbol for a company.
    
    Args:
        query (str): The name of the company or search query (e.g., 'Apple', 'Microsoft', 'Saudi Aramco').
        
    Returns:
        str: A string with the found ticker symbol and company name, or a message indicating no ticker was found.
    """
    query_clean = query.strip()
    try:
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        params = {'q': query_clean, 'quotesCount': 3, 'newsCount': 0}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        quotes = data.get('quotes', [])
        
        if quotes:
            results = []
            for quote in quotes:
                symbol = quote.get('symbol')
                shortname = quote.get('shortname')
                longname = quote.get('longname')
                exchange = quote.get('exchange')
                name = shortname or longname or query_clean
                if symbol:
                    results.append(f"Ticker: '{symbol}' for '{name}' (Exchange: {exchange})")
            
            return "\n".join(results)
        
        return f"Could not find any stock tickers matching '{query_clean}'."
    except Exception as e:
        return f"Error searching for ticker matching '{query_clean}': {str(e)}"
