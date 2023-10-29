# pylint: disable=redefined-outer-name, unused-argument
"""
FastAPI server for gateway
"""

import datetime as dt

from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings

from fastapi import FastAPI
import ib_insync
import nest_asyncio

class Settings(BaseSettings):
    """
    Read server settings
    """
    ib_gateway_host: str
    ib_gateway_port: str
    timezone: str = "US/Eastern"
    timeformat: str = "%Y-%m-%dT%H%M"

# from pydantic import BaseModel
# from .gateway import IBConnection

nest_asyncio.apply()
ibkr = ib_insync.IB()
settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Connect to gateway
    """
    ibkr.connect(
                host = settings.ib_gateway_host,
                port = settings.ib_gateway_port,
                clientId = dt.datetime.utcnow().strftime('%H%M%S'),
                timeout = 15,
                readonly = True)
    yield
    ibkr.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    """
    Root path
    """
    return {"Hello": "YES"}

@app.get("/stats")
def stats():
    """
    Perform test of the connection
    """
    results = ibkr.client.connectionStats()
    return results

@app.get("/positions")
def positions():
    """
    Get positions
    """
    results = ib_insync.util.df(ibkr.positions()).transpose()
    return results

@app.get("/portfolio")
def portfolio():
    """
    Get portfolio
    """
    results = ib_insync.util.df(ibkr.portfolio()).transpose()
    return results
