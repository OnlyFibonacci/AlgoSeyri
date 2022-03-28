def alphaTrend(okunacakCsv): #CSV şeklinde gelen parite verileri 
    basliklar = ['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat', 'tbbav', 'tbqav',
                 'ignore']
    df = pd.read_csv(okunacakCsv, names=basliklar)
    open = df['open']
    close = df['close']
    high = df['high']
    low = df['low']
    volume = df['vol']
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

    at = pd.DataFrame(data=k1, columns=['k1'])
    at['k2'] = k2
    return at
