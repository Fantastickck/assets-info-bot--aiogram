from decimal import Decimal

import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from loader import dp

from utils.market_data.share_etf.market_data import get_last_price
from utils.market_data.crypto.market_data import get_last_price_crypto

from keyboards.default.params_share import share_keyboard
from keyboards.default.params_etf import etf_keyboard
from keyboards.default.params_crypto import crypto_keyboard

from messages.config import CMD_EMOJI
from states.asset_state import AssetState


@dp.message_handler(filters.Text(equals=CMD_EMOJI.get('last_price')), state=AssetState)
async def get_share_last_price(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        ticker_asset = data['ticker_asset']
        type_asset = data['type_asset']

    if type_asset != '' and ticker_asset != '':
        if type_asset == 'share':
            keyboard = share_keyboard
            last_price = get_last_price(ticker_asset, type_asset)
            last_price = last_price.quantize(Decimal('1.00'))
        elif type_asset == 'etf':
            keyboard = etf_keyboard
            last_price = get_last_price(ticker_asset, type_asset)
            last_price = last_price.quantize(Decimal('1.0000'))
        elif type_asset == 'crypto':
            keyboard = crypto_keyboard
            last_price = get_last_price_crypto(ticker_asset)
            last_price = last_price.quantize(Decimal('1.0000'))
        await message.answer(
            fmt.text(
                f'Последняя цена {fmt.hbold(ticker_asset.upper())}:  {fmt.hbold(last_price)}'), reply_markup=keyboard
        )
    elif data['type_asset'] == '':
        await message.answer('Вы не выбрали тип актива')
    elif data['ticker_asset'] == '':
        await message.answer('Вы не вводили тикер интструмента')