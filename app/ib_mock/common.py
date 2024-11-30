from ib_async.objects import Contract


def local_symbol(contract: Contract) -> str:
  if contract.secType == "OPT":
    return f"{contract.tradingClass}  {contract.lastTradeDateOrContractMonth}{contract.right}{contract.strike:07.0f}"
  else:
    return contract.symbol


def contract_id(contract: Contract) -> int:
  if contract.secType == "IND":
    return 100
  elif contract.secType == "OPT":
    return int(float(contract.lastTradeDateOrContractMonth) + contract.strike)
  else:
    return contract.conId
