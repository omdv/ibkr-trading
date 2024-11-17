import logging
import datetime as dt

import pandas as pd
from ib_async import IB, Index
from ib_async.contract import Contract
from exchange_calendars import get_calendar


logger = logging.getLogger(__name__)


def get_contract_price(ibkr: IB, contract: Contract):
  """
  Get the price of the contract
  """
  # Check if market is open
  nyse = get_calendar("XNYS")
  current_time = dt.datetime.now(dt.UTC)
  is_market_open = nyse.is_open_on_minute(current_time)
  logger.info("Market is open: %s", is_market_open)

  # Set market data type based on market status
  # 1 = Live
  # 2 = Frozen
  # 3 = Delayed
  # 4 = Delayed Frozen
  ibkr.reqMarketDataType(1 if is_market_open else 2)
  ticker = ibkr.reqMktData(contract)

  # Wait for market data to arrive (timeout after 10 seconds)
  timeout = 10
  start_time = dt.datetime.now()
  while (not ticker.last or pd.isna(ticker.last)) and (
    dt.datetime.now() - start_time
  ).seconds < timeout:
    ibkr.sleep(0.1)

  price = ticker.last
  if not price or pd.isna(price):
    logger.warning("Could not get price data within timeout period")

  # Cancel the market data subscription when done
  ibkr.cancelMktData(contract)
  return price


def trade_execution(ibkr: IB, contract: Contract):
  """
  Trade logic
  TODO: Pass the size for each leg
  TODO: Pass the action for each leg
  """
  # Get the price of the contract
  price = get_contract_price(ibkr, contract)
  logger.info("Contract price: %s", price)


if __name__ == "__main__":
  ibkr = IB()
  ibkr.connect("localhost", 8888)
  contract = Index("SPX", "CBOE")
  print(get_contract_price(ibkr, contract))
