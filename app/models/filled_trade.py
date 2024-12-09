from datetime import datetime
from sqlmodel import Field, SQLModel
from ib_async.order import Trade
from storage.db import DB
from .option_spread import OptionSpread


class FilledTrade(SQLModel, table=True):
  """
  Custom FilledTrade model with SQL support
  """

  __tablename__ = "trades"

  id: int = Field(primary_key=True)
  timestamp: datetime = Field(default_factory=datetime.now)
  expiry: str
  symbol: str
  strike: float
  width: float
  size: int
  right: str
  filled_price: float
  commission: float

  def __init__(self, contract: OptionSpread, trade: Trade):
    self.timestamp = datetime.now()
    self.expiry = contract.expiry
    self.symbol = str(contract)
    self.strike = contract.strike
    self.width = contract.width
    self.size = contract.size
    self.right = contract.right
    self.filled_price = trade.orderStatus.avgFillPrice
    self.commission = sum(fill.commissionReport.commission for fill in trade.fills)

  def save(self, db: DB) -> "FilledTrade":
    """Save the FilledTrade to the database"""
    with db.get_session() as session:
      session.add(self)
      session.commit()
      session.refresh(self)
    return self
