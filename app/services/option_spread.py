"""
Option spread related services
"""

import logging

from ib_async import Contract, IB, ComboLeg, Order

from models import OptionSpread
from services.contract import ContractService

logger = logging.getLogger(__name__)


class OptionSpreadService:
  def __init__(self, ibkr: IB, option_spread: OptionSpread):
    self.ibkr = ibkr
    self.spread = option_spread

  def get_short_leg_contract(self) -> Contract:
    """
    Get the short leg contract
    """
    for leg in self.spread.legs:
      if leg.position_size < 0:
        short_contract_id = leg.conId
        break
    logger.info("Short contract ID: %s", short_contract_id)
    contract = Contract(conId=short_contract_id, exchange="SMART")
    self.ibkr.qualifyContracts(contract)
    return contract

  def get_long_leg_contract(self) -> Contract:
    """
    Get the long leg contract
    """
    for leg in self.spread.legs:
      if leg.position_size > 0:
        long_contract_id = leg.conId
        break

    contract = Contract(conId=long_contract_id, exchange="SMART")
    self.ibkr.qualifyContracts(contract)
    return contract

  def create_spread_contract(self) -> Contract:
    """
    Create the spread contract from the OptionSpreads object
    """
    short_contract = self.get_short_leg_contract()
    long_contract = self.get_long_leg_contract()

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
      cds = self.ibkr.reqContractDetails(spread)
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

  def get_current_price(self) -> float:
    """
    Get the current price of the spread
    """
    short_contract = self.get_short_leg_contract()
    short_contract_service = ContractService(self.ibkr, short_contract)
    short_price = short_contract_service.get_current_price("bid")

    long_contract = self.get_long_leg_contract()
    long_contract_service = ContractService(self.ibkr, long_contract)
    long_price = long_contract_service.get_current_price("ask")

    price = long_price - short_price

    return price

  def get_spread_delta(self) -> float:
    """
    Get the delta for the spread
    TODO: modelGreeks vs lastGreeks
    """
    short_contract = self.get_short_leg_contract()
    self.ibkr.reqMktData(short_contract)
    ticker = self.ibkr.reqTickers(short_contract)
    self.ibkr.cancelMktData(short_contract)
    return ticker[0].modelGreeks.delta

  def trade_spread(self) -> None:
    """
    Trade the spread with price adjustment logic if the order doesn't fill
    """
    spread_contract = self.create_spread_contract()
    current_price = self.get_current_price()
    max_attempts = 3
    price_increment = 0.05

    order = Order()
    order.action = "BUY"
    order.totalQuantity = self.spread.size
    order.orderType = "LMT"
    order.lmtPrice = current_price

    logger.info(
      "Placing order for spread: %s x %s at %s",
      spread_contract,
      self.spread.size,
      current_price,
    )
    trade = self.ibkr.placeOrder(spread_contract, order)

    # Wait for order to fill
    for attempt in range(max_attempts):
      filled = False
      timeout = 30  # seconds to wait for fill

      while timeout > 0 and not filled:
        if trade.orderStatus.status == "Filled":
          logger.info("Order filled at %s", trade.orderStatus.avgFillPrice)
          filled = True
          break

        self.ibkr.sleep(1)
        timeout -= 1

      if filled:
        import pickle
        from datetime import datetime

        with open(
          f'./data/trade-{datetime.now().strftime("%Y%m%d-%H%M%S")}.pkl', "wb"
        ) as f:
          pickle.dump(trade, f)
        break

      # If not filled, adjust price upward
      new_price = order.lmtPrice + price_increment
      logger.info(
        "Order not filled after %d seconds. Adjusting price to %s", 30, new_price
      )

      # Cancel existing order
      self.ibkr.cancelOrder(trade.order)

      # Place new order with adjusted price
      order.lmtPrice = new_price
      trade = self.ibkr.placeOrder(spread_contract, order)

    if not filled:
      logger.warning("Failed to execute spread trade after %d attempts", max_attempts)
      self.ibkr.cancelOrder(trade.order)
