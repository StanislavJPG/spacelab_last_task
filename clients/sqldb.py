import asyncio
from datetime import datetime
from threading import Thread

import httpx
from tortoise import Tortoise

import logging

from clients.db.models import ExchangeRate
from clients.interfaces import AbstractAPIClient


class BinanceDbClient(AbstractAPIClient):
    def __init__(self, currency: str, period: int) -> None:
        self.currency = currency
        self.period = period

    def save_to_db(self, i: int = None):
        Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': ['clients.db.models']}
        )
        Tortoise.generate_schemas()

        with httpx.Client() as client:
            response = client.get(f'https://api.binance.com/api/v3/avgPrice?symbol={self.currency}')
            row = response.json()
            ExchangeRate.create(mins=row['mins'], price=row['price'],
                                close_time=row['closeTime'])
        logging.basicConfig(level=logging.INFO, format='%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()
        logging.info(current_time.strftime('%Y-%m-%d %H:%M:%S'))

    # async def start(self) -> None:
    #     for i in range(self.period):
    #         target = await self._save_to_db()
    #         t1 = Thread(target=target)
    #         t1.start()
    #         t1.join()
    #
    #         logging.basicConfig(level=logging.INFO, format='%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
    #         current_time = datetime.now()
    #         logging.info(current_time.strftime('%Y-%m-%d %H:%M:%S'))
    #         await asyncio.sleep(1.5)


# inst = BinanceDbClient(
#     'BTCUSDT', 2)
#
# if __name__ == '__main__':
#     asyncio.run(inst.start())
