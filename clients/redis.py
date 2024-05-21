import logging
import random

from clients.interfaces import APIClient
import asyncio_redis

"""
I'm using asyncio_redis because of some errors of default redis package 
"""

logging.basicConfig(level=logging.INFO, format='%(message)s')


async def init_async_redis() -> asyncio_redis:
    # create connection to the redis
    connection = await asyncio_redis.Connection.create(host='localhost', port=6379)
    return connection


class BinanceRedisClient(APIClient):
    def __init__(self, currency: str, period: int) -> None:
        super().__init__(currency, period)

    async def _save_to_db(self):
        try:
            for period in range(self.period):
                data = await super()._get_binance_exchange()
                connection = await init_async_redis()
                await connection.set(f'ExchangeRate[{period}]', f'mins:{data["mins"]} price:{data["price"]} '
                                                                f'close_time:{data["closeTime"]}', 120)
                logging.info(random.randrange(10))
        except KeyError:
            logging.error(f'Is the currency {self.currency} valid?')

    def start(self):
        return super().start()
