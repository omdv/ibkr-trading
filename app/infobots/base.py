"""
InfoBot - downloading data from IBKR on schedule
"""
import time
import os
import datetime as dt
import sqlite3

import pytz
import ib_insync

from google.cloud import storage
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

    def _save_data_to_gcs(self, data):
        """
        Save data to google cloud storage
        """
        client = storage.Client()

        filename = self._formatted_now()
        bucket = client.get_bucket(self.config['persist']['gcs_bucket_name'])
        bucket.blob(f'{filename}.csv').upload_from_string(
            data.to_csv(index=False), 'text/csv')


    def _save_data_to_file(self, data):
        """
        Save data to file
        """
        filename = os.path.join(
            self.config['persist']['mount_path'],
            self._formatted_now())
        data.to_csv(f'{filename}', index=False)


    def _save_data_to_sqlite(self, data):
        """
        Save data to sqlite db
        """
        filename = os.path.join(
            self.config['persist']['mount_path'],
            self.config['persist']['sqlite_filename'])
        con = sqlite3.connect(filename)
        data['quote_time'] = self._formatted_now()
        data.to_sql(name='spx', con=con, if_exists='append', index=False)
        con.close()
