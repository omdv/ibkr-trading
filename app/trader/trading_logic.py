import datetime as dt
from loguru import logger
from ib_async import IB, Index
from ib_async.contract import Option, Contract
from ib_async.util import df

from models import OptionSpread, OptionWithSize
from services.option_spread import OptionSpreadService
from services.contract import ContractService
from exchange_calendars import get_calendar


def next_trading_day() -> str:
  """
  Get the next trading day
  """
  nyse = get_calendar("XNYS")
  today = dt.datetime.now()

  # Get the next trading day after today (regardless of market status)
  next_trading_day = nyse.next_open(today.date() + dt.timedelta(days=1)).strftime(
    "%Y%m%d"
  )
  logger.debug("Next trading day: {}", next_trading_day)

  return next_trading_day


def need_to_open_spread(ibkr: IB, spreads: list[OptionSpread]):
  """
  Check trade logic
  TODO: add the logic here
  TODO: check for delta of the short leg
  TODO: check for symbols - we assume it is only SPXW
  """
  # When empty, we need to open a spread
  return_flag = True

  if len(spreads) == 2:
    return_flag = False
  if len(spreads) == 1:
    # Check if the existing spread expires today
    today = dt.datetime.now().strftime("%Y%m%d")
    if spreads[0].expiry == today:
      option_spread_service = OptionSpreadService(ibkr, spreads[0])
      current_delta = option_spread_service.get_spread_delta()
      logger.info("Current delta: {}", current_delta)

      if current_delta > -0.02:
        return_flag = True
      else:
        return_flag = False
    else:
      return_flag = False

  return return_flag


def target_delta() -> float:
  """
  Target delta
  TODO: add the logic here

  """
  return -0.05


def target_width() -> int:
  """
  Target width
  TODO: add the logic here
  """
  return 100


def position_size(ibkr: IB) -> int:
  """
  Position size
  TODO: add the logic here
  """

  # Get the net value
  net_value = float(
    [
      v
      for v in ibkr.accountValues()
      if v.tag == "NetLiquidationByCurrency" and v.currency == "BASE"
    ][0].value
  )

  # Calculate the position size
  kelly_factor = 0.25
  multiplier = 100

  position_size = round(net_value * kelly_factor / target_width() / multiplier)
  return int(position_size)


def _short_leg_contract_to_open(ibkr: IB, expiry: str) -> Contract:
  """
  Get the short leg contract
  TODO: Model Greeks vs Last Greeks?
  """
  # Create a contract for SPX
  spx = Index("SPX", "CBOE")
  ibkr.qualifyContracts(spx)

  # Get the current price of the underlying
  contract_service = ContractService(ibkr, spx)
  underlying_price = contract_service.get_current_price()

  # Request option chain
  chains = ibkr.reqSecDefOptParams(spx.symbol, "", spx.secType, spx.conId)
  chain = next(c for c in chains if c.tradingClass == "SPXW" and c.exchange == "SMART")

  # Filter out puts and get the right expiration
  strikes = [
    s
    for s in sorted(chain.strikes)
    if s < underlying_price and s > underlying_price * 0.93
  ]
  expirations = [e for e in chain.expirations if e == expiry]
  puts = [
    Option("SPX", expiration, strike, right, "SMART", tradingClass="SPXW")
    for right in ["P"]
    for expiration in expirations
    for strike in strikes
  ]
  puts = ibkr.qualifyContracts(*puts)

  # Get tickers with greeks
  tickers = ibkr.reqTickers(*puts)
  contracts = df([t.contract for t in tickers])

  try:
    model_greeks = df([t.modelGreeks for t in tickers])
    contracts = contracts.merge(model_greeks, left_index=True, right_index=True)
  except TypeError:
    logger.warning("No model greeks available")

  contracts = contracts[contracts["delta"] > target_delta()]
  strike = contracts.iloc[-1].strike
  short_contract = [e for e in puts if e.strike == strike][0]

  logger.debug("Target short contract: {}", short_contract)
  return short_contract


def _long_leg_contract_to_open(
  ibkr: IB, expiry: str, short_contract: Contract
) -> Contract:
  """
  Get the long leg contract
  """
  # TODO: check that the strike exists in the chain

  short_strike = short_contract.strike
  long_strike = short_strike - target_width()

  long_contract = Option(
    symbol="SPX",
    lastTradeDateOrContractMonth=expiry,
    strike=long_strike,
    multiplier=100,
    right="P",
    tradingClass="SPXW",
    exchange="SMART",
    currency="USD",
  )
  long_contract = ibkr.qualifyContracts(long_contract)[0]
  logger.debug("Target long contract: {}", long_contract)
  return long_contract


def get_spread_to_open(ibkr: IB, spreads: list[OptionSpread]) -> OptionSpread:
  """
  Determine which spread to open
  """

  expiry = next_trading_day()
  short_leg = _short_leg_contract_to_open(ibkr, expiry)
  logger.debug("Short leg: {}", short_leg)
  long_leg = _long_leg_contract_to_open(ibkr, expiry, short_leg)
  logger.debug("Long leg: {}", long_leg)

  # assign size to the legs
  legs = [
    OptionWithSize(position_size=-position_size(ibkr), option=short_leg),
    OptionWithSize(position_size=+position_size(ibkr), option=long_leg),
  ]
  logger.debug("Legs: {}", legs)

  spread = OptionSpread(legs=legs)
  return spread


if __name__ == "__main__":
  ibkr = IB()
  ibkr.connect("localhost", 8888)
  contract = get_spread_to_open(ibkr, [])
  logger.info("Target spread: {}", contract)
  ibkr.disconnect()
