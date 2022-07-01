from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from loader import dp, bot
from states.asset_state import AssetState

from utils.market_data.generic.chart import Chart
from keyboards.inline.charts import charts_markup, chart_cb
from messages.config import CMD_EMOJI


TRANSLATE_PERIOD = {
    '1m': '1 месяц',
    '3m': '3 месяца',
    '6m': '6 месяцев',
    '1y': '1 год'
}


@dp.message_handler(filters.Text(equals=CMD_EMOJI.get('charts')), state=AssetState)
async def select_chart_period(message: types.Message, state: FSMContext):
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


@dp.callback_query_handler(chart_cb.filter(action='show_chart'), state=AssetState)
async def create_graph(query: types.CallbackQuery, callback_data: dict):
    type_asset = callback_data['type_asset']
    ticker_asset = callback_data['ticker_asset']
    period = callback_data['period']
    message_loading = await bot.send_message(chat_id=query.message.chat.id, text='Загрузка графика...')
    chart = Chart(type_asset, ticker_asset, period)
    path_to_chart = chart.create_chart()
    keyboard = charts_markup(type_asset, ticker_asset)

    await bot.send_photo(chat_id=query.message.chat.id,
        caption=f'График за {TRANSLATE_PERIOD.get(period)} для {ticker_asset}', 
        photo=types.InputFile(path_to_chart), 
        reply_markup=keyboard
    )
    await bot.delete_message(chat_id=query.message.chat.id, message_id=message_loading.message_id)