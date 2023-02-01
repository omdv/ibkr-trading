"""
Bot class.
"""

import ib_insync

from .base import InfoBot
from .utils import logger
from .utils import if_after_hours, print_elapsed_time

class OptionsBot(InfoBot):
    """
    Downloading options quotes
    """

    def _set_market_data_type(self):
        """
        Set market data type for the download process
        """
        logger.info('Setting market data type')
        self.ibkr.reqMarketDataType(
            self.config['download']['mkt_data_type'])

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
            'gcs': self._save_data_to_gcs,
            'file': self._save_data_to_file,
            'sqlite': self._save_data_to_sqlite
        }

        func = switcher.get(self.config['persistence']['backend'], "None")
        func(self.config, tickers)


    @print_elapsed_time
    def _get_option_chain(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        if if_after_hours(self.config['settings']['timezone']):
            logger.info("Market is closed, skipping")
            return

        logger.info("Attempting to get options")

        self._connect_to_gateway()
        logger.info("Connected to IB")

        under = ib_insync.Index(self.config['download']['symbol'], 'CBOE')
        [under] = self.ibkr.qualifyContracts(under)
        self.ibkr.reqMarketDataType(2)
        [ticker] = self.ibkr.reqTickers(under)
        under_value = ticker.marketPrice()
        logger.debug('Underlying value: %s', under_value)

        chains = self.ibkr.reqSecDefOptParams(under.symbol, '', under.secType, under.conId)

        chain = next(c for c in chains if
            c.tradingClass == self.config['download']['trading_class'] and c.exchange == 'SMART')

        strikes = [strike for strike in chain.strikes
            if under_value*0.9 < strike < under_value*1.1]

        expirations = sorted(exp for exp in chain.expirations)[:3]
        logger.debug(expirations)

        rights = ['P', 'C']
        contracts = [ib_insync.Option(
                self.config['download']['symbol'],
                expiration,
                strike,
                right,
                'SMART',
                tradingClass=self.config['download']['trading_class'])
            for right in rights
            for expiration in expirations
            for strike in strikes]

        contracts = self.ibkr.qualifyContracts(*contracts)
        logger.info('Found %s contracts', len(contracts))

        tickers = self.ibkr.reqTickers(*contracts)
        self._save_option_chain(tickers)

        self.ibkr.disconnect()
        logger.info("Disconnected from IB")


    def run(self):
        """
        Main function for the loop
        """
        self._get_option_chain()
