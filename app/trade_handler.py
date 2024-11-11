import logging
import datetime as dt

from ib_async import IB
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
  ibkr.reqMarketDataType(1 if is_market_open else 3)

  ticker = ibkr.reqMktData(contract)
  price = ticker.last

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
