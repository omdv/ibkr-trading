"""
Template for IB API trading bot.
"""
import os
import time
import schedule

from infobots.base import InfoBot
from infobots.positions import PositionsBot
from infobots.options import OptionsBot
from infobots.utils import logger

if __name__ == "__main__":

    BASE_CONFIG = {
        'server': {
            'trading_mode': os.getenv('TRADING_MODE', 'paper'),
            'ib_gateway_host': os.getenv('IB_GATEWAY_HOST', '127.0.0.1'),
            'ib_gateway_port': os.getenv('IB_GATEWAY_PORT', '4001'),
        },
        'settings': {
            'timezone': 'US/Eastern',
            'timeformat': "%Y-%m-%dT%H%M"
        },
        'persist': {
            'backend': os.getenv('STORAGE_BACKEND', 'file'),
            'mount_path': os.getenv('STORAGE_MOUNT_PATH', '/data'),
            'gcs_bucket_name': os.getenv('GCS_BUCKET_NAME'),
            'sqlite_filename': 'example.db'
        }
    }

    positions_config = BASE_CONFIG
    positions_config['download'] = {
        'frequency': os.getenv('DOWNLOAD_EVERY_MINS', '1'),
    }

    options_config = BASE_CONFIG
    options_config['download'] = {
        'frequency': os.getenv('DOWNLOAD_EVERY_MINS', '30'),
        'mkt_data_type': os.getenv('MKT_DATA_TYPE', '4'),
        'symbol': os.getenv('SYMBOL', 'SPX'),
        'trading_class': os.getenv('TRADING_CLASS', 'SPXW'),
    }

    base = InfoBot(BASE_CONFIG)
    base.test_connection()

    bots = [
        OptionsBot(options_config),
        PositionsBot(positions_config)
    ]

    for bot in bots:
        schedule.every(
            int(bot.config['download']['frequency'])).minutes.do(
                bot.run)


    logger.info("Started schedule")
    while True:
        schedule.run_pending()
        time.sleep(1)
