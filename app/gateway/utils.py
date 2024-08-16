"""
Utility functions.
"""

import datetime as dt
from holidays.financial.ny_stock_exchange import NYSE

def if_market_open(timezone, now = None):
  """
  Check if market is open, got it from /u/numbuh-0
  """
  if not now:
    now = dt.datetime.now(timezone)

  # add 1hr before and after market close
  open_time = dt.time(hour = 8, minute = 30, second = 0)
  close_time = dt.time(hour = 16, minute = 0, second = 0)

  nyse_holidays = NYSE(years = now.year)
  if now.strftime('%Y-%m-%d') in nyse_holidays:
    return False
  if (now.time() < open_time) or (now.time() > close_time):
    return False
  if now.date().weekday() > 4:
    return False
  return True
