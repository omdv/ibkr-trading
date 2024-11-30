"""
Generate mocked tickers
"""

from datetime import datetime as dt
from ib_async import Ticker, OptionComputation, Contract
from trader.trading_logic import next_trading_day
from .common import local_symbol, contract_id


def gen_tickers():
  """Generate mocked tickers"""
  tickers = [
    Ticker(
      contract=Contract(
        secType="IND",
        symbol="SPX",
      ),
      last=6200.0,
    ),
    Ticker(
      contract=Contract(
        secType="OPT",
        symbol="SPX",
        tradingClass="SPXW",
        lastTradeDateOrContractMonth=dt.now().strftime("%Y%m%d"),
        strike=6100.0,
        right="P",
      ),
      modelGreeks=OptionComputation(
        tickAttrib=1,
        impliedVol=0.5,
        delta=-0.001,
        optPrice=0.5,
        pvDividend=0.0,
        gamma=0.5,
        vega=0.5,
        theta=0.5,
        undPrice=100.0,
      ),
    ),
  ]

  expiry = next_trading_day()
  for strike in [
    5910,
    5900,
    5890,
    5880,
    5870,
    5860,
    5850,
    5840,
    5830,
    5820,
    5810,
    5800,
  ]:
    tickers.append(
      Ticker(
        contract=Contract(
          secType="OPT",
          symbol="SPX",
          lastTradeDateOrContractMonth=expiry,
          right="P",
          strike=strike,
          tradingClass="SPXW",
        ),
        modelGreeks=OptionComputation(
          tickAttrib=1,
          impliedVol=0.5,
          delta=-0.07 + 0.001 * strike,
          optPrice=0.5,
          pvDividend=0.0,
          gamma=0.5,
          vega=0.5,
          theta=0.5,
          undPrice=100.0,
        ),
        ask=round(strike * 0.01005, 2),
        bid=round(strike * 0.01001, 2),
        last=round(strike * 0.01003, 2),
      )
    )

  for ticker in tickers:
    ticker.contract.conId = contract_id(ticker.contract)
    ticker.contract.localSymbol = local_symbol(ticker.contract)

  return {ticker.contract.conId: ticker for ticker in tickers}
