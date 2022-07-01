import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import CommandStart
from aiogram import types

from loader import dp
from keyboards.default.type_asset import type_asset_keyboard
from messages.config import CMD_EMOJI
from states.asset_state import AssetState


@dp.message_handler(CommandStart(), state='*')
@dp.message_handler(filters.Text(equals=CMD_EMOJI.get('change_asset_type')), state=AssetState)
async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = type_asset_keyboard
    async with state.proxy() as data:
        data['type_asset'] = ''
        data['ticker_asset'] = ''

    await AssetState.type_asset.set()
    await message.answer('Привет, я Бот, который может помочь тебе узнать какую либо информацию об инвестиционном инструменте.')
    await message.answer('Выбери тип инструмента', reply_markup=keyboard)
