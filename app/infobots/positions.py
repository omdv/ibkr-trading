"""
Bot class.
"""

from .base import InfoBot
from .utils import logger
from .utils import print_elapsed_time


class PositionsBot(InfoBot):
    """
    Downloading positions
    """

    @print_elapsed_time
    def _get_positions(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        # if if_after_hours(self.config['settings']['timezone']):
        #     logger.info("Market is closed, skipping")
        #     return

        logger.info("Attempting to get positions")

        self._connect_to_gateway()
        logger.info("Connected to IB")

        positions = self.ibkr.positions()
        logger.info("Positions:")
        logger.info(positions)

        self.ibkr.disconnect()
        logger.info("Disconnected from IB")


    def _save_positions(self, tickers):
        """
        Aux function to serialize and save the positions
        """


    def run(self):
        """
        Main function for the loop
        """

        self._get_positions()
