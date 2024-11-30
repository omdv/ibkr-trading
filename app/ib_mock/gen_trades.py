"""
Generate mock trades
"""

from ib_async.contract import Contract
from ib_async.order import Order, Trade, OrderStatus


def gen_trades(contract: Contract, order: Order):
  """Generate mock trades"""
  trade = Trade(
    contract=contract,
    order=order,
    orderStatus=OrderStatus(
      status="Filled",
      avgFillPrice=round(order.lmtPrice, 2),
    ),
  )
  return trade
