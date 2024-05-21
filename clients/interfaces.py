import asyncio
import time
from abc import ABC, abstractmethod
from threading import Thread

import httpx
from yarl import URL


class APIClient(ABC):
    def __init__(self, currency: str, period: int) -> None:
        self.currency = currency
        self.period = period

    @abstractmethod
    def _save_to_db(self):
        # logic of saving data to the NoSQL, SQL databases
        ...

    def start(self):
        # creation threads method
        t1 = Thread(target=asyncio.run, args=(self._save_to_db(),))
        t1.start()
        time.sleep(1.5)
        return t1

    async def _get_binance_exchange(self):
        # main method of getting binance exchanges from API
        async with httpx.AsyncClient() as client:
            url = URL('https://api.binance.com/api/v3/avgPrice').with_query(symbol=self.currency)
            response = await client.get(str(url))
        return response.json()
