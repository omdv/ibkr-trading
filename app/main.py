"""
Trading bot
"""

import schedule
import time
import sys

from loguru import logger

from settings import Settings
from trader.trading_bot import TradingBot

# Set logging level to INFO
logger.remove()
logger.add(sys.stderr, level="INFO")

if __name__ == "__main__":
  # Create trading bot
  settings = Settings()
  bot = TradingBot(settings, mocked=True)

  schedule.every(2).minutes.do(bot.trade_loop)
  schedule.run_all()
  logger.info("Started schedule")
  while True:
    schedule.run_pending()
    time.sleep(1)
