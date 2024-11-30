"""
Generate random mock positions
"""

import random
import datetime as dt
from ib_async.objects import Position, Contract

from .common import local_symbol, contract_id

random.seed(42)


def gen_positions(num_positions: int = 10) -> list[Position]:
  """Generate random positions"""
  account = "U1234567"
  positions = [
    Position(
      account=account,
      contract=Contract(
        symbol="SPX",
        secType="STK",
        exchange="BATS",
        currency="USD",
        localSymbol="SPX",
        tradingClass="SPX",
      ),
      position=500.0,
      avgCost=100.0,
    ),
    Position(
      account=account,
      contract=Contract(
        symbol="SPX",
        secType="OPT",
        lastTradeDateOrContractMonth=dt.datetime.now().strftime("%Y%m%d"),
        strike=6000.0,
        right="P",
        multiplier="100",
        currency="USD",
        tradingClass="SPXW",
      ),
      position=10.0,
      avgCost=128.70595,
    ),
    Position(
      account=account,
      contract=Contract(
        symbol="SPX",
        secType="OPT",
        lastTradeDateOrContractMonth=dt.datetime.now().strftime("%Y%m%d"),
        strike=6100.0,
        right="P",
        multiplier="100",
        currency="USD",
        tradingClass="SPXW",
      ),
      position=-10.0,
      avgCost=88.79595,
    ),
  ]
  for position in positions:
    position.contract.localSymbol = local_symbol(position.contract)
    position.contract.conId = contract_id(position.contract)
  return positions
