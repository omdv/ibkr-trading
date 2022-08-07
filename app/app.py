"""
Template for IB API trading bot.
"""

import logging
import os
import datetime as dt
import time
import random
import functools
import holidays
import ib_insync
import schedule
import pytz
from google.cloud import storage


logging.basicConfig(level=logging.DEBUG)
bot_logger = logging.getLogger('bot')
ib_logger = logging.getLogger('ib')

us_holidays = holidays.US()

def print_elapsed_time(func):
    """
    Wrapper to bring elapsed time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        bot_logger.info('Running job %s', func.__name__)
        result = func(*args, **kwargs)
        bot_logger.info('Job %s completed in %ss', func.__name__, time.time() - start_timestamp)
        return result

    return wrapper


class Bot():
    """Class representing a trading bot."""
    def __init__(self, params):
        self.config = params
        self.ibkr = None
        self.ptf = []
        self.options = []
        self.ptf_stats = {}
        self.pos_stats = {}
        self.timezone = pytz.timezone('US/Eastern')
        self.tfmt = "%Y-%m-%dT%H%M"


    def __del__(self):
        try:
            self.ibkr.disconnect()
        except AttributeError:
            pass


    def connect_to_gateway(self):
        """
        Create and connect IB client
        """
        host = self.config['IB_GATEWAY_HOST']
        port = self.config['IB_GATEWAY_PORT']

        self.ibkr = ib_insync.IB()
        self.ibkr.connect(
            host = host,
            port = port,
            clientId =self.config['CLIENT_ID'],
            timeout = 15,
            readonly = True)
        ib_logger.debug('Connected to IB on %s:%s', host, port)
        self.ibkr.reqMarketDataType(self.config['MKT_DATA_TYPE'])


    def after_hours(self, now = None):
        """
        Check if market is open, got it from /u/numbuh-0
        """
        if not now:
            now = dt.datetime.now(self.timezone)

        # add 1hr before and after market close
        open_time = dt.time(hour = 8, minute = 30, second = 0)
        close_time = dt.time(hour = 17, minute = 0, second = 0)

        if now.strftime('%Y-%m-%d') in us_holidays:
            return True
        if (now.time() < open_time) or (now.time() > close_time):
            return True
        if now.date().weekday() > 4:
            return True

        return False


    @print_elapsed_time
    def get_option_chain(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        if self.after_hours():
            bot_logger.info("Market is closed, skipping")
            return

        bot_logger.info("Attempting to get options")
        self.connect_to_gateway()

        under = ib_insync.Index(self.config['SYMBOL'], 'CBOE')
        [under] = self.ibkr.qualifyContracts(under)
        self.ibkr.reqMarketDataType(2)
        [ticker] = self.ibkr.reqTickers(under)
        under_value = ticker.marketPrice()
        bot_logger.debug('Underlying value: %s', under_value)

        chains = self.ibkr.reqSecDefOptParams(under.symbol, '', under.secType, under.conId)
        chain = next(c for c in chains if
            c.tradingClass == self.config['TRADING_CLASS'] and c.exchange == 'SMART')

        strikes = [strike for strike in chain.strikes
            if under_value*0.9 < strike < under_value*1.1]

        expirations = sorted(exp for exp in chain.expirations)[:3]
        bot_logger.debug(expirations)

        rights = ['P', 'C']
        contracts = [ib_insync.Option(
                self.config['SYMBOL'],
                expiration,
                strike,
                right,
                'SMART',
                tradingClass=self.config['TRADING_CLASS'])
            for right in rights
            for expiration in expirations
            for strike in strikes]

        contracts = self.ibkr.qualifyContracts(*contracts)
        bot_logger.info('Found %s contracts', len(contracts))

        tickers = self.ibkr.reqTickers(*contracts)
        self.save_option_chain(tickers)

        self.ibkr.disconnect()


    def save_option_chain(self, tickers):
        """
        Aux function to serialize and save the chain
        """
        tickers = ib_insync.util.df(tickers)
        filename = dt.datetime.now(self.timezone).strftime(self.tfmt)

        contract_attr = [
            'symbol',
            'localSymbol',
            'right',
            'strike',
            'lastTradeDateOrContractMonth'
        ]
        for attr in contract_attr:
            tickers[attr] = tickers['contract'].apply(lambda x, a=attr: getattr(x, a))

        greeks_attr = [
            'impliedVol',
            'delta',
            'optPrice',
            'gamma',
            'vega',
            'theta',
            'undPrice']

        try:
            for attr in greeks_attr:
                tickers[attr] = tickers['modelGreeks'].apply(lambda x, a=attr: getattr(x, a))
            tickers = tickers[contract_attr + greeks_attr+['ask', 'bid']]

        except AttributeError:
            tickers = tickers[contract_attr + ['ask', 'bid']]

        if self.config['STORAGE_BACKEND'] == 'gcs':
            client = storage.Client()
            bucket = client.get_bucket(self.config['GCS_BUCKET_NAME'])
            bucket.blob(f'options/{filename}.csv').upload_from_string(
                tickers.to_csv(index=False),
                'text/csv')
        else:
            tickers.to_csv(f'/tmp/{filename}', index=False)


    def run(self):
        """
        Run loop
        """
        # schedule.every().hour.at(":00").do(self.get_option_chain)
        # schedule.every().hour.at(":20").do(self.get_option_chain)
        # schedule.every().hour.at(":20").do(self.get_option_chain)
        schedule.every(10).minutes.do(self.get_option_chain)

        bot_logger.info("Started schedule")
        while True:
            schedule.run_pending()
            time.sleep(1)



if __name__ == "__main__":
    config = {
        'TRADING_MODE': os.getenv('TRADING_MODE', 'paper'),
        'IB_GATEWAY_HOST': os.getenv('IB_GATEWAY_HOST', '127.0.0.1'),
        'IB_GATEWAY_PORT': os.getenv('IB_GATEWAY_PORT', '4001'),
        'CLIENT_ID': os.getenv('CLIENT_ID', random.randint(1001,9999)),
        'MKT_DATA_TYPE': os.getenv('MKT_DATA_TYPE', '4'),
        'SYMBOL': os.getenv('SYMBOL', 'SPX'),
        'TRADING_CLASS': os.getenv('TRADING_CLASS', 'SPXW'),
        'STORAGE_BACKEND': os.getenv('STORAGE_BACKEND', 'local'),
        'GCS_BUCKET_NAME': os.getenv('GCS_BUCKET_NAME'),
    }

    bot = Bot(params=config)
    bot.run()
