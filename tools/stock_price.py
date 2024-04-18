from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
from .yf_tools import get_stock_price

class StockPriceCheckInput(BaseModel):
    """Input for Stock price check."""

    stock_ticker: str = Field(...,
                             description="Ticker symbol for stock or index")
    period: str = Field('1d', description="Period for stock price check, default is 1d, can be 1d, 1mo")

class StockPriceTool(BaseTool):
    name = "get_stock_ticker_price"
    description = (
        "Useful for when you need to find out the price of stock. "
        "You should input the stock ticker used on the yfinance API"
    )

    def _run(self, stock_ticker: str, period: str = '1d'):
        data = get_stock_price(stock_ticker, period)
        return data
        
    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput

