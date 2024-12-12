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
  bot = TradingBot(settings, mocked=False)

  # Clear any existing jobs (in case of previous abrupt exits)
  schedule.clear()

  # Schedule the trading loop
  schedule.every(1).minute.do(bot.trade_loop)
  logger.info("Trading schedule initialized")

  try:
    while True:
      schedule.run_pending()
      time.sleep(1)
  except KeyboardInterrupt:
    logger.info("Shutting down trading bot gracefully...")
    schedule.clear()
    sys.exit(0)
