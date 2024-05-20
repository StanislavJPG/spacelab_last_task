import asyncio
import logging
import random
from threading import Thread

import httpx

from clients.interfaces import AbstractAPIClient
import asyncio_redis

from redis import Redis

"""
I'm using asyncio_redis because of some errors of default redis package 
"""


class BinanceRedisClient(AbstractAPIClient):
    def __init__(self, currency: str, period: int) -> None:
        self.currency = currency
        self.period = period

    def save_to_db(self, i: int = None):
        with httpx.Client() as client:
            response = client.get(f'https://api.binance.com/api/v3/avgPrice?symbol={self.currency}')
            row = response.json()

        redis = Redis(host='localhost', port=6379, decode_responses=True)
        redis.set(f'ExchangeRate[{i}]', f'mins:{row["mins"]} price:{row["price"]} '
                        f'close_time:{row["closeTime"]}', 120)
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        logging.info(random.randrange(10))

        # connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
        # await connection.set(f'ExchangeRate[{i}]', f'mins:{row["mins"]} price:{row["price"]} '
        #                                            f'close_time:{row["closeTime"]}', 120)

    # async def start(self) -> None:
    #     for i in range(self.period):
    #         target = await self._save_to_db(i=i)
    #         t1 = Thread(target=target)
    #         t1.start()
    #         t1.join()
    #         logging.basicConfig(level=logging.INFO, format='%(message)s')
    #         logging.info(random.randrange(10))


# inst = BinanceRedisClient(
#     'BTCUSDT', 2)

# if __name__ == '__main__':
#     asyncio.run(inst.start())
