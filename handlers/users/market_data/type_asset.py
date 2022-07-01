import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from loader import dp
from messages.config import ASSET_EMOJI
from states.asset_state import AssetState


@dp.message_handler(filters.Text(equals=ASSET_EMOJI.get('share')), state=AssetState)
async def cmd_share(message: types.Message, state: FSMContext):
    type_asset = 'share'
    async with state.proxy() as data:
        data['type_asset'] = type_asset

    # await AssetState.next()
    await state.update_data(type_asset='share')
    await message.answer('Введите тикер акции, уникальное короткое название инструмента (длина: 1-6 символов).')


@dp.message_handler(filters.Text(equals=ASSET_EMOJI.get('etf')), state=AssetState)
async def cmd_fund(message: types.Message, state: FSMContext):
    type_asset = 'etf'
    async with state.proxy() as data:
        data['type_asset'] = type_asset
    await message.answer('Введите тикер фонда, уникальное короткое название инструмента (длина: 1-6 символов).')


@dp.message_handler(filters.Text(equals=ASSET_EMOJI.get('crypto')), state=AssetState)
async def cmd_crypto(message: types.Message, state: FSMContext):
    type_asset = 'crypto'
    async with state.proxy() as data:
        data['type_asset'] = type_asset
    await message.answer('Введите тикер отношения, например: "BTCUSDT"')
