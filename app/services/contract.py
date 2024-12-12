from loguru import logger
import datetime as dt
import pandas as pd
from ib_async import IB, Contract
from services.utilities import is_market_open


class ContractService:
  def __init__(self, ibkr: IB, contract: Contract):
    self.ibkr = ibkr
    self.contract = contract

  def get_current_price(self, price_type: str = "last") -> float:
    """
    Get the current price of the contract
    """
    logger.debug("Getting price for contract: {}", self.contract)
    logger.debug("Contract conId: {}", self.contract.conId)

    # Set market data type based on market status
    self.ibkr.reqMarketDataType(1 if is_market_open(self.ibkr) else 2)

    # Qualify the contract
    self.ibkr.qualifyContracts(self.contract)

    # Request market data
    ticker = self.ibkr.reqMktData(self.contract)

    # Wait for market data to arrive (timeout after 20 seconds)
    timeout = 20
    start_time = dt.datetime.now()
    while (not ticker.last or pd.isna(ticker.last)) and (
      dt.datetime.now() - start_time
    ).seconds < timeout:
      self.ibkr.sleep(0.1)

    price = getattr(ticker, price_type)
    if not price or pd.isna(price):
      logger.error("Could not get price data within timeout period")

    # Cancel the market data subscription when done
    self.ibkr.cancelMktData(self.contract)

    return price
