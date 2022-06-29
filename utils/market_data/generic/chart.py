import os
from datetime import date

import plotly.graph_objects as go

from utils.market_data.share_etf.market_data import get_figi_by_search
from utils.market_data.share_etf.candles import get_candles_stock_etf
from utils.market_data.crypto.candles import get_candles_crypto


class Chart:
    """
    Class Chart for creating a chart. Using plotly library
    """

    def __init__(self, type_asset, ticker_asset, time_period):
        self._type = type_asset
        self._ticker = ticker_asset
        self._period = time_period
        if self._type in ['share', 'etf']:
            self._figi = get_figi_by_search(self._ticker, self._type)
            self._data_candles = get_candles_stock_etf(
                self._figi, self._period)
        elif self._type == 'crypto':
            self._data_candles = get_candles_crypto(self._ticker, self._period)

    def _create_path_to_chart(self):
        date_today = date.today().strftime('%d-%m-%Y')
        if self._type in ['share', 'etf']:
            path = os.path.join('charts', date_today,
                                'shares_etf', self._period)
        elif self._type == 'crypto':
            path = os.path.join('charts', date_today, 'crypto', self._period)
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
