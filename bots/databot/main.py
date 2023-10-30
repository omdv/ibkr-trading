"""
DataBot - downloading data from IBKR on schedule
"""
import os
import csv
import datetime as dt

import pytz
import ib_insync

from .utils import logger
from .utils import print_elapsed_time, if_after_hours


class ConnectionIssue(Exception):
    """ My custom exception class. """


class DataBot():
    """Class representing a data downloading bot."""
    def __init__(self, settings):
        self.config = settings
        self.ibkr = None
        self.timezone = pytz.timezone(self.config.timezone)
        self._connect()

    def __del__(self):
        try:
            self.ibkr.disconnect()
        except AttributeError:
            pass

    def _connect(self):
        """
        Create and connect IB client
        """
        host = self.config.ib_gateway_host
        port = self.config.ib_gateway_port

        self.ibkr = ib_insync.IB()

        try:
            self.ibkr.connect(
                host = host,
                port = port,
                clientId = dt.datetime.utcnow().strftime('%H%M'),
                timeout = 15,
                readonly = True)
        except ConnectionIssue as e:
            logger.error(e)

        logger.debug('Connected to IB on %s:%s', host, port)


    def _formatted_now(self):
        """
        Return now() formatted as specified in config.
        """
        return dt.datetime.now(self.timezone).\
                strftime(self.config.timeformat)


    @print_elapsed_time
    def get_positions(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        logger.info("Getting positions for current session")
        positions = self.ibkr.positions()
        logger.info("Saving positions for current session")
        self._save_positions(positions)


    def _save_positions(self, positions):
        """
        Aux function to serialize and save the positions
        """
        result = []
        header = []
        for pos in positions:
            combined = {
                'symbol': pos.contract.localSymbol,
                'position': pos.position,
                'avgcost': pos.avgCost
            }
            header = combined.keys()
            result.append(combined)

        filename = os.path.join(
            self.config.storage_path,
            'positions_'+self._formatted_now())

        logger.info("Saving data to file %s", filename)
        with open(filename, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = header)
            writer.writeheader()
            writer.writerows(result)

    @print_elapsed_time
    def get_options_chain(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        if if_after_hours(self.timezone):
            logger.info("Market is closed, skipping")
            return

        logger.info("Attempting to get options")

        under = ib_insync.Index('SPX', 'CBOE')
        [under] = self.ibkr.qualifyContracts(under)
        self.ibkr.reqMarketDataType(3)
        [ticker] = self.ibkr.reqTickers(under)
        under_value = ticker.marketPrice()
        logger.debug('Underlying value: %s', under_value)

        chains = self.ibkr.reqSecDefOptParams(under.symbol, '', under.secType, under.conId)

        chain = next(c for c in chains if
            c.tradingClass == 'SPXW' and c.exchange == 'SMART')

        strikes = [strike for strike in chain.strikes
            if under_value*0.9 < strike < under_value*1.1]

        expirations = sorted(exp for exp in chain.expirations)[:3]
        logger.debug(expirations)

        rights = ['P', 'C']
        contracts = [ib_insync.Option(
                'SPX',
                expiration,
                strike,
                right,
                'SMART',
                tradingClass='SPXW')
            for right in rights
            for expiration in expirations
            for strike in strikes]

        contracts = self.ibkr.qualifyContracts(*contracts)
        logger.info('Found %s contracts', len(contracts))

        tickers = self.ibkr.reqTickers(*contracts)
        self._save_option_chain(tickers)

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
            'file': self._save_options_to_file,
        }
        func = switcher.get(self.config.backend, "None")
        func(tickers)


    def _save_options_to_file(self, data):
        """
        Save data to file
        """
        filename = os.path.join(
            self.config.storage_path,
            'options_' + self._formatted_now())
        data.to_csv(f'{filename}', index=False)
