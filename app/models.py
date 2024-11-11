"""
Data models
"""

import datetime as dt
from typing import Optional
from sqlmodel import Field, SQLModel
from ib_async.objects import Position
from ib_async.contract import Contract


class Contracts(SQLModel, table=True):
  """
  Contracts SQLModel
  """

  id: int = Field(primary_key=True)
  symbol: str
  sec_type: str
  currency: str
  exchange: Optional[str] = None
  multiplier: Optional[str] = None
  expiry: Optional[str] = None
  strike: Optional[float] = None
  right: Optional[str] = None
  trading_class: Optional[str] = None
  local_symbol: Optional[str] = None

  def __init__(self, contract: Contract):
    self.id = contract.conId
    self.symbol = contract.symbol
    self.sec_type = contract.secType
    self.currency = contract.currency
    self.exchange = contract.exchange
    self.multiplier = contract.multiplier
    self.expiry = contract.lastTradeDateOrContractMonth
    self.strike = contract.strike
    self.right = contract.right
    self.trading_class = contract.tradingClass
    self.local_symbol = contract.localSymbol


class Positions(SQLModel, table=True):
  """
  Positions SQLModel
  """

  id: int = Field(primary_key=True)
  timestamp: int
  account: str
  contract_id: int
  contract_type: str
  symbol: str
  expiry: Optional[str] = None
  strike: Optional[float] = None
  right: Optional[str] = None
  trading_class: Optional[str] = None
  position: float
  avg_cost: float

  def __init__(self, position: Position):
    self.timestamp = dt.datetime.now().timestamp()
    self.account = position.account
    self.contract_id = position.contract.conId
    self.contract_type = position.contract.secType
    self.symbol = position.contract.symbol
    self.expiry = position.contract.lastTradeDateOrContractMonth
    self.strike = position.contract.strike
    self.right = position.contract.right
    self.trading_class = position.contract.tradingClass
    self.position = position.position
    self.avg_cost = position.avgCost


class OptionSpreads(SQLModel, table=False):
  """
  OptionSpread SQLModel
  """

  id: int = Field(primary_key=True)
  expiry: str
  symbol: str
  size: float
  strike: float
  protection: float
  right: str

  def __init__(self, expiry: str, legs: list[dict]):
    """
    Logic to build the spread
    """
    self.expiry = expiry
    self.symbol = legs[0]["symbol"]

    # checks
    if len(legs) != 2:
      return None
    if legs[0]["size"] + legs[1]["size"] != 0:
      return None
    if legs[0]["right"] != legs[1]["right"]:
      return None

    sorted_legs = sorted(legs, key=lambda x: x["strike"])

    self.size = abs(legs[0]["size"])
    self.right = legs[0]["right"]
    self.protection = abs(sorted_legs[0]["strike"] - sorted_legs[1]["strike"])

    if legs[0]["right"] == "C":
      self.strike = sorted_legs[0]["strike"]
    elif legs[0]["right"] == "P":
      self.strike = sorted_legs[1]["strike"]
