import logging
import pandas as pd
from ib_async import IB, Position
from models import OptionSpread, PositionOption

logger = logging.getLogger(__name__)


class PositionsService:
  def __init__(self, ibkr: IB, positions: list[Position]):
    self.ibkr = ibkr
    self.positions = positions

  def get_option_spreads(self) -> list[OptionSpread]:
    """
    Get the option spreads from the positions by grouping options by expiry and symbol
    """

    # Filter and create list of option contracts
    option_positions = []
    for pos in self.positions:
      if pos.contract.secType == "OPT":
        option_positions.append(
          {
            "contract": pos.contract,
            "position_size": int(pos.position),
            "symbol": pos.contract.symbol,
            "expiry": pos.contract.lastTradeDateOrContractMonth,
          }
        )
    df = pd.DataFrame(option_positions)
    grouped = df.groupby(["expiry", "symbol"])

    # Create OptionSpread objects
    spreads = []
    for (expiry, symbol), group in grouped:
      if len(group) > 1:  # Only create spreads with multiple legs
        legs = []
        for leg_data in group.to_dict("records"):
          position_option = PositionOption(
            option=leg_data["contract"], position_size=leg_data["position_size"]
          )
          legs.append(position_option)
        spreads.append(OptionSpread(legs=legs))
    return spreads
