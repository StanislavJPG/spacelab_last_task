import asyncio
import time
from datetime import datetime
from threading import Thread

from tortoise import Tortoise

import logging


from clients.db.models import ExchangeRate
from clients.interfaces import AbstractAPIClient


async def tortoise_init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['clients.db.models']}
    )
    await Tortoise.generate_schemas()


class BinanceDbClient(AbstractAPIClient):
    def __init__(self, currency: str, period: int) -> None:
        self.currency = currency
        self.period = period

    async def _save_to_db(self, i: int = None):
        await tortoise_init()
        for i in range(self.period):
            row = await self.get_binance_exchange(currency=self.currency)
            await ExchangeRate.create(mins=row['mins'], price=row['price'],
                                      close_time=row['closeTime'])

    def start(self) -> None:
        try:
            t1 = Thread(target=asyncio.run, args=(self._save_to_db(),))
            t1.start()
        finally:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            logging.info(current_time.strftime('%Y-%m-%d %H:%M:%S'))
            # asyncio.run(Tortoise.close_connections())
            time.sleep(1.5)
