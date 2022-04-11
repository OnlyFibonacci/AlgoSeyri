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

