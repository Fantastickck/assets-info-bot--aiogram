from aiogram import types

from messages.config import CMD_EMOJI


def etf_markup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(CMD_EMOJI.get('last_price'))
    keyboard.add(CMD_EMOJI.get('change_asset_type'))
    return keyboard