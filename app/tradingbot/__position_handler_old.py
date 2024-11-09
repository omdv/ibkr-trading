"""
Position handling
"""

from ib_insync.objects import Position


class PositionHandler(Position):
  def __init__(self) -> None:
    pass

  # def save_positions(self):
  #   """
  #   Save the positions
  #   """
  #   save_positions(self.config, self.get_positions())
  #   logger.info("Saved positions")

  # def parse_positions(self):
  #   """
  #   Parse the positions
  #   """
  #   options = parse_positions(self.config, self.get_positions())
  #   logger.info("Parsed positions: %s", options)


# class Positions(SQLModel, table=True):
#   """
#   Positions SQLModel
#   """
#   table_name = "positions"

#   id: int = Field(primary_key=True)
#   timestamp: int
#   account: str
#   contract_id: int
#   contract_type: str
#   symbol: str
#   expiry: Optional[str] = None
#   strike: Optional[float] = None
#   right: Optional[str] = None
#   trading_class: Optional[str] = None
#   position: float
#   avg_cost: float

#   def __init__(self, position: Position):
#     self.timestamp = dt.datetime.now().timestamp()
#     self.account = position.account
#     self.contract_id = position.contract.conId
#     self.contract_type = position.contract.secType
#     self.symbol = position.contract.symbol
#     self.expiry = position.contract.lastTradeDateOrContractMonth
#     self.strike = position.contract.strike
#     self.right = position.contract.right
#     self.trading_class = position.contract.tradingClass
#     self.position = position.position
#     self.avg_cost = position.avgCost
