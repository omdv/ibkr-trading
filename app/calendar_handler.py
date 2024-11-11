import datetime as dt
from exchange_calendars import get_calendar


def next_trading_day() -> str:
  """
  Get the next trading day
  """
  nyse = get_calendar("XNYS")  # NYSE (New York Stock Exchange) calendar
  today = dt.datetime.now()

  # Get the next trading day's end
  next_session = nyse.next_session(today.strftime("%Y-%m-%d"))
  next_trading_day = next_session.strftime("%Y%m%d")

  return next_trading_day
