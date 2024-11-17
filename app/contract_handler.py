import logging

from ib_async import IB, Index
from ib_async.contract import Option, Contract, ComboLeg
from ib_async.util import df

from models import OptionSpreads
from calendar_handler import next_trading_day
from trade_logic import target_delta, target_protection
from trade_handler import get_contract_price

logger = logging.getLogger(__name__)


def get_short_leg_contract(ibkr: IB, expiry: str) -> Contract:
  """
  Get the short leg contract
  TODO: Model Greeks vs Last Greeks?
  """
  # Create a contract for SPX
  spx = Index("SPX", "CBOE")
  ibkr.qualifyContracts(spx)
  underlying_price = get_contract_price(ibkr, spx)
  logger.info("Underlying price: %s", underlying_price)

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

  logger.debug("Target short contract: %s", short_contract)
  return short_contract


def get_long_leg_contract(ibkr: IB, expiry: str, short_contract: Contract) -> Contract:
  """
  Get the long leg contract
  """
  # TODO: check that the strike exists in the chain

  short_strike = short_contract.strike
  long_strike = short_strike - target_protection()

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
  logger.debug("Target long contract: %s", long_contract)
  return long_contract


def get_spread_contract(
  ibkr: IB, expiry: str, short_contract: Contract, long_contract: Contract
) -> OptionSpreads:
  """
  Create the option spreads
  """
  # Create empty combo contract
  contract = Contract(
    symbol=short_contract.symbol,
    secType="BAG",
    currency="USD",
    exchange="SMART",
  )

  # Add legs to the contract
  legs = []
  for side, spread in [("short", short_contract), ("long", long_contract)]:
    cds = ibkr.reqContractDetails(spread)
    leg = ComboLeg()
    leg.conId = cds[0].contract.conId
    leg.ratio = 1
    leg.exchange = "SMART"
    leg.action = "BUY" if side == "long" else "SELL"
    legs.append(leg)

  contract.comboLegs = legs

  # Log contract details
  logger.debug("Target spread: %s", contract)

  return contract


def get_spread_to_open(ibkr: IB, spreads: list[OptionSpreads]) -> Contract:
  """
  Determine which spread to open
  """

  # if not need_to_open_spread(ibkr, spreads):
  #   return None

  expiry = next_trading_day()
  short_leg = get_short_leg_contract(ibkr, expiry)
  logger.debug("Short leg: %s", short_leg)
  long_leg = get_long_leg_contract(ibkr, expiry, short_leg)
  logger.debug("Long leg: %s", long_leg)
  contract = get_spread_contract(ibkr, expiry, short_leg, long_leg)

  return contract


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  ibkr = IB()
  ibkr.connect("localhost", 8888)
  contract = get_spread_to_open(ibkr, [])
  logger.info("Target spread: %s", contract)
  ibkr.disconnect()
