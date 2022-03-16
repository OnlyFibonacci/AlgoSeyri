from binance import Client
import csv
import pandas as pd
from datetime import datetime as dt

client = Client(None, None)


periyotlar = {
    '1m': Client.KLINE_INTERVAL_1MINUTE,
    '3m': Client.KLINE_INTERVAL_3MINUTE,
    '5m': Client.KLINE_INTERVAL_5MINUTE,
    '15m': Client.KLINE_INTERVAL_15MINUTE,
    '30m': Client.KLINE_INTERVAL_30MINUTE,
    '1h': Client.KLINE_INTERVAL_1HOUR,
    '2h': Client.KLINE_INTERVAL_2HOUR,
    '4h': Client.KLINE_INTERVAL_4HOUR,
    '6h': Client.KLINE_INTERVAL_6HOUR,
    '8h': Client.KLINE_INTERVAL_8HOUR,
    '12h': Client.KLINE_INTERVAL_12HOUR,
    '1d': Client.KLINE_INTERVAL_1DAY,
    '3d': Client.KLINE_INTERVAL_3DAY,
    '1w': Client.KLINE_INTERVAL_1WEEK,
    '1M': Client.KLINE_INTERVAL_1MONTH
}


def verileriGetir(sembol, periyot, baslangic, bitis):
    mumlar = client.get_historical_klines(sembol, periyot, baslangic, bitis)
    return mumlar


def veriCekmeVeMatrikseUyarlama(semboller, periyot, baslangic, bitis):
    for coin in semboller:
        excelYap(csvOlustur(coin, verileriGetir(coin, periyot, baslangic, bitis)))
        print(coin, " Verileri Getirildi.")


def zamanHesapla(timestamp):
    return dt.fromtimestamp(timestamp / 1000)


def excelYap(okunacakCsv):
    basliklar = ['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat', 'tbbav', 'tbqav',
                 'ignore']
    df = pd.read_csv(okunacakCsv, names=basliklar)
    tarihler = pd.Series(map(lambda x: zamanHesapla(x).date(), df['open_time']))
    saatler = pd.Series(map(lambda x: zamanHesapla(x).time(), df['open_time']))
    total = pd.DataFrame(
        {'Tarih': tarihler, 'Saat': saatler, 'Acilis': df['open'], 'Yuksek': df['high'], 'Dusuk': df['low'],
         'Kapanis': df['close'], 'HacimLot': df['vol'], 'AOrt': 0})
    with pd.ExcelWriter(okunacakCsv + '.xlsx') as writer:
        total.to_excel(writer, sheet_name='Sayfa1', index=False)


def csvOlustur(sembol, mumlar):
    dosyaAdi = str(sembol + ".csv")
    csvDosya = open(dosyaAdi, 'w', newline='')
    yazici = csv.writer(csvDosya, delimiter=',')
    for mumVerileri in mumlar:
        yazici.writerow(mumVerileri)
    csvDosya.close()
    return dosyaAdi


def periyotGir():
    print('PERİYOTLAR')
    for i in periyotlar:
        print(i)
    print('########################')
    secim = input("Lütfen Periyot Seçin : ")
    return periyotlar.get(secim)


def zamanGir(d):
    print("Lütfen zaman değerini örnekteki gibi girin : ( 6 March 2017 )")
    if d == 0:
        secim = input("Başlangıç Zamanı Girin : ")
    elif d == 1:
        secim = input("Bitiş Zamanı Girin : ")
    else:
        secim = 0

    return secim


def sembolGir():
    koinlistesi = []
    print("Sizden koin adları girmenizi isteyeceğim.\nLütfen parite çiftlerini doğru yazın.\nİstediğiniz kadar " \
    "girebilirsiniz\nYeterli olduğunda hiç koin adı girmeden ENTER yapın. ")
    while True:
        secim = input("Koin Adı Girin :")
        if secim == '':
            break
        else:
            koinlistesi.append(secim)
    return koinlistesi


veriCekmeVeMatrikseUyarlama(sembolGir(), periyotGir(), zamanGir(0), zamanGir(1))
