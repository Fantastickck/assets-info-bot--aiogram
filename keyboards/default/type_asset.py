from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from messages.config import ASSET_EMOJI


type_asset_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(ASSET_EMOJI.get('share')),
            KeyboardButton(ASSET_EMOJI.get('etf'))
        ],
        [
            KeyboardButton(ASSET_EMOJI.get('crypto'))
        ]
    ],
    resize_keyboard=True
)
