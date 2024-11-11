import logging
from datetime import date

from .models import OptionSpreads

logger = logging.getLogger(__name__)


def need_to_open_spread(spreads: list[OptionSpreads]):
  """
  Check trade logic
  """
  # When empty, we need to open a spread
  return_flag = True

  if len(spreads) == 2:
    return_flag = False
  if len(spreads) == 1:
    # Check if the existing spread expires today
    today = date.today().strftime("%Y%m%d")
    if spreads[0].expiry == today:
      return_flag = True
    else:
      return_flag = False

  return return_flag


def target_delta() -> float:
  """
  Target delta
  """
  return -0.06


def target_protection() -> float:
  """
  Target protection
  """
  return 100
