import re
from decimal import Decimal

import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot

from utils.market_data import get_info_share, get_info_etf, get_last_price
from utils.market_data_crypto import get_last_price_crypto
from utils.charts_data import Chart

from keyboards.inline.charts import charts_markup, chart_cb
from keyboards.default.params_share import share_markup
from keyboards.default.params_etf import etf_markup
from keyboards.default.params_crypto import crypto_markup
from keyboards.default.type_asset import type_asset_markup

from messages.config import CMD_EMOJI, ASSET_EMOJI


TRANSLATE_PERIOD = {
    '1m': '1 месяц',
    '3m': '3 месяца',
    '6m': '6 месяцев',
    '1y': '1 год'
}


@dp.message_handler(lambda message: message.text == CMD_EMOJI.get('change_asset_type'))
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = type_asset_markup()
    async with state.proxy() as data:
        data['type_asset'] = ''
        data['ticker_asset'] = ''

    await message.answer('Привет, я Бот, который может помочь тебе узнать какую либо информацию об инвестиционном инструменте.')
    await message.answer('Выбери тип инструмента', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == CMD_EMOJI.get('charts'))
async def chart_test(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        type_asset = data['type_asset']
        ticker_asset = data['ticker_asset']
        if type_asset in ['share', 'etf', 'crypto'] and ticker_asset != '':
            keyboard = charts_markup(type_asset, ticker_asset)
            await message.answer(f'Выберите период графика по {ticker_asset}', reply_markup=keyboard)
        elif type_asset == '':
            await message.answer('Выберите актив')
        elif ticker_asset == '':
            await message.answer('Введите тикер')
        else:
            await message.answer('Выбери другой актив')


@dp.callback_query_handler(chart_cb.filter(action='show_chart'))
async def create_graph(query: types.CallbackQuery, callback_data: dict):
    type_asset = callback_data['type_asset']
    ticker_asset = callback_data['ticker_asset']
    period = callback_data['period']
    message_loading = await bot.send_message(chat_id=query.message.chat.id, text='Загрузка графика...')
    print(type_asset, ticker_asset, period)
    graph = Chart(type_asset, ticker_asset, period)
    path_to_graph = graph.create_chart()
    keyboard = charts_markup(type_asset, ticker_asset)

    await bot.send_photo(chat_id=query.message.chat.id,
        caption=f'График за {TRANSLATE_PERIOD.get(period)} для {ticker_asset}', 
        photo=types.InputFile(path_to_graph), 
        reply_markup=keyboard
    )
    await bot.delete_message(chat_id=query.message.chat.id, message_id=message_loading.message_id)


@dp.message_handler(lambda message: message.text == ASSET_EMOJI.get('share'))
async def cmd_share(message: types.Message, state: FSMContext):
    type_asset = 'share'
    async with state.proxy() as data:
        data['type_asset'] = type_asset
    await message.answer('Введите тикер акции, уникальное короткое название инструмента (длина: 1-6 символов).')


@dp.message_handler(lambda message: message.text == ASSET_EMOJI.get('etf'))
async def cmd_fund(message: types.Message, state: FSMContext):
    type_asset = 'etf'
    async with state.proxy() as data:
        data['type_asset'] = type_asset
    await message.answer('Введите тикер фонда, уникальное короткое название инструмента (длина: 1-6 символов).')


@dp.message_handler(lambda message: message.text == ASSET_EMOJI.get('crypto'))
async def cmd_crypto(message: types.Message, state: FSMContext):
    type_asset = 'crypto'
    async with state.proxy() as data:
        data['type_asset'] = type_asset
    await message.answer('Введите тикер отношения, например: "BTCUSDT"')


@dp.message_handler(lambda message: message.text == CMD_EMOJI.get('last_price'))
async def get_share_last_price(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        ticker_asset = data['ticker_asset']
        type_asset = data['type_asset']

    if type_asset != '' and ticker_asset != '':
        if type_asset == 'share':
            keyboard = share_markup()
            last_price = get_last_price(ticker_asset, type_asset)
            last_price = last_price.quantize(Decimal('1.00'))
        elif type_asset == 'etf':
            keyboard = etf_markup()
            last_price = get_last_price(ticker_asset, type_asset)
            last_price = last_price.quantize(Decimal('1.0000'))
        elif type_asset == 'crypto':
            keyboard = crypto_markup()
            last_price = get_last_price_crypto(ticker_asset)
            last_price = last_price.quantize(Decimal('1.0000'))
        await message.answer(
            fmt.text(
                f'Последняя цена {fmt.hbold(ticker_asset.upper())}:  {fmt.hbold(last_price)}'),
            parse_mode='HTML', reply_markup=keyboard
        )
    elif data['type_asset'] == '':
        await message.answer('Вы не выбрали тип актива')
    elif data['ticker_asset'] == '':
        await message.answer('Вы не вводили тикер интструмента')


@dp.message_handler(lambda message: message.text == ASSET_EMOJI.get('fundamentals'))
async def get_share_fund_info(message: types.Message, state: FSMContext):
    keyboard = share_markup()
    async with state.proxy() as data:
        if data['type_asset'] == 'share' and data['ticker_asset'] != '':
            ticker = data['ticker_asset']
            fundam_data = ticker
            await message.answer(f'Фундаментальные показатели, {ticker.upper()}: P/E: {fundam_data}', reply_markup=keyboard)
            await message.answer('Функционал еще не готов!')
        else:
            await message.answer('ОШИБКА: Для этого типа актива такого функционала нет')


@dp.message_handler(lambda message: message.text == 'Состав фонда')
async def get_fund_structure(message: types.Message):
    keyboard = etf_markup()
    await message.answer('Функционал еще не готов', reply_markup=keyboard)


@dp.message_handler()
@dp.message_handler(lambda message: message.text == CMD_EMOJI.get('general_info'))
async def cmd_info_stock(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        type_asset = data['type_asset']
        if type_asset == 'share':
            if message.text == CMD_EMOJI.get('general_info'):
                ticker = data['ticker_asset']
            else:
                ticker = message.text.upper()
            if re.match(r'(?=^.{1,6}$)[a-zA-Z]', ticker):
                keyboard = share_markup()
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
                keyboard = etf_markup()
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
            keyboard = crypto_markup()
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