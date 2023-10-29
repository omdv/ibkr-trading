"""
Utility functions.
"""

import functools
import time
import logging
import sys
import datetime as dt
import holidays

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
    level=logging.INFO)
logger = logging.getLogger('databot')


def print_elapsed_time(func):
    """
    Wrapper to bring elapsed time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        logger.info('Running job %s', func.__name__)
        result = func(*args, **kwargs)
        logger.info('Job %s completed in %ss', func.__name__, time.time() - start_timestamp)
        return result

    return wrapper


def if_after_hours(timezone, now = None):
    """
    Check if market is open, got it from /u/numbuh-0
    """
    if not now:
        now = dt.datetime.now(timezone)

    # add 1hr before and after market close
    open_time = dt.time(hour = 8, minute = 30, second = 0)
    close_time = dt.time(hour = 17, minute = 0, second = 0)

    us_holidays = holidays.US()
    if now.strftime('%Y-%m-%d') in us_holidays:
        return True
    if (now.time() < open_time) or (now.time() > close_time):
        return True
    if now.date().weekday() > 4:
        return True
    return False
