"""
Template for IB API trading bot.
"""
import os
import random
from bot import main

if __name__ == "__main__":

    CONFIG = {
        'server': {
            'trading_mode': os.getenv('TRADING_MODE', 'paper'),
            'ib_gateway_host': os.getenv('IB_GATEWAY_HOST', '127.0.0.1'),
            'ib_gateway_port': os.getenv('IB_GATEWAY_PORT', '4001'),
            'client_id': os.getenv('CLIENT_ID', random.randint(1001,9999)),
        },
        'settings': {
            'timezone': 'US/Eastern',
            'timeformat': "%Y-%m-%dT%H%M"
        },
        'downloader': {
            'mkt_data_type': os.getenv('MKT_DATA_TYPE', '4'),
            'symbol': os.getenv('SYMBOL', 'SPX'),
            'trading_class': os.getenv('TRADING_CLASS', 'SPXW'),
        },
        'persistence': {
            'backend': os.getenv('STORAGE_BACKEND', 'file'),
            'mount_path': os.getenv('STORAGE_MOUNT_PATH', '/data'),
            'gcs_bucket_name': os.getenv('GCS_BUCKET_NAME')
        }
    }


    bot = main.Bot(config=CONFIG)
    bot.run()
