import logging
import pickle
from ib_async import IB
from ib_async.objects import AccountValue

from .gen_positions import gen_positions
from .gen_tickers import gen_tickers
from .gen_option_chain import gen_option_chain
from .common import contract_id

logger = logging.getLogger(__name__)


class MockIB(IB):
  def __init__(self, pickle_dir=None):
    super().__init__()
    self.pickle_dir = pickle_dir
    self._positions = []
    if pickle_dir:
      self._load_pickle_data()

  def _load_pickle_data(self):
    """Load mock data from pickle files"""
    try:
      with open(f"{self.pickle_dir}/positions.pickle", "rb") as f:
        self._positions = pickle.load(f)
      with open(f"{self.pickle_dir}/trades.pickle", "rb") as f:
        self._trades = pickle.load(f)
    except FileNotFoundError as e:
      print(f"Warning: Could not load pickle data: {e}")
    except Exception as e:
      print(f"Error loading pickle data: {e}")

  def connect(self, *args, **kwargs):
    """Mock connect - always succeeds"""
    logger.debug("Mocking connect")
    return True

  def positions(self):
    """Mock positions - return mock positions"""
    logger.debug("Mocking positions")
    return gen_positions()

  def qualifyContracts(self, *args, **kwargs):
    """Mock qualifyContracts"""
    logger.debug("Mocking qualifyContracts for contracts: %s", args)
    for arg in args:
      arg.conId = contract_id(arg)
    return args

  def reqMarketDataType(self, *args, **kwargs):
    """Mock reqMarketDataType - always succeeds"""
    logger.debug("Mocking reqMarketDataType")
    return True

  def reqTickers(self, *args, **kwargs):
    """Mock reqTickers - return mocked ticker"""
    logger.debug("Mocking tickers for contracts: %s", args)
    mock_tickers = gen_tickers()
    result = []
    for arg in args:
      if arg.conId in mock_tickers:
        result.append(mock_tickers[arg.conId])
    return result

  def reqMktData(self, contract):
    """Mock reqMktData - always succeeds"""
    logger.debug("Mocking reqMktData for contract: %s", contract.conId)
    mock_tickers = gen_tickers()
    if contract.conId in mock_tickers:
      logger.debug("Mocking reqMktData for contract: %s", mock_tickers[contract.conId])
      return mock_tickers[contract.conId]
    else:
      return None

  def reqSecDefOptParams(self, *args, **kwargs):
    """Mock reqSecDefOptParams - return mocked option chain"""
    logger.debug("Mocking reqSecDefOptParams for contract: %s", args[0])
    return gen_option_chain()

  def cancelMktData(self, *args, **kwargs):
    """Mock cancelMktData - always succeeds"""
    logger.debug("Mocking cancelMktData for contract: %s", args[0].conId)
    return True

  def placeOrder(self, *args, **kwargs):
    """Mock placeOrder - return pickled trade"""
    logger.debug("Mocking placeOrder for order: %s", args[0])
    return self._trades

  def accountValues(self, *args, **kwargs):
    """Mock accountValues - return mocked account values"""
    logger.debug("Mocking accountValues")
    account_values = [
      AccountValue(
        account="U123456",
        tag="NetLiquidationByCurrency",
        currency="BASE",
        value=100000.0,
        modelCode="",
      ),
    ]
    return account_values
