"""
Parse and store the portfolio positions.
"""
import logging
import datetime as dt

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the base class
Base = declarative_base()

class Contract(Base):
  """
  Contract specifications class
  """
  __tablename__ = 'contracts'

  id = Column(Integer, primary_key=True)
  symbol = Column(String, nullable=False)
  sec_type = Column(String, nullable=False)
  currency = Column(String, nullable=False)
  exchange = Column(String, nullable=True)
  multiplier = Column(String, nullable=True)
  expiry = Column(String, nullable=True)
  strike = Column(Float, nullable=True)
  right = Column(String, nullable=True)
  trading_class = Column(String, nullable=True)
  local_symbol = Column(String, nullable=True)

class Position(Base):
  """
  Positions class
  """
  __tablename__ = 'positions'

  id = Column(Integer, primary_key=True)
  timestamp = Column(Integer, nullable=False)
  account = Column(String, nullable=False)
  contract = Column(Integer, nullable=False)
  position = Column(Float, nullable=False)
  avg_cost = Column(Float, nullable=False)

logger = logging.getLogger(__name__)


def save_positions(config, positions):
  """
  Parse the positions and store them
  """
  try:
    engine = create_engine(f'sqlite:///{config.storage_path}')
  except Exception as e: # pylint: disable=W0718
    logger.error("Error connecting to database: %s", e)

  try:
    Base.metadata.create_all(engine)
  except Exception as e: # pylint: disable=W0718
    logger.error("Error creating tables: %s", e)

  session_maker = sessionmaker(bind=engine)
  timestamp = int(dt.datetime.now().timestamp())

  try:
    with session_maker() as session:
      for pos in positions:
        contract = Contract(
          id = pos.contract.conId,
          symbol = pos.contract.symbol,
          sec_type = pos.contract.secType,
          currency = pos.contract.currency,
          exchange = pos.contract.exchange,
          multiplier = pos.contract.multiplier,
          expiry = pos.contract.lastTradeDateOrContractMonth,
          strike = pos.contract.strike,
          right = pos.contract.right,
          local_symbol = pos.contract.localSymbol,
          trading_class = pos.contract.tradingClass
        )

        position = Position(
          timestamp = timestamp,
          account = pos.account,
          contract = pos.contract.conId,
          position = pos.position,
          avg_cost = pos.avgCost
        )
        if session.query(Contract).get(contract.id) is None:
          session.add(contract)
        session.add(position)
        session.commit()
  except Exception as e: # pylint: disable=W0718
    logger.error("Error saving positions: %s", e)

  logger.info("Saved positions")
