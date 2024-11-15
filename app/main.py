"""
Gateway - interactions with TWS API
"""

import datetime as dt
import logging
import schedule
import time

from ib_async import IB

from settings import Settings
from position_handler import parse_option_spreads
from trade_logic import need_to_open_spread

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logging.getLogger("ib_async").setLevel(logging.INFO)
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
    self.spreads = None
    self.positions = None
    self.net_value = None
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

    try:
      self.positions = self.ibkr.positions()
    except Exception as e:
      logger.error("Error getting positions: %s", e)
      raise e

  def trade_loop(self):
    """
    Main trading loop
    """

    # Get existing option spreads
    existing_spreads = parse_option_spreads(self.ibkr.positions())
    self.spreads = existing_spreads
    logger.info("Found the following spreads: %s", existing_spreads)

    # 3. Identify which spreads needs to be closed
    # 3.1. Check trade logic - delta, etc
    if not need_to_open_spread(self.ibkr, existing_spreads):
      logger.info("No spreads need to be opened")
      return

    # 3.2. Close the spread with execution logic
    if self.config.close_spread_on_expiry:
      # TODO: implement the closing logic
      pass

    # 4. Identify which spreads needs to be opened
    # 4.1. Check trade logic and create new contract
    # contract = get_spread_to_open(self.ibkr, existing_spreads)

    # 4.2. Open the spread with execution logic - get the price, wait for the fill
    # trade_execution(self.ibkr, contract)

    # 5. Logging


if __name__ == "__main__":
  settings = Settings()
  bot = TradingBot(settings)

  schedule.every(10).minutes.do(bot.trade_loop)
  schedule.run_all()

  logger.info("Started schedule")
  while True:
    schedule.run_pending()
    time.sleep(1)
