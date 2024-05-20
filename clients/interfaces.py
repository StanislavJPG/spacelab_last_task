from abc import ABC, abstractmethod


class AbstractAPIClient(ABC):
    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def save_to_db(self, i=None):
        ...

    # @abstractmethod
    # async def start(self) -> None:
    #     ...

# https://api.binance.com/api/v3/avgPrice?symbol=
