import datetime as dt
import logging
from ib_async import IB
from ib_async.contract import Option, Contract, ComboLeg
from exchange_calendars import get_calendar

logger = logging.getLogger(__name__)


def create_spread_contract(ibkr: IB):
  """
  Create the option spreads with dynamic expiration and strikes
  """
  nyse = get_calendar("XNYS")  # NYSE (New York Stock Exchange) calendar
  today = dt.datetime.now()

  # Get the next trading day's end
  next_session = nyse.next_session(today.strftime("%Y-%m-%d"))
  expiry = next_session.strftime("%Y%m%d")

  # TODO: Make this dynamic
  short_strike = 5900
  long_strike = short_strike - 100

  # Create long put first
  long = Option(
    symbol="SPX",
    lastTradeDateOrContractMonth=expiry,
    strike=long_strike,
    multiplier=100,
    right="P",
    exchange="SMART",
    currency="USD",
  )

  short = Option(
    symbol="SPX",
    lastTradeDateOrContractMonth=expiry,
    strike=short_strike,
    multiplier=100,
    right="P",
    exchange="SMART",
    currency="USD",
  )
  ibkr.qualifyContracts(short)
  ibkr.qualifyContracts(long)

  spreads = {"long": long, "short": short}

  # Create empty combo contract
  contract = Contract(
    symbol=long.symbol,
    secType="BAG",
    currency="USD",
    exchange="SMART",
  )

  # Add legs to the contract
  legs = []
  for side, spread in spreads.items():
    cds = ibkr.reqContractDetails(spread)
    leg = ComboLeg()
    leg.conId = cds[0].contract.conId
    leg.ratio = 1
    leg.exchange = "SMART"
    leg.action = "BUY" if side == "long" else "SELL"
    legs.append(leg)

  contract.comboLegs = legs

  # Log contract details
  logger.info("Contract details: %s", contract)

  return contract
