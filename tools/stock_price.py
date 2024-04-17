from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
from .yf_tools import get_stock_price

class StockPriceCheckInput(BaseModel):
    """Input for Stock price check."""

    stock_ticker: str = Field(...,
                             description="Ticker symbol for stock or index")

class StockPriceTool(BaseTool):
    name = "get_stock_ticker_price"
    description = (
        "Useful for when you need to find out the price of stock. "
        "You should input the stock ticker used on the yfinance API"
    )

    def _run(self, stock_ticker: str):
        price = get_stock_price(stock_ticker)
        return f"The price of {stock_ticker} is {price}"
        
    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput

