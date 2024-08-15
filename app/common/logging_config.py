"""
Helper to create logging configuration.
"""
import logging

def setup_logging():
  """
  main helper
  """
  logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
      'standard': {
          'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
          'datefmt': '%Y-%m-%d %H:%M:%S',
      },
    },
    'handlers': {
      'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'standard',
        'level': 'DEBUG',
      },
      'file': {
        'class': 'logging.FileHandler',
        'filename': 'app.log',
        'formatter': 'standard',
        'level': 'INFO',
      },
    },
    'loggers': {
      '': {  # root logger
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
        'propagate': True,
      },
    }
  }
  logging.config.dictConfig(logging_config)
