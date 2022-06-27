from decimal import Decimal
from datetime import datetime, date
import os
from typing import Dict, List
from dateutil.relativedelta import relativedelta

from tinkoff.invest import Client
from .market_data import API_TOKEN, get_figi_by_search

from tinkoff.invest.schemas import CandleInterval

import plotly.graph_objects as go


PERIOD_DATE = {
    '1m': datetime.today() - relativedelta(months=1),
    '3m': datetime.today() - relativedelta(months=3),
    '6m': datetime.today() - relativedelta(months=6),
    '1y': datetime.today() - relativedelta(years=1)
}


def get_candles_stock_etf(figi, period):
    date_to = datetime.today()
    date_from = PERIOD_DATE.get(period)
    with Client(API_TOKEN) as client:
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


# def create_path_to_graph(ticker, period):
#     date_today = datetime.today().strftime('%d-%m-%Y')
#     path = os.path.join('charts', period, date_today)
#     file_name = f'{ticker}.png'
#     result_path = os.path.join(path, file_name)
#     if os.path.isdir(path):
#         return result_path
#     else:
#         os.mkdir(path)
#     return result_path


# def create_graph_plotly(data):
#     fig = go.Figure(data=[go.Candlestick(x=data['date_data'],
#     open=data['open_data'], high=data['high_data'], low=data['low_data'], close=data['close_data'])])
#     fig.write_image()
#     return fig


# def get_path_to_graph(ticker, type_asset, period):
#     figi = get_figi_by_search(ticker, type_asset)
#     data = get_candles_stock_etf(figi)
#     result_path = create_path_to_graph(ticker, period)
#     fig = create_graph_plotly(data)
#     fig.write_image(result_path, width=1000)
#     return result_path


class Chart:
    
    def __init__(self, type_asset, ticker_asset, time_period):
        self._type = type_asset
        self._ticker = ticker_asset
        self._period = time_period
        self._figi = get_figi_by_search(self._ticker, self._type)
        self._data_candles = get_candles_stock_etf(self._figi, self._period)
    

    def _create_path_to_chart(self):
        date_today = date.today().strftime('%d-%m-%Y')
        path = os.path.join('charts', date_today, self._period)
        file_name = f'{self._ticker}.png'
        result_path = os.path.join(path, file_name)
        if os.path.isdir(path):
            return result_path
        else:
            os.makedirs(path)
        return result_path


    def create_chart(self):
        fig = go.Figure(data=[go.Candlestick(x=self._data_candles['date_data'],
        open=self._data_candles['open_data'], high=self._data_candles['high_data'], 
        low=self._data_candles['low_data'], close=self._data_candles['close_data'])])
        path = self._create_path_to_chart()
        fig.write_image(path, width=1000)
        return path


# if __name__ == '__main__':
#     graph = Graph('share', 'NVTK', '1y')
#     print(graph.get_path_to_graph())
