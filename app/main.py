"""
Template for IB API trading bot.
"""

import logging
from pydantic_settings import BaseSettings
from tradingbot import TradingBot

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logging.getLogger("ib_async").setLevel(logging.INFO)


class Settings(BaseSettings):
  """
  Read server settings
  """

  ib_gateway_host: str
  ib_gateway_port: str
  timezone: str = "US/Eastern"
  timeformat: str = "%Y-%m-%dT%H%M"
  storage: str = "file"
  storage_path: str = "./data/state.db"


if __name__ == "__main__":
  settings = Settings()
  bot = TradingBot(settings)
  bot.trade_loop()
  # bot.parse_positions()
  # schedule.every().hour.at(":00").do(bot.save_positions)
  # schedule.run_all()

  # logger.info("Started schedule")
  # while True:
  #   schedule.run_pending()
  #   time.sleep(1)
