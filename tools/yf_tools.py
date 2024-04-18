import yfinance as yf

def get_stock_price(symbol: str, period: str = '1d'):
    """
    Fetches the closing price of a stock for a specified period using its ticker symbol.
    
    Args:
    - symbol (str): The ticker symbol of the stock.
    - period (str): The time period to fetch data for (e.g., '1d', '1mo', '1y').

    Returns:
    - dict: A dictionary containing the following keys:
        - country: The country where the stock is listed.
        - sector: The sector the stock belongs to.
        - price: The closing price of the stock per share.
        - currency: The currency the stock is traded in.
    """
    if symbol.isdigit():
        symbol += '.TW'

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        data = ticker.history(period=period)
    except Exception as e:
        return {
            'error': str(e)
        }

    return {
        'country': info['country'],
        'sector': info['sector'],
        'price': round(data['Close'][0], 3),
        'currency': info['currency'],
        'date': data.index[0].strftime('%Y-%m-%d')
    }