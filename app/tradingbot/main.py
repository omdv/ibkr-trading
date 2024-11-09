"""
Gateway - interactions with TWS API
"""

import datetime as dt
import logging

from ib_async import IB

from .position_handler import parse_positions
from .contract_handler import create_spread_contract
from .trade_handler import trade_execution

logger = logging.getLogger(__name__)


class ConnectionIssue(Exception):
  """My custom exception class."""


class TradingBot:
  """
  Trading bot class, which orchestrates interactions with the IB API
  and trade logic
  """

  def __init__(self, settings):
    self.config = settings
    self.ibkr = None
    self._connect()

  def __del__(self):
    try:
      self.ibkr.disconnect()
    except AttributeError:
      pass

  def _connect(self):
    """
    Create and connect IB client
    """
    host = self.config.ib_gateway_host
    port = self.config.ib_gateway_port

    self.ibkr = IB()

    try:
      self.ibkr.connect(
        host=host,
        port=port,
        clientId=dt.datetime.now(dt.UTC).strftime("%H%M"),
        timeout=120,
        readonly=True,
      )
      self.ibkr.RequestTimeout = 30
    except ConnectionIssue as e:
      logger.error("Error connecting to IB: %s", e)
    logger.debug("Connected to IB on %s:%s", host, port)

  def _get_positions(self):
    """
    Handle interactions with API and raise related exceptions here
    """
    try:
      positions = self.ibkr.positions()
      return positions
    except Exception as e:
      logger.error("Error getting positions: %s", e)
      return []

  def trade_loop(self):
    """
    Main trading loop
    """

    # 1. Get raw positions
    positions = self._get_positions()

    # 2. Get existing option spreads
    spreads = parse_positions(positions)
    logger.info("Found the following spreads: %s", spreads)

    # 3. Identify which spreads needs to be closed
    # 3.1. Check trade logic - delta, etc
    # 3.2. Close the spread with execution logic

    # 4. Identify which spreads needs to be opened
    # 4.1. Check trade logic and create new combo contract
    contract = create_spread_contract(self.ibkr)

    # 4.2. Open the spread with execution logic - get the price, wait for the fill
    trade_execution(self.ibkr, contract)

    # 5. Logging
