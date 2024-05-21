from datetime import datetime

from tortoise import Tortoise

import logging

from clients.db.models import ExchangeRate
from clients.interfaces import APIClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')


async def tortoise_init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['clients.db.models']}
    )
    await Tortoise.generate_schemas()


class BinanceDbClient(APIClient):

    def __init__(self, currency: str, period: int) -> None:
        super().__init__(currency, period)

    async def _save_to_db(self):
        await tortoise_init()
        try:
            for period in range(self.period):
                data = await super()._get_binance_exchange()
                await ExchangeRate.create(mins=data['mins'], price=data['price'],
                                          close_time=data['closeTime'])
                current_time = datetime.now()
                logging.info(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        except KeyError:
            logging.error(f'Is the currency {self.currency} valid?')

    def start(self):
        return super().start()
