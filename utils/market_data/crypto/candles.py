from datetime import datetime
from dateutil.relativedelta import relativedelta

from binance.spot import Spot


PERIOD_DATE = {
    '1m': datetime.today() - relativedelta(months=1),
    '3m': datetime.today() - relativedelta(months=3),
    '6m': datetime.today() - relativedelta(months=6),
    '1y': datetime.today() - relativedelta(years=1)
}


def get_candles_crypto(ticker, period):
    """
    Get info about candles crypto, api: binance API,
    data: date, open, close, high, low
    """
    date_to = int(datetime.today().timestamp() * 1000)
    date_from = int(PERIOD_DATE.get(period).timestamp()*1000)
    spot_client = Spot(base_url="https://api.binance.com")
    if period == '1m':
        candles = spot_client.klines(
            ticker, '6h', startTime=date_from, endTime=date_to)
    elif period == '1y':
        candles = spot_client.klines(
            ticker, '3d', startTime=date_from, endTime=date_to)
    else:
        candles = spot_client.klines(
            ticker, '1d', startTime=date_from, endTime=date_to)
    date_data = []
    open_data = []
    close_data = []
    high_data = []
    low_data = []
    for candle in candles:
        date_ = datetime.fromtimestamp(candle[6]/1000.0)
        open_ = candle[1]
        close = candle[4]
        high = candle[2]
        low = candle[3]
        date_data.append(date_)
        open_data.append(open_)
        close_data.append(close)
        high_data.append(high)
        low_data.append(low)
    return {
        'date_data': date_data,
        'open_data': open_data,
        'close_data': close_data,
        'high_data': high_data,
        'low_data': low_data
    }
