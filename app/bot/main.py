"""
Bot class.
"""

import time
import datetime as dt

import pytz
import schedule
import ib_insync

from .utils import bot_logger, ib_logger
from .utils import save_options_to_file, save_options_to_sqlite, save_options_to_gcs
from .utils import if_after_hours, print_elapsed_time


class ConnectionIssue(Exception):
    """ My custom exception class. """


class Bot():
    """Class representing a trading bot."""
    def __init__(self, config):
        self.config = config
        self.ibkr = None
        self.config['settings']['timezone'] =\
            pytz.timezone(self.config['settings']['timezone'])

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
                clientId = dt.datetime.utcnow().strftime('%H%M'),
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
            time.sleep(10)
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

        switcher = {
            'gcs': save_options_to_gcs,
            'file': save_options_to_file,
            'sqlite': save_options_to_sqlite
        }

        func = switcher.get(self.config['persistence']['backend'], "None")
        func(self.config, tickers)


    @print_elapsed_time
    def _get_option_chain(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        if if_after_hours(self.config['settings']['timezone']):
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
            c.tradingClass == self.config['downloader']['trading_class'] and c.exchange == 'SMART')

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

        schedule.every(str(self.config['downloader']['frequency'])).minutes.do(self._get_option_chain)

        bot_logger.info("Started schedule")
        while True:
            schedule.run_pending()
            time.sleep(1)
