import json
import msgpack
import base64
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.types import TypeDecorator

from ib_async.contract import Option


class OptionWithSizeListEncoder(TypeDecorator):
  """Enables binary storage by encoding and decoding on the fly."""

  impl = JSON

  def process_bind_param(self, value, dialect):
    if value is not None:
      packed = msgpack.packb([leg.to_dict() for leg in value])
      return base64.b64encode(packed).decode()
    return None

  def process_result_value(self, value, dialect):
    if value is not None:
      from .option_sized import (
        OptionWithSize,
      )  # Import here to avoid circular imports

      packed = base64.b64decode(value.encode())
      return [OptionWithSize.from_dict(leg) for leg in msgpack.unpackb(packed)]
    return None


class OptionWithSize(Option):
  """
  Custom Option class that includes position size
  """

  def __init__(self, option: Option, position_size: int, delta: float):
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
    self.delta = delta

  @classmethod
  def from_dict(cls, data: dict) -> "OptionWithSize":
    """Create OptionWithSize from a dictionary"""
    option = Option(
      conId=data.get("conId"),
      symbol=data["symbol"],
      lastTradeDateOrContractMonth=data["lastTradeDateOrContractMonth"],
      strike=data["strike"],
      tradingClass=data.get("tradingClass"),
      right=data["right"],
      multiplier=data.get("multiplier"),
      exchange=data.get("exchange", "SMART"),
      currency=data.get("currency", "USD"),
      localSymbol=data.get("localSymbol", ""),
    )
    return cls(
      option=option,
      position_size=data["position_size"],
      delta=data["delta"],
    )

  def to_dict(self):
    base_dict = super().to_dict() if hasattr(super(), "to_dict") else vars(super())
    return {**base_dict, "position_size": self.position_size}

  def to_json(self):
    return json.dumps(self.to_dict())

  def __str__(self) -> str:
    """Return a string representation of the OptionWithSize"""
    return self.localSymbol.replace(" ", "")

  def __repr__(self) -> str:
    """Return a string representation of the OptionWithSize"""
    return f"OptionWithSize(localSymbol={self.localSymbol}, position_size={self.position_size})"
