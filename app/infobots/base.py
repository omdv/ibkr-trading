"""
InfoBot - downloading data from IBKR on schedule
"""
import time
import datetime as dt

import pytz
import ib_insync

from .utils import logger


class ConnectionIssue(Exception):
    """ My custom exception class. """


class InfoBot():
    """Class representing a trading bot."""
    def __init__(self, config):
        self.config = config
        self.ibkr = None
        self.timezone = pytz.timezone(self.config['settings']['timezone'])

    def __del__(self):
        try:
            self.ibkr.disconnect()
        except AttributeError:
            pass

    def _formatted_now(self):
        """
        Return now() formatted as specified in config.
        """
        return dt.datetime.now(self.timezone).\
                strftime(self.config['settings']['timeformat'])

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
            logger.error(e)

        logger.debug('Connected to IB on %s:%s', host, port)

    def test_connection(self):
        """
        Test connection to IB
        """
        try:
            self._connect_to_gateway()
            time.sleep(10)
            self.ibkr.disconnect()
        except ConnectionIssue as e:
            logger.error(e)
            return False
        return True
