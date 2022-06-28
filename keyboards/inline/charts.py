from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


chart_cb = CallbackData('vote', 'action', 'period',
                        'ticker_asset', 'type_asset')


def charts_markup(type_asset, ticker_asset):
    charts_inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('1 мес', callback_data=chart_cb.new(
                    action='show_chart', period='1m', type_asset=type_asset, ticker_asset=ticker_asset)),
                InlineKeyboardButton('3 мес', callback_data=chart_cb.new(
                    action='show_chart', period='3m', type_asset=type_asset, ticker_asset=ticker_asset))
            ],
            [
                InlineKeyboardButton('6 мес', callback_data=chart_cb.new(
                    action='show_chart', period='6m', type_asset=type_asset, ticker_asset=ticker_asset)),
                InlineKeyboardButton('1 год', callback_data=chart_cb.new(
                    action='show_chart', period='1y', type_asset=type_asset, ticker_asset=ticker_asset))
            ]
        ]
    )
    return charts_inline_keyboard
