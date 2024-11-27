import logging
import datetime as dt
import pandas as pd
from ib_async import IB, Contract
from exchange_calendars import get_calendar

logger = logging.getLogger(__name__)


class ContractService:
  def __init__(self, ibkr: IB, contract: Contract):
    self.ibkr = ibkr
    self.contract = contract

  def get_current_price(self, price_type: str = "last") -> float:
    """
    Get the current price of the contract
    """
    logger.debug("Getting price for contract: %s", self.contract)
    logger.debug("Contract conId: %s", self.contract.conId)

    # Check if market is open
    nyse = get_calendar("XNYS")
    current_time = dt.datetime.now(dt.UTC)
    is_market_open = nyse.is_open_on_minute(current_time)
    logger.debug("Market is open: %s", is_market_open)

    # Set market data type based on market status
    self.ibkr.reqMarketDataType(1 if is_market_open else 2)

    # Qualify the contract
    self.ibkr.qualifyContracts(self.contract)

    # Request market data
    ticker = self.ibkr.reqMktData(self.contract)

    # Wait for market data to arrive (timeout after 10 seconds)
    timeout = 10
    start_time = dt.datetime.now()
    while (not ticker.last or pd.isna(ticker.last)) and (
      dt.datetime.now() - start_time
    ).seconds < timeout:
      self.ibkr.sleep(0.1)

    price = getattr(ticker, price_type)
    if not price or pd.isna(price):
      logger.warning("Could not get price data within timeout period")

    # Cancel the market data subscription when done
    self.ibkr.cancelMktData(self.contract)

    return price
