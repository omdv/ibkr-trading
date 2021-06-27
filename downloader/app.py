import logging
import os
import ib_insync
import datetime as dt
import pytz
import time
import schedule
import json
from google.cloud import storage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
ib_insync.util.logToConsole(level=logging.INFO)

class NegativePrice(Exception):
    pass

class Bot():
    def __init__(self, config):
        self.config = config

        self.ptf = []
        self.options = []
        self.ptf_stats = {}
        self.pos_stats = {}

        self.tz = pytz.timezone('US/Eastern')
        self.tfmt = "%Y-%m-%dT%H:%M:%S%z"

    
    def __del__(self):
        try:
            self.ib.disconnect()
        except AttributeError:
            pass


    def serialize_ticker(self, ticker):
        attr_to_serialize = [
            'symbol'
            'localsymbol',
            'lastTradeDateOrContractMonth',
            'strike',
            'right',
            'ask',
            'askSize',
            'bid',
            'bidSize',
            'modelGreeks'
        ]
        dummy_dict = {}
        for attr in attr_to_serialize:
            dummy_dict[attr] = ticker[attr]

        return dummy_dict 


    def connect_to_gateway(self):
        """
        Create and connect IB client
        """
        host = self.config['IB_GATEWAY_HOST']
        port = self.config['IB_GATEWAY_PORT']

        self.ib = ib_insync.IB()
        self.ib.connect(
            host = host,
            port = port,
            clientId = self.config['CLIENT_ID'],
            timeout = 15,
            readonly = True)
        logger.debug("Connected to IB on {}:{}.".format(host,port))
        self.ib.reqMarketDataType(self.config['MKT_DATA_TYPE'])

    
    def get_option_chain(self):
        """
        Handle interactions with API and raise related exceptions here
        """
        self.connect_to_gateway()

        under = ib_insync.Index(self.config['SYMBOL'], 'CBOE')
        [under] = self.ib.qualifyContracts(under)
        self.ib.reqMarketDataType(2)
        [ticker] = self.ib.reqTickers(under)
        underValue = ticker.marketPrice()
        logger.info("Underlying value: {}".format(underValue))

        chains = self.ib.reqSecDefOptParams(under.symbol, '', under.secType, under.conId)
        chain = next(c for c in chains if
            c.tradingClass == self.config['TRADING_CLASS'] and c.exchange == 'SMART')

        strikes = [strike for strike in chain.strikes
            if underValue*0.9 < strike < underValue*1.1]

        expirations = sorted(exp for exp in chain.expirations)[:3]
        logger.debug(expirations)

        rights = ['P', 'C']
        contracts = [ib_insync.Option(
                self.config['SYMBOL'],
                expiration,
                strike,
                right,
                'SMART',
                tradingClass=self.config['TRADING_CLASS'])
            for right in rights
            for expiration in expirations
            for strike in strikes]

        contracts = self.ib.qualifyContracts(*contracts)
        logger.info('Found {} contracts'.format(len(contracts)))

        tickers = self.ib.reqTickers(*contracts)
        self.save_option_chain(tickers)

        self.ib.disconnect()
    
    def save_option_chain(self, tickers):
        """
        Aux function to serialize and save the chain
        """
        tickers = ib_insync.util.df(tickers)


        contract_attr = [
            'symbol',
            'localSymbol',
            'right',
            'strike',
            'lastTradeDateOrContractMonth'
        ]
        for a in contract_attr:
            tickers[a] = tickers['contract'].apply(lambda x: getattr(x, a))


        greeks_attr = [
            'impliedVol',
            'delta',
            'optPrice',
            'gamma',
            'vega',
            'theta',
            'undPrice']
        for a in greeks_attr:
            tickers[a] = tickers['modelGreeks'].apply(lambda x: getattr(x, a))

        current_time = tickers.iloc[-1]['time']

        tickers = tickers[contract_attr+greeks_attr]

        filename = current_time.strftime("%Y%m%d%H%M")

        if self.config['STORAGE_BACKEND'] == 'gcs':
            client = storage.Client()
            bucket = client.get_bucket(self.config['GCS_BUCKET_NAME'])
            bucket.blob('options/{}.csv'.format(filename)).upload_from_string(
                tickers.to_csv(index=False),
                'text/csv')
        else:
            tickers.to_csv('/tmp/{}'.format(filename), index=False)

    
    def run(self):
        """
        Run loop
        """
        schedule.every().hour.at(":00").do(self.get_option_chain)
        schedule.every().hour.at(":30").do(self.get_option_chain)

        logger.debug("Started bot")
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    config = {
        'TRADING_MODE': os.getenv('TRADING_MODE', 'paper'),
        'IB_GATEWAY_HOST': os.getenv('IB_GATEWAY_HOST', '127.0.0.1'),
        'IB_GATEWAY_PORT': os.getenv('IB_GATEWAY_PORT', 4001),
        'CLIENT_ID': os.getenv('CLIENT_ID', 1010),
        'MKT_DATA_TYPE': os.getenv('MKT_DATA_TYPE', 4),
        'SYMBOL': os.getenv('SYMBOL', 'SPX'),
        'TRADING_CLASS': os.getenv('TRADING_CLASS', 'SPXW'),
        'STORAGE_BACKEND': os.getenv('STORAGE_BACKEND', 'local'),
        'GCS_BUCKET_NAME': os.getenv('GCS_BUCKET_NAME'),
        'DELAY': 120
    }

    bot = Bot(config)
    bot.run()
