from aiogram import types

from messages.config import ASSET_EMOJI


def type_asset_markup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(ASSET_EMOJI.get('share'), ASSET_EMOJI.get('etf'))
    keyboard.add(ASSET_EMOJI.get('crypto'))
    return keyboard