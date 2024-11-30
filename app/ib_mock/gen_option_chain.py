"""
Generate a mocked option chain
"""

from ib_async import OptionChain
from trader.trading_logic import next_trading_day


def gen_option_chain():
  """Generate a mocked option chain"""

  chain = OptionChain(
    underlyingConId=1000000000,
    exchange="SMART",
    tradingClass="SPXW",
    multiplier=100,
    expirations=[next_trading_day()],
    strikes=[5900, 5890, 5880, 5870, 5860],
  )
  return [chain]
