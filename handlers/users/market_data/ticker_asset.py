import re

import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from loader import dp

from keyboards.default.params_crypto import crypto_keyboard
from keyboards.default.params_etf import etf_keyboard
from keyboards.default.params_share import share_keyboard

from messages.config import ASSET_EMOJI, CMD_EMOJI
from states.asset_state import AssetState
from utils.market_data.crypto.market_data import get_last_price_crypto
from utils.market_data.share_etf.market_data import get_info_etf, get_info_share


@dp.message_handler(state=AssetState)
@dp.message_handler(filters.Text(equals=CMD_EMOJI.get('general_info')), state=AssetState)
async def choice_ticker_asset(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        type_asset = data['type_asset']
        if type_asset == 'share':
            print(type_asset)
            if message.text == CMD_EMOJI.get('general_info'):
                ticker = data['ticker_asset']
            else:
                ticker = message.text.upper()
            print(ticker)
            if re.match(r'(?=^.{1,6}$)[a-zA-Z]', ticker):
                keyboard = share_keyboard
                data['ticker_asset'] = ticker
                try:
                    share_info = get_info_share(ticker, type_asset)
                except:
                    await message.answer('Я не нашел тикер такой акции(, попробуй еще раз')
                else:
                    name = share_info['name']
                    sector = share_info['sector']
                    currency = share_info['currency']
                    country_of_risk = share_info['country_of_risk']
                    country_of_risk_name = share_info['country_of_risk_name']
                    await message.answer(fmt.text(
                        f'Название эмитента: {fmt.hbold(name)}\n' +
                        f'Тип актива: {fmt.hbold(ASSET_EMOJI.get(type_asset))}\n' +
                        f'Валюта актива: {fmt.hbold(currency).upper()}\n' +
                        f'Сектор эк-ки: {fmt.hbold(sector)}\n' +
                        f'Страна: {country_of_risk_name} ({fmt.hbold(country_of_risk)})',
                    ),
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )
            else:
                await message.answer('Упс, неправильный формат тикера(. Попробуй еще раз')
        elif type_asset == 'etf':
            if message.text == CMD_EMOJI.get('general_info'):
                ticker = data['ticker_asset']
            else:
                ticker = message.text.upper()
            if re.match(r'(?=^.{1,6}$)[a-zA-Z]', ticker):
                keyboard = etf_keyboard
                data['ticker_asset'] = ticker
                try:
                    etf_info = get_info_etf(ticker, type_asset)
                except:
                    await message.answer('Я не нашел тикер такой акции(, попробуй еще раз')
                else:
                    name = etf_info['name']
                    focus_type = etf_info['focus_type']
                    currency = etf_info['currency']
                    country_of_risk = etf_info['country_of_risk']
                    country_of_risk_name = etf_info['country_of_risk_name']
                    await message.answer(fmt.text(
                        f'Название эмитента: {fmt.hbold(name)}\n' +
                        f'Тип актива: {fmt.hbold(ASSET_EMOJI.get(type_asset))}\n' +
                        f'Валюта актива: {fmt.hbold(currency).upper()}\n' +
                        f'Фокусный актив: {fmt.hbold(focus_type.upper())}\n' +
                        f'Страна: {country_of_risk_name} ({fmt.hbold(country_of_risk)})',
                    ),
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )
            else:
                await message.answer('Упс, неправильный формат тикера(. Попробуй еще раз')

        elif type_asset == 'crypto':
            keyboard = crypto_keyboard
            if message.text == CMD_EMOJI.get('general_info'):
                ticker = data['ticker_asset']
            else:
                ticker = message.text.upper()
            data['ticker_asset'] = ticker
            try:
                last_price = get_last_price_crypto(ticker)
            except:
                await message.answer('Неправильный тикер. Попробуй например: "BTCUSDT"')
            else:
                await message.answer(f'Соотношение: {ticker}', reply_markup=keyboard)
        else:
            await message.answer('Выбери тип инструмента')
