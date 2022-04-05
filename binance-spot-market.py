from parameters import *
from binance.spot import Spot as Client
spot_client = Client(key, secret)

# Sembol için geçerli olan ortalama fiyat
def avg_price(coinName: str):
    coin_avg = spot_client.avg_price(symbol=str(coinName))
    return coin_avg['price']


# borsa Verileri
def exchangeInfo(coinName: str):
    exc = spot_client.exchange_info(symbol=str(coinName))
    return exc


# mum verileri
def spot_klinesCoin(coinName: str, period: str, limit: int = None):
    kline = spot_client.klines(symbol=str(coinName), interval=str(period), limit=limit)
    return kline


# 24 saatlik değişimin verisi
def ticker24h(coinName: str):
    hticker24 = spot_client.ticker_24hr(symbol=str(coinName))
    return hticker24


# fiyat
def price(coinName: str):
    return spot_client.ticker_price(symbol=str(coinName))['price']


# timestamp
def serverTime():
    return spot_client.time()['serverTime']


# emir defteri
def book(coinName: str, limit: int):
    return spot_client.depth(symbol=coinName, limit=limit)


# tüm spot verileri
def spot_all_symbols():
    response = spot_client.exchange_info()
    return list(map(lambda symbol: symbol['symbol'], response['symbols']))


#spottaki tüm koinleri sınıflandırma
usdtList = []
btcList = []
ethList = []
for coin in spot_all_symbols():
    if 'USDT' in coin and 'UP' not in coin and 'DOWN' not in coin:
        usdtList.append(coin)
    elif 'BTC' in coin:
        btcList.append(coin)
    elif 'ETH' in coin:
        ethList.append(coin)


# içerisine aktarılan kline veriyi sınıflandırma, dataframe'e dönüştürme        
def spot_symbols_data(coinName: str, period: str, limit: int):
    kline = spot_klinesCoin(coinName=coinName, period=period, limit=limit)
    converted = pd.DataFrame(kline, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                             'quote_asset_volume', 'number_of_trades', 'tbbav', 'tbqav', 'ignore'],
                             dtype=float)
    return converted
