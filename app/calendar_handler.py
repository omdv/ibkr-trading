import datetime as dt
from exchange_calendars import get_calendar


def next_trading_day() -> str:
  """
  Get the next trading day
  """
  nyse = get_calendar("XNYS")  # NYSE (New York Stock Exchange) calendar
  today = dt.datetime.now()

  # Find the next valid trading day
  next_trading_day = nyse.next_open(today).strftime("%Y%m%d")

  return next_trading_day


if __name__ == "__main__":
  print(next_trading_day())
