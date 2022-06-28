from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from messages.config import CMD_EMOJI


etf_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(CMD_EMOJI.get('last_price'))
        ],
        [
            KeyboardButton(CMD_EMOJI.get('change_asset_type'))
        ]
    ],
    resize_keyboard=True
)
