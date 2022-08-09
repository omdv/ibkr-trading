"""
Bot class.
"""

import time
import datetime as dt

import pytz
import schedule
import ib_insync

from google.cloud import storage

from .utils import bot_logger, ib_logger
from .utils import if_after_hours, print_elapsed_time


class ConnectionIssue(Exception):
    """ my custom exception class """


class Bot():
    """Class representing a trading bot."""
    def __init__(self, config):
        self.config = config
        self.ibkr = None
        self.timezone = pytz.timezone('US/Eastern')


    def __del__(self):
        try:
            self.ibkr.disconnect()
        except AttributeError:
            pass


    def _connect_to_gateway(self):
        """
        Create and connect IB client
        """
        host = self.config['server']['ib_gateway_host']
        port = self.config['server']['ib_gateway_port']

        self.ibkr = ib_insync.IB()

        try:
            self.ibkr.connect(
                host = host,
                port = port,
                clientId =self.config['server']['client_id'],
                timeout = 15,
                readonly = True)
        except ConnectionIssue as e:
            bot_logger.error(e)

        ib_logger.debug('Connected to IB on %s:%s', host, port)

        ib_logger.info('Setting market data type')
        self.ibkr.reqMarketDataType(
            self.config['downloader']['mkt_data_type'])


    def _test_connection(self):
        """
        Test connection to IB
        """
        try:
            self._connect_to_gateway()
            bot_logger.info("Connected to IB")
            self.ibkr.disconnect()
        except ConnectionIssue as e:
            bot_logger.error(e)
            return False
        return True


    def _save_option_chain(self, tickers):
        """
        Aux function to serialize and save the chain
        """
        tickers = ib_insync.util.df(tickers)
        filename = dt.datetime.now(self.timezone).\
            strftime(self.config['settings']['timeformat'])

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

        if self.config['STORAGE_BACKEND'] == 'file':
            tickers.to_csv(f'/data/{filename}', index=False)


    @print_elapsed_time
    def _get_option_chain(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        if if_after_hours(self.timezone):
            bot_logger.info("Market is closed, skipping")
            return

        bot_logger.info("Attempting to get options")

        self._connect_to_gateway()
        bot_logger.info("Connected to IB")

        under = ib_insync.Index(self.config['downloader']['symbol'], 'CBOE')
        [under] = self.ibkr.qualifyContracts(under)
        self.ibkr.reqMarketDataType(2)
        [ticker] = self.ibkr.reqTickers(under)
        under_value = ticker.marketPrice()
        bot_logger.debug('Underlying value: %s', under_value)

        chains = self.ibkr.reqSecDefOptParams(under.symbol, '', under.secType, under.conId)

        chain = next(c for c in chains if
            c.tradingClass == self.config['donwloader']['trading_class'] and c.exchange == 'SMART')

        strikes = [strike for strike in chain.strikes
            if under_value*0.9 < strike < under_value*1.1]

        expirations = sorted(exp for exp in chain.expirations)[:3]
        bot_logger.debug(expirations)

        rights = ['P', 'C']
        contracts = [ib_insync.Option(
                self.config['downloader']['symbol'],
                expiration,
                strike,
                right,
                'SMART',
                tradingClass=self.config['downloader']['trading_class'])
            for right in rights
            for expiration in expirations
            for strike in strikes]

        contracts = self.ibkr.qualifyContracts(*contracts)
        bot_logger.info('Found %s contracts', len(contracts))

        tickers = self.ibkr.reqTickers(*contracts)
        self._save_option_chain(tickers)

        self.ibkr.disconnect()
        bot_logger.info("Disconnected from IB")


    def run(self):
        """
        Run loop
        """

        self._test_connection()

        # schedule.every().hour.at(":00").do(self.get_option_chain)
        # schedule.every().hour.at(":20").do(self.get_option_chain)
        # schedule.every().hour.at(":20").do(self.get_option_chain)
        schedule.every(10).minutes.do(self._get_option_chain)

        bot_logger.info("Started schedule")
        while True:
            schedule.run_pending()
            time.sleep(1)
