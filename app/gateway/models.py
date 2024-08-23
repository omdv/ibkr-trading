"""
Data models
"""

from typing import Optional
from sqlmodel import Field, SQLModel


class Contracts(SQLModel, table=True):
    """
    Contract specifications class
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


class Positions(SQLModel, table=True):
    """
    Positions class
    """

    id: int = Field(primary_key=True)
    timestamp: int
    account: str
    contract: int
    position: float
    avg_cost: float
