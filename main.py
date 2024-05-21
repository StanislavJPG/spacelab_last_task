from clients.redis import BinanceRedisClient
from clients.sqldb import BinanceDbClient

if __name__ == "__main__":
    binance_btc_redis_client = BinanceRedisClient(
        currency='BTCUSDT', period=5
    )
    binance_ltc_db_client = BinanceDbClient(
        currency='LTCUSDT', period=6
    )

    thread1 = binance_btc_redis_client.start()
    thread2 = binance_ltc_db_client.start()

    thread1.join()
    thread2.join()
