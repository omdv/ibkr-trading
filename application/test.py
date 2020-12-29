import logging
import os
import ib_insync
import random

log_level = 10
logging.basicConfig()
logging.getLogger().setLevel(log_level)

ib_insync.util.logToConsole(level=log_level)

def connect_to_ib():
    # Connect to market gateway
    ibinstance = ib_insync.IB()
    trading_mode = os.getenv('TRADING_MODE', 'paper')
    ib_port = 4042 if trading_mode == 'paper' else 4041

    ibinstance.connect(host=os.getenv('IB_GATEWAY_HOST', 'ib-gateway'),
                       port=ib_port,
                       clientId=int(os.getenv('EFP_CLIENT_ID', (5+random.randint(0, 4)))),
                       timeout=15,
                       readonly=True)
    logging.info("Connected to IB in {} mode.".format(trading_mode))

    ibinstance.reqMarketDataType(int(os.getenv('MKT_DATA_TYPE', '4')))
    return ibinstance

def main():
    ib_insync.util.sleep(30)
    ib_conn = connect_to_ib()
    ptf = ib_conn.portfolio()
    
    assert type(ptf), list
    logging.info("Passed connection test.")
    
    ib_conn.disconnect()

if __name__ == '__main__':
    main()