from decimal import Decimal
from datetime import datetime
import os
from IPython.display import Image

from tinkoff.invest import Client
from market_data import API_TOKEN, get_figi_by_search

from tinkoff.invest.schemas import CandleInterval

import plotly.graph_objects as go
from datetime import datetime


def get_candles(figi):
    with Client(API_TOKEN) as client:
        candles = client.get_all_candles(figi=figi, from_=datetime(day=24, month=1, year=2022), 
        to=datetime(day=24, month=6, year=2022), interval=CandleInterval.CANDLE_INTERVAL_DAY)
    #     candles_list = []
    #     for item in candles:
    #         open_ = Decimal(str(item.open.units) + '.' + str(item.open.nano))
    #         close = Decimal(str(item.close.units) + '.' + str(item.close.nano))
    #         high = Decimal(str(item.high.units) + '.' + str(item.high.nano))
    #         low = Decimal(str(item.low.units) + '.' + str(item.low.nano))
    #         candle = (item.time, open_, close, high, low)
    #         candles_list.append(candle)
    # return candles_list
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
    # fig.show()


if __name__ == '__main__':
    get_graph_plotly('AAPL', 'share')
    # data = get_candles('AAPL', 'share')

    # fig = go.Figure(data=[go.Candlestick(x=data['date_data'],
    # open=data['open_data'], high=data['high_data'], low=data['low_data'], close=data['close_data'])])

    # fig.write_image('charts/lol.png')
    # fig.show()

#     import matplotlib.pyplot as plt
#     from mpl_finance import candlestick_ohlc
#     import pandas as pd
#     import matplotlib.dates as mpl_dates
#     import numpy as np
#     import datetime

#     stock_prices = pd.DataFrame({'date': data[0],
#                                 'open': data[1],
#                                 'close': data[2],
#                                 'high': data[3],
#                                 'low': data[4]})

#     ohlc = stock_prices.loc[:, ['date', 'open', 'high', 'low', 'close']]
#     ohlc['date'] = pd.to_datetime(ohlc['date'])
#     ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num)
#     ohlc = ohlc.astype(float)

#     # Creating Subplots
#     fig, ax = plt.subplots()
#     fig.set_size_inches(10, 5)

#     candlestick_ohlc(ax, ohlc.values, width=1.3, colorup='red',
#                     colordown='green', alpha=0.4)

#     # Setting labels & titles
#     ax.set_xlabel('Дата')
#     ax.set_ylabel('Цена')
#     fig.suptitle('График цены за 6 мес')

#     date_format = mpl_dates.DateFormatter('%d-%m-%Y')
#     ax.xaxis.set_major_formatter(date_format)
#     fig.autofmt_xdate()

#     fig.tight_layout()

#     plt.savefig('charts/fin.png')
