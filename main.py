from clients.redis import BinanceRedisClient
from clients.sqldb import BinanceDbClient

if __name__ == "__main__":
    inst = BinanceRedisClient(
        'BTCUSDT', 5)
    inst2 = BinanceDbClient(
        'LTCUSDT', 6)

    inst.start()
    inst2.start()
