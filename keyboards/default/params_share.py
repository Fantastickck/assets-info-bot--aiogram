from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from messages.config import CMD_EMOJI


share_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(CMD_EMOJI.get('general_info'))
        ],
        [
            KeyboardButton(CMD_EMOJI.get('charts')),
            KeyboardButton(CMD_EMOJI.get('last_price'))
        ],
        [
            KeyboardButton(CMD_EMOJI.get('fundamentals'))
        ],
        [
            KeyboardButton(CMD_EMOJI.get('change_asset_type'))
        ]
    ],
    resize_keyboard=True
)
