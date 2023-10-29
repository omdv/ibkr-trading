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

    # positions_config = copy.deepcopy(BASE_CONFIG)
    # positions_config['download'] = {
    #     'frequency': os.getenv('DOWNLOAD_EVERY_MINS', '5'),
    # }

    # options_config = copy.deepcopy(BASE_CONFIG)
    # options_config['download'] = {
    #     'frequency': os.getenv('DOWNLOAD_EVERY_MINS', '5'),
    #     'mkt_data_type': os.getenv('MKT_DATA_TYPE', '4'),
    #     'symbol': os.getenv('SYMBOL', 'SPX'),
    #     'trading_class': os.getenv('TRADING_CLASS', 'SPXW'),
    # }

    schedule.every(5).minutes.do(bot.get_positions)
    schedule.every(5).minutes.do(bot.get_options_chain)

    logger.info("Started schedule")
    while True:
        schedule.run_pending()
        time.sleep(1)
