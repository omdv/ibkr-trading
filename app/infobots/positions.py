"""
Bot class.
"""

import os
import csv

from .base import InfoBot
from .utils import logger
from .utils import print_elapsed_time


class PositionsBot(InfoBot):
    """
    Downloading positions
    """

    @print_elapsed_time
    def _get_fills(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        logger.info("Attempting to get fills for current session")

        self._connect_to_gateway()
        logger.info("Connected to IB")

        fills = self.ibkr.fills()
        self._save_fills(fills)

        self.ibkr.disconnect()
        logger.info("Disconnected from IB")


    def _save_fills(self, fills):
        """
        Aux function to serialize and save the fills
        """
        result = []
        for fill in fills:
            combined = fill.contract.dict() | fill.execution.dict()
            header = combined.keys()
            result.append(combined)

        filename = os.path.join(
            self.config['persistence']['mount_path'],
            self._formatted_now())

        with open(filename, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = header)
            writer.writeheader()
            writer.writerows(result)


    def run(self):
        """
        Main function for the loop
        """

        self._get_fills()
