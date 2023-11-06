"""
Template for IB API trading bot.
"""
import time
import schedule

from pydantic_settings import BaseSettings

from databot import DataBot
from databot import logger

class Settings(BaseSettings):
    """
    Read server settings
    """
    ib_gateway_host: str
    ib_gateway_port: str
    timezone: str = "US/Eastern"
    timeformat: str = "%Y-%m-%dT%H%M"
    storage: str = "file"
    storage_path: str = "/data"

if __name__ == "__main__":

    settings = Settings()
    bot = DataBot(settings)

    schedule.every().hour.at(":30").do(bot.get_options_chain)
    schedule.every().hour.at(":00").do(bot.get_options_chain)
    schedule.every().hour.at(":00").do(bot.get_positions)

    # schedule.every(5).minutes.do(bot.get_options_chain)

    logger.info("Started schedule")
    while True:
        schedule.run_pending()
        time.sleep(1)
