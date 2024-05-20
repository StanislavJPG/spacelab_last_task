import asyncio
import logging
import random
import time
from threading import Thread

from clients.interfaces import AbstractAPIClient
import asyncio_redis

"""
I'm using asyncio_redis because of some errors of default redis package 
"""


class BinanceRedisClient(AbstractAPIClient):
    def __init__(self, currency: str, period: int) -> None:
        self.currency = currency
        self.period = period

    async def _save_to_db(self, i: int = None):
        for i in range(self.period):
            row = await self.get_binance_exchange(currency=self.currency)
            connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
            await connection.set(f'ExchangeRate[{i}]', f'mins:{row["mins"]} price:{row["price"]} '
                                                       f'close_time:{row["closeTime"]}', 120)

    def start(self) -> None:
        try:
            t1 = Thread(target=asyncio.run, args=(self._save_to_db(),))
            t1.start()
        finally:
            logging.basicConfig(level=logging.INFO, format='%(message)s')
            logging.info(random.randrange(10))
            time.sleep(1.5)
