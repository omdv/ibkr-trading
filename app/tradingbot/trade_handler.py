from exchange_calendars import get_calendar
import datetime as dt
import logging
from ib_async import IB
from ib_async.contract import Contract

logger = logging.getLogger(__name__)


def get_contract_price(ibkr: IB, contract: Contract):
  """
  Get the price of the contract
  """
  # Check if market is open
  nyse = get_calendar("XNYS")
  current_time = dt.datetime.now(dt.UTC)
  is_market_open = nyse.is_open_on_minute(current_time)
  logger.warning("Market is open: %s", is_market_open)

  # Set market data type based on market status
  # 1 = Live
  # 2 = Frozen
  # 3 = Delayed
  # 4 = Delayed Frozen
  ibkr.reqMarketDataType(1 if is_market_open else 1)

  ticker = ibkr.reqMktData(contract)
  ibkr.sleep(3)

  # Print the current price
  logger.info("Current price: %s", ticker.last)

  # Don't forget to cancel the market data subscription when done
  ibkr.cancelMktData(contract)


def trade_execution(ibkr: IB, contract: Contract):
  """
  Trade logic
  TODO: Pass the size for each leg
  TODO: Pass the action for each leg
  """
  # Get the price of the contract
  price = get_contract_price(ibkr, contract)
  logger.info("Contract price: %s", price)
