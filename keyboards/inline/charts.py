from aiogram import types
from aiogram.utils.callback_data import CallbackData


chart_cb = CallbackData('vote', 'action', 'period', 'ticker_asset', 'type_asset')


def charts_markup(type_asset, ticker_asset):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('1 мес', callback_data=chart_cb.new(action='show_chart', period='1m', type_asset=type_asset, ticker_asset=ticker_asset)),
        types.InlineKeyboardButton('3 мес', callback_data=chart_cb.new(action='show_chart', period='3m', type_asset=type_asset, ticker_asset=ticker_asset))
    )
    keyboard.add(
        types.InlineKeyboardButton('6 мес', callback_data=chart_cb.new(action='show_chart', period='6m', type_asset=type_asset, ticker_asset=ticker_asset)),
        types.InlineKeyboardButton('1 год', callback_data=chart_cb.new(action='show_chart', period='1y', type_asset=type_asset, ticker_asset=ticker_asset))
    )
    return keyboard