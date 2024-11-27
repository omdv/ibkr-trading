"""
Data models only
"""

from sqlmodel import Field, SQLModel
from ib_async.contract import Option


class PositionOption(Option):
  """
  Extended Option class that includes position size
  """

  def __init__(self, option: Option, position_size: float):
    super().__init__(
      conId=option.conId,
      symbol=option.symbol,
      lastTradeDateOrContractMonth=option.lastTradeDateOrContractMonth,
      strike=option.strike,
      tradingClass=option.tradingClass,
      right=option.right,
      multiplier=option.multiplier,
      exchange=option.exchange,
      currency=option.currency,
      localSymbol=option.localSymbol,
    )
    self.position_size = position_size

  def to_dict(self):
    base_dict = super().to_dict() if hasattr(super(), "to_dict") else vars(super())
    return {**base_dict, "position_size": self.position_size}

  def __str__(self) -> str:
    """Return a string representation of the PositionOption"""
    return self.localSymbol.replace(" ", "")

  def __repr__(self) -> str:
    """Return a string representation of the PositionOption"""
    return f"PositionOption(localSymbol={self.localSymbol}, position_size={self.position_size})"


class OptionSpread(SQLModel, table=False):
  """
  OptionSpread SQLModel
  """

  id: int = Field(primary_key=True)
  expiry: str
  symbol: str
  tradingClass: str
  size: float
  strike: float
  protection: float
  right: str
  legs: list[PositionOption]

  @staticmethod
  def validate_legs(legs: list[PositionOption]) -> bool:
    """Validate the legs of the spread"""
    if len(legs) != 2:
      raise ValueError("Spread must have exactly 2 legs")

    if legs[0].position_size + legs[1].position_size != 0:
      raise ValueError("Legs must have opposite sizes")

    if legs[0].right != legs[1].right:
      raise ValueError("Both legs must be the same type (calls or puts)")

    return True

  def __init__(self, legs: list[PositionOption]):
    """Initialize an option spread"""
    self.validate_legs(legs)

    self.legs = sorted(legs, key=lambda x: x.position_size)

    self.expiry = self.legs[0].lastTradeDateOrContractMonth
    self.symbol = self.legs[0].symbol
    self.size = self.legs[0].position_size
    self.right = self.legs[0].right
    self.protection = abs(self.legs[0].strike - self.legs[1].strike)
    self.strike = (
      self.legs[0].strike if self.legs[0].right == "P" else self.legs[1].strike
    )
    self.tradingClass = self.legs[0].tradingClass

  def __str__(self) -> str:
    """Return a string description of the spread"""
    return f"{self.size} x {self.legs[0]}|{str(self.legs[1])[-8:]}"

  def __repr__(self) -> str:
    """Return a string representation of the OptionSpread"""
    return f"OptionSpread(legs={self.legs})"


if __name__ == "__main__":
  option = Option(
    symbol="AAPL", right="C", strike=150, lastTradeDateOrContractMonth="20241213"
  )
  print("Option dict:", option.__dict__)

  position_option = PositionOption(option=option, position_size=100)
  print("PositionOption dict:", position_option.__dict__)
