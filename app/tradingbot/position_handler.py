from ib_async.objects import Position
from collections import defaultdict
from .models import OptionSpreads


def parse_positions(positions: list[Position]):
  """
  Parse the positions and return option spreads
  """
  by_expiry = defaultdict(list)
  for pos in positions:
    try:
      if pos.contract.secType == "OPT":
        by_expiry[pos.contract.lastTradeDateOrContractMonth].append(
          {
            "symbol": pos.contract.symbol,
            "size": pos.position,
            "strike": pos.contract.strike,
            "right": pos.contract.right,
          }
        )
    except AttributeError:
      pass
  expiries = {e: g for e, g in by_expiry.items() if len(g) > 1}

  spreads = []
  for k, v in expiries.items():
    spread = OptionSpreads(expiry=k, legs=v)
    print(spread)
    spreads.append(spread)
  return spreads
