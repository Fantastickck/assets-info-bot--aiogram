from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta

from tinkoff.invest import Client
from tinkoff.invest.schemas import CandleInterval

from config import TINVEST_API_TOKEN

PERIOD_DATE = {
    '1m': datetime.today() - relativedelta(months=1),
    '3m': datetime.today() - relativedelta(months=3),
    '6m': datetime.today() - relativedelta(months=6),
    '1y': datetime.today() - relativedelta(years=1)
}


def get_candles_stock_etf(figi, period):
    """
    Get info about asset candles. Assets: share/etf
    """
    date_to = datetime.today()
    date_from = PERIOD_DATE.get(period)
    with Client(TINVEST_API_TOKEN) as client:
        candles = client.get_all_candles(figi=figi, from_=date_from,
            to=date_to, interval=CandleInterval.CANDLE_INTERVAL_DAY)

        date_data = []
        open_data = []
        close_data = []
        high_data = []
        low_data = []
        for item in candles:
            date_ = item.time
            open_ = Decimal(str(item.open.units) + '.' + str(item.open.nano))
            close = Decimal(str(item.close.units) + '.' + str(item.close.nano))
            high = Decimal(str(item.high.units) + '.' + str(item.high.nano))
            low = Decimal(str(item.low.units) + '.' + str(item.low.nano))
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
