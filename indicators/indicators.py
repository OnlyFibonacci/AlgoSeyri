import math

import pandas as pd
import pandas_ta as ta
from function import *


def alphaTrend(high, low, close, volume, coeff, ap):
    coeff = 1
    ap = 14
    tr = ta.true_range(high, low, close)
    atr = ta.sma(tr, ap)
    noVolumeData = False
    coeff = 1
    upt = []
    downT = []
    AlphaTrend = [0.0]
    src = close
    rsi = ta.rsi(src, 14)
    hlc3 = []
    k1 = []
    k2 = []
    mfi = ta.mfi(high, low, close, volume, 14)
    for i in range(len(close)):
        hlc3.append((high[i] + low[i] + close[i]) / 3)

    for i in range(len(low)):
        if pd.isna(atr[i]):
            upt.append(0)
        else:
            upt.append(low[i] - (atr[i] * coeff))
    for i in range(len(high)):
        if pd.isna(atr[i]):
            downT.append(0)
        else:
            downT.append(high[i] + (atr[i] * coeff))
    for i in range(1, len(close)):
        if noVolumeData is True and rsi[i] >= 50:
            if upt[i] < AlphaTrend[i - 1]:
                AlphaTrend.append(AlphaTrend[i - 1])
            else:
                AlphaTrend.append(upt[i])

        elif noVolumeData is False and mfi[i] >= 50:
            if upt[i] < AlphaTrend[i - 1]:
                AlphaTrend.append(AlphaTrend[i - 1])
            else:
                AlphaTrend.append(upt[i])
        else:
            if downT[i] > AlphaTrend[i - 1]:
                AlphaTrend.append(AlphaTrend[i - 1])
            else:
                AlphaTrend.append(downT[i])

    for i in range(len(AlphaTrend)):
        if i < 2:
            k2.append(0)
            k1.append(AlphaTrend[i])
        else:
            k2.append(AlphaTrend[i - 2])
            k1.append(AlphaTrend[i])

    print(AlphaTrend)
    print(len(AlphaTrend))

    at = pd.DataFrame(data=k1, columns=['k1'])
    at['k2'] = k2
    return at
    #########




def elis(high,low,close,period=50,mult=2,gear=2):
    if gear>5 or gear<1 :
        gear=2
    src = close
    basis = ta.sma(src, period).fillna(value=1)
    dev = []
    upper = []
    lower = []
    stdev = ta.stdev(src, period).fillna(value=1)
    atr = ta.atr(high, low, close, period).fillna(value=1)

    # DEV HESAPLAMA
    for i in range(len(src)):
        dev.append(mult * stdev[i])

    # UPPER HESAPLAMA
    for i in range(len(src)):
        upper.append(basis[i] + dev[i])

    # LOWER HESAPLAMA
    for i in range(len(src)):
        lower.append(basis[i] - dev[i])

    # nATR HESAPLAMA
    nATR = []
    for i in range(len(atr)):
        nATR.append(atr[i] / src[i])

    # nSD HESAPLAMA
    nSD = []
    for i in range(len(stdev)):
        nSD.append(stdev[i] / src[i])

    # hATR - lATR HESAPLAMA
    hATR = []
    nATRn = []
    lATR = []
    nSDn = []
    hSD = []
    lSD = []
    for i in range(len(nATR)):
        nATRn.append(nATR[i])
        hATR.append(highest(nATRn, period))
        lATR.append(lowest(nATRn, period))
        ######
        nSDn.append(nSD[i])
        hSD.append(highest(nSDn, period))
        lSD.append(lowest(nSDn, period))

    ma = ta.wma(pd.Series(nATR), period)


    # PERM HESAPLAMALAR
    perm = []
    pers = []
    pera = []
    perb = []
    per = []

    for i in range(len(src)):
        persPayda = (hSD[i] - lSD[i])
        peraPayda = (hATR[i] - lATR[i])
        if persPayda==0:
            persPayda=1
        if peraPayda==0:
            peraPayda=1
        perm.append(100 * abs(nATR[i] - ma[i]) / ma[i])
        pers.append(100 * (nSD[i] - lSD[i]) / persPayda)
        pera.append(100 * (nATR[i] - lATR[i]) / peraPayda)
        perb.append(100 * (src[i] - lower[i]) / (upper[i] - lower[i]))
        if gear == 4 or gear == 5:
            per.append((perm[i] + pers[i] + pera[i] + perb[i]) / 4)
        elif gear == 1:
            per.append(min(100, (pers[i] + pera[i] + perb[i]) / 2.5))
        else:
            per.append((pers[i] + pera[i] + perb[i]) / 3)

    # ELiS HESAPLAMA
    EL = []
    for i in range(len(per)):
        EL.append((100 - per[i]) / (6 - gear))

    ELiS = []
    for i in range(len(EL)):
        if pd.isna(EL[i]):
            ELiS.append(1)
        else:
            ELiS.append(max(1,int(EL[i] + 0.5)))

    return ELiS


