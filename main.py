import asyncio
from threading import Thread

from clients.redis import BinanceRedisClient
from clients.sqldb import BinanceDbClient

inst = BinanceRedisClient(
    'BTCUSDT', 2)

inst2 = BinanceDbClient(
    'LTCUSDT', 3)


t1 = Thread(target=inst.save_to_db())
t1.start()
t1.join()

t2 = Thread(target=inst2.save_to_db())
t2.start()
t2.join()
