"""
expose the setup_logging function to the package level
"""
from .logging_config import setup_logging
from .utils import if_market_open

__all__ = [
  'setup_logging',
  'if_market_open'
]