def fibonacci(high, low, ratio=618, lookBack=233):
    peek = highest(high, lookBack)
    deep = lowest(low, lookBack)

    def fibCalculate(value):
        if value == 0.5 or value == 50:
            value = 500
        if distance(high, peek) < distance(low, deep):
            return peek - ((peek - deep) * value / 1000)
        else:
            return deep + ((peek - deep) * value / 1000)

    return fibCalculate(ratio)



def ott(data, lentgh=2, percent=1.4, mav='VAR'):
    """Availaeble MA's:
    dema, ema, fwma, hma, linreg, midpoint, pwma, rma,
    sinwma, sma, swma, t3, tema, trima, vidya, wma, zlma"""

    def var():
        alpha = 2 / (lentgh + 1)
        data['ud1'] = np.where(data['close'] > data['close'].shift(1), (data['close'] - data['close'].shift()), 0)
        data['dd1'] = np.where(data['close'] < data['close'].shift(1), (data['close'].shift() - data['close']), 0)
        data['UD'] = data['ud1'].rolling(9).sum()
        data['DD'] = data['dd1'].rolling(9).sum()
        data['CMO'] = ((data['UD'] - data['DD']) / (data['UD'] + data['DD'])).fillna(0).abs()

        data['Var'] = 0.0
        for i in range(lentgh, len(data)):
            data['Var'].iat[i] = (alpha * data['CMO'].iat[i] * data['close'].iat[i]) + (
                        1 - alpha * data['CMO'].iat[i]) * \
                                 data['Var'].iat[
                                     i - 1]
        return data['Var']


    def getMA(src, length):
        if mav == 'VAR':
            return var()
        else:
            return ta.ma(mav, src, length=length).fillna(value=0)

    data['MAvg'] = getMA(data['close'], lentgh)
    data['fark'] = data['MAvg'] * percent * 0.01
    data['newlongstop'] = data['MAvg'] - data['fark']
    data['newshortstop'] = data['MAvg'] + data['fark']
    data['longstop'] = 0.0
    data['shortstop'] = 0.0

    
    i = 0
    while i < len(data):
        def maxlongstop():
            data.loc[(data['newlongstop'] > data['longstop'].shift(1)), 'longstop'] = data['newlongstop']
            data.loc[(data['longstop'].shift(1) > data['newlongstop']), 'longstop'] = data['longstop'].shift(1)

            return data['longstop']

        def minshortstop():
            data.loc[(data['newshortstop'] < data['shortstop'].shift(1)), 'shortstop'] = data['newshortstop']
            data.loc[(data['shortstop'].shift(1) < data['newshortstop']), 'shortstop'] = data['shortstop'].shift(1)

            return data['shortstop']

        data['longstop'] = np.where((data['MAvg'] > data['longstop'].shift(1)), maxlongstop(), data['newlongstop'])

        data['shortstop'] = np.where((data['MAvg'] < data['shortstop'].shift(1)), minshortstop(),
                                     data['newshortstop'])
        i += 1

    # get xover

    data['xlongstop'] = np.where(
        (
                (data['MAvg'].shift(1) > data['longstop'].shift(1)) &
                (data['MAvg'] < data['longstop'].shift(1))
        ), 1, 0)

    data['xshortstop'] = np.where(
        ((data['MAvg'].shift(1) < data['shortstop'].shift(1)) & (data['MAvg'] > data['shortstop'].shift(1))), 1, 0)

    data['trend'] = 0
    data['dir'] = 0

    i = 0
    while i < len(data):
        data['trend'] = np.where((data['xshortstop'] == 1), 1,
                                 (np.where((data['xlongstop'] == 1), -1, data['trend'].shift(1))))

        data['dir'] = np.where((data['xshortstop'] == 1), 1,
                               (np.where((data['xlongstop'] == 1), -1, data['dir'].shift(1).fillna(1))))

        i += 1

    data['MT'] = np.where(data['dir'] == 1, data['longstop'], data['shortstop'])
    data['OTT'] = np.where(data['MAvg'] > data['MT'], (data['MT'] * (200 + percent) / 200),
                           (data['MT'] * (200 - percent) / 200))
    data['OTT'] = data['OTT'].shift(2)
    ott = pd.DataFrame(data['OTT'])
    ott['MAvg'] = data['MAvg']
    return ott


