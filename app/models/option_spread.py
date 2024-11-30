from sqlmodel import Field, SQLModel
from .option_sized import OptionWithSize, OptionWithSizeListEncoder
from storage.db import DB


class OptionSpread(SQLModel, table=True):
  """
  Custom OptionSpread model with SQL support
  """

  __tablename__ = "option_spreads"

  id: int = Field(primary_key=True)
  expiry: str
  symbol: str
  tradingClass: str
  size: int
  strike: float
  protection: float
  right: str
  legs: list[OptionWithSize] = Field(sa_type=OptionWithSizeListEncoder)

  @staticmethod
  def validate_legs(legs: list[OptionWithSize]) -> bool:
    """Validate the legs of the spread"""
    if len(legs) != 2:
      raise ValueError("Spread must have exactly 2 legs")

    if legs[0].position_size + legs[1].position_size != 0:
      raise ValueError("Legs must have opposite sizes")

    if legs[0].right != legs[1].right:
      raise ValueError("Both legs must be the same type (calls or puts)")

    return True

  def __init__(self, legs: list[OptionWithSize]):
    """Initialize an option spread"""
    self.validate_legs(legs)

    self.legs = sorted(legs, key=lambda x: x.position_size)

    self.expiry = self.legs[0].lastTradeDateOrContractMonth
    self.symbol = self.legs[0].symbol
    self.size = abs(self.legs[0].position_size)
    self.right = self.legs[0].right
    self.protection = abs(self.legs[0].strike - self.legs[1].strike)
    self.strike = (
      self.legs[0].strike if self.legs[0].right == "P" else self.legs[1].strike
    )
    self.tradingClass = self.legs[0].tradingClass

  def __str__(self) -> str:
    """Return a string description of the spread"""
    return f"{self.legs[0].position_size} x {self.legs[0]}|{str(self.legs[1])[-8:]}"

  def __repr__(self) -> str:
    """Return a string representation of the OptionSpread"""
    return f"OptionSpread(legs={self.legs})"

  def save(self, db: DB) -> "OptionSpread":
    """Save the OptionSpread to the database"""
    with db.get_session() as session:
      session.add(self)
      session.commit()
      session.refresh(self)
    return self
