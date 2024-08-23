"""
Parse and store the portfolio positions.
"""

import logging
import datetime as dt
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy import exists
from .models import Contracts, Positions


logger = logging.getLogger(__name__)

# def parse_positions(config, positions):
#   """
#   Find options positions in the portfolio
#   """
#   options_positions = []
#   for pos in positions:
#     if pos.contract.secType == 'OPT':
#       options_positions.append(pos)

#   print(options_positions)


def save_positions(config, positions):
  """
  Parse the positions and store them
  """
  try:
    engine = create_engine(f"sqlite:///{config.storage_path}")
  except Exception as e:  # pylint: disable=W0718
    logger.error("Error connecting to database: %s", e)

  try:
    SQLModel.metadata.create_all(engine)
  except Exception as e:  # pylint: disable=W0718
    logger.error("Error creating tables: %s", e)

  timestamp = int(dt.datetime.now().timestamp())

  try:
    with Session(engine) as session:
      for pos in positions:
        contract = Contracts(
          id=pos.contract.conId,
          symbol=pos.contract.symbol,
          sec_type=pos.contract.secType,
          currency=pos.contract.currency,
          exchange=pos.contract.exchange,
          multiplier=pos.contract.multiplier,
          expiry=pos.contract.lastTradeDateOrContractMonth,
          strike=pos.contract.strike,
          right=pos.contract.right,
          local_symbol=pos.contract.localSymbol,
          trading_class=pos.contract.tradingClass,
        )

        position = Positions(
          timestamp=timestamp,
          account=pos.account,
          contract=pos.contract.conId,
          position=pos.position,
          avg_cost=pos.avgCost,
        )

        query = select(exists().where(Contracts.id == contract.id))
        if session.exec(query).first() is False:
          session.add(contract)

        session.add(position)
        session.commit()
  except Exception as e:  # pylint: disable=W0718
    logger.error("Error saving positions: %s", e)

  logger.info("Saved positions")
