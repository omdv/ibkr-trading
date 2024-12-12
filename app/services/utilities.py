"""
Utility functions
"""

from loguru import logger
import datetime as dt
from exchange_calendars import get_calendar

from ib_async import IB
from ib_async.contract import Option


def is_market_open(ibkr: IB) -> bool:
  """
  Check if the market is open
  """
  nyse = get_calendar("XNYS")
  current_time = dt.datetime.now(dt.UTC)
  is_market_open = nyse.is_open_on_minute(current_time)
  logger.debug("Market is open: {}", is_market_open)
  return is_market_open


def next_trading_day() -> str:
  """
  Get the next trading day
  """
  nyse = get_calendar("XNYS")
  today = dt.datetime.now()

  # Get the next trading day after today (regardless of market status)
  next_trading_day = nyse.next_open(today.date() + dt.timedelta(days=1)).strftime(
    "%Y%m%d"
  )
  logger.debug("Next trading day: {}", next_trading_day)
  return next_trading_day


def get_delta(ibkr: IB, contracts: list[Option]) -> float:
  """
  Get the delta for an option contract
  TODO: modelGreeks vs lastGreeks
  """
  ibkr.reqMarketDataType(1 if is_market_open(ibkr) else 4)

  logger.debug("Getting delta for contracts: {}", contracts)
  ibkr.qualifyContracts(*contracts)
  tickers = ibkr.reqTickers(*contracts)

  deltas = []
  for ticker in tickers:
    try:
      deltas.append(ticker.modelGreeks.delta)
    except Exception as e:
      logger.error("Error getting delta: {}", e)
      deltas.append(0)
  logger.debug("Deltas: {}", deltas)
  return deltas
