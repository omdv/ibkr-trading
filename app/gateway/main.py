"""
Gateway - interactions with TWS API
"""
import datetime as dt
import logging
import ib_insync

from .positions import save_positions

logger = logging.getLogger(__name__)

class ConnectionIssue(Exception):
  """ My custom exception class. """


class Gateway():
  """Class representing a gateway and interactions."""
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

    self.ibkr = ib_insync.IB()

    try:
      self.ibkr.connect(
        host = host,
        port = port,
        clientId = dt.datetime.now(dt.UTC).strftime('%H%M'),
        timeout = 15,
        readonly = True)
    except ConnectionIssue as e:
      logger.error("Error connecting to IB: %s", e)
    logger.debug('Connected to IB on %s:%s', host, port)


  def get_positions(self):
    """
    Handle interactions with API and raise related exceptions here
    """
    try:
      positions = self.ibkr.positions()
      return positions
    except Exception as e: # pylint: disable=W0718
      logger.error("Error getting positions: %s", e)
      return []


  def save_positions(self):
    """
    Save the positions
    """
    save_positions(self.config, self.get_positions())
    logger.info("Saved positions")
