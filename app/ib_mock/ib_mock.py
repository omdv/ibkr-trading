from loguru import logger

from ib_async import IB
from ib_async.objects import AccountValue
from ib_async.contract import ContractDetails, Contract
from ib_async.order import Order

from .gen_positions import gen_positions
from .gen_tickers import gen_tickers
from .gen_option_chain import gen_option_chain
from .gen_trades import gen_trades
from .common import contract_id, local_symbol


class MockIB(IB):
  def __init__(self):
    super().__init__()

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
    logger.debug("Mocking qualifyContracts for contracts: {}", args)
    for arg in args:
      arg.conId = contract_id(arg)
      arg.localSymbol = local_symbol(arg)
    return args

  def reqContractDetails(self, *args, **kwargs):
    """Mock reqContractDetails - return mocked contract details"""
    logger.debug("Mocking reqContractDetails for contracts: {}", args)
    contract_details = []
    for arg in args:
      cd = ContractDetails(contract=arg)
      cd.contract.conId = contract_id(arg)
      cd.contract.localSymbol = local_symbol(arg)
      contract_details.append(cd)
    return contract_details

  def reqMarketDataType(self, *args, **kwargs):
    """Mock reqMarketDataType - always succeeds"""
    logger.debug("Mocking reqMarketDataType")
    return True

  def reqTickers(self, *args, **kwargs):
    """Mock reqTickers - return mocked ticker"""
    logger.debug("Mocking tickers for contracts: {}", args)
    mock_tickers = gen_tickers()
    result = []
    for arg in args:
      if arg.conId in mock_tickers:
        result.append(mock_tickers[arg.conId])
    return result

  def reqMktData(self, contract):
    """Mock reqMktData - always succeeds"""
    logger.debug("Mocking reqMktData for contract: {}", contract.conId)
    mock_tickers = gen_tickers()
    if contract.conId in mock_tickers:
      logger.debug("Mocking reqMktData for contract: {}", mock_tickers[contract.conId])
      return mock_tickers[contract.conId]
    else:
      return None

  def reqSecDefOptParams(self, *args, **kwargs):
    """Mock reqSecDefOptParams - return mocked option chain"""
    logger.debug("Mocking reqSecDefOptParams for contract: {}", args[0])
    return gen_option_chain()

  def cancelMktData(self, *args, **kwargs):
    """Mock cancelMktData - always succeeds"""
    logger.debug("Mocking cancelMktData for contract: {}", args[0].conId)
    return True

  def placeOrder(self, contract: Contract, order: Order):
    """Mock placeOrder - return mocked trade"""
    logger.debug("Mocking placeOrder for contract: {}, order: {}", contract, order)
    trade = gen_trades(contract, order)
    return trade

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
