from decimal import Decimal
from datetime import datetime

import plotly.graph_objects as go
from tinkoff.invest import Client
from tinkoff.invest.schemas import CandleInterval
from binance.spot import Spot 

from market_data import API_TOKEN, get_figi_by_search


def get_candles(figi):
    with Client(API_TOKEN) as client:
        candles = client.get_all_candles(figi=figi, from_=datetime(day=24, month=1, year=2022), 
            to=datetime(day=24, month=6, year=2022), interval=CandleInterval.CANDLE_INTERVAL_DAY)
        date_data = []
        open_data = []
        close_data = []
        high_data = []
        low_data = []
        for item in candles:
            date = item.time
            open_ = Decimal(str(item.open.units) + '.' + str(item.open.nano))
            close = Decimal(str(item.close.units) + '.' + str(item.close.nano))
            high = Decimal(str(item.high.units) + '.' + str(item.high.nano))
            low = Decimal(str(item.low.units) + '.' + str(item.low.nano))
            date_data.append(date)
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


def get_graph_plotly(ticker, type_asset):
    figi = get_figi_by_search(ticker, type_asset)
    data = get_candles(figi)
    fig = go.Figure(data=[go.Candlestick(x=data['date_data'],
    open=data['open_data'], high=data['high_data'], low=data['low_data'], close=data['close_data'])])
    fig.write_image(f'charts/{ticker}.png', width=1000)


def get_candles_crypto(ticker, period):
    spot_client = Spot(base_url="https://api.binance.com")
    candles = spot_client.klines(ticker, '1d', startTime='1624788131000', endTime='1656324131000')
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
