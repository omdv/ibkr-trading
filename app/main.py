"""
Trading bot
"""

import logging
import schedule
import time

from settings import Settings
from trader.trading_bot import TradingBot

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
  # Create trading bot
  settings = Settings()
  bot = TradingBot(settings, mock_data_path="./mock_data")

  schedule.every(60).minutes.do(bot.trade_loop)
  schedule.run_all()
  logger.info("Started schedule")
  while True:
    schedule.run_pending()
    time.sleep(1)
