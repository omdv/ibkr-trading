from datetime import datetime
from sqlmodel import Field, SQLModel
from ib_async.order import Order
from storage.db import DB


class MyTrade(SQLModel, table=True):
  """
  Custom Trade model with SQL support
  """

  __tablename__ = "trades"

  id: int = Field(primary_key=True)
  timestamp: datetime = Field(default_factory=datetime.utcnow)
  contract: int
  trade: float
  price: float
  commission: float

  @classmethod
  def from_ib_trade(cls, trade: Order) -> "MyTrade":
    """Create a MyTrade from an IB Trade object"""
    return cls(
      contract=trade.contract,
      trade=trade.trade,
      price=trade.price,
      commission=trade.commission,
    )

  @classmethod
  def save(cls, db: DB, trade: "MyTrade") -> "MyTrade":
    """Save the MyTrade to the database"""
    with db.get_session() as session:
      session.add(trade)
      session.commit()
      session.refresh(trade)
    return trade
