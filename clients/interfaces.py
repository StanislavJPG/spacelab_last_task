import asyncio
from abc import ABC, abstractmethod

import httpx
from tortoise import Tortoise
from yarl import URL


class AbstractAPIClient(ABC):
    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def _save_to_db(self, i=None):
        ...

    @abstractmethod
    def start(self) -> None:
        ...

    @staticmethod
    async def get_binance_exchange(currency):
        async with httpx.AsyncClient() as client:
            url = URL('https://api.binance.com/api/v3/avgPrice').with_query(symbol=currency)
            response = await client.get(str(url))
            row = response.json()
        return row
