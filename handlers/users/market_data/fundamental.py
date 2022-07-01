import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from numpy import histogram_bin_edges

from loader import dp
from keyboards.default.params_share import share_keyboard
from messages.config import CMD_EMOJI
from states.asset_state import AssetState

from utils.market_data.share_etf.fundamental import get_fundamental


@dp.message_handler(filters.Text(equals=CMD_EMOJI.get('fundamentals')), state=AssetState)
async def get_share_fund_info(message: types.Message, state: FSMContext):
    keyboard = share_keyboard
    async with state.proxy() as data:
        if data['type_asset'] == 'share' and data['ticker_asset'] != '':
            ticker = data['ticker_asset']
            fundam_data = get_fundamental(ticker)
            if 'Name' in fundam_data:
                await message.answer(fmt.text(
                    f"Эмитент:  {fmt.hbold(fundam_data['Name'])} \n" +
                    f"{fmt.hbold('Оценка стоимости: ')} \n" +
                    f"- P/E:  {fmt.hbold(fundam_data['TrailingPE'])} \n" +
                    f"- P/E forward:  {fmt.hbold(fundam_data['ForwardPE'])} \n" +
                    f"- P/S:  {fmt.hbold(fundam_data['PriceToSalesRatioTTM'])} \n" +
                    f"- P/B:  {fmt.hbold(fundam_data['PriceToBookRatio'])} \n" +
                    f"{fmt.hbold('Отчет о доходах: ')} \n" +
                    f"- EBITDA:  {fmt.hbold(fundam_data['EBITDA'])} \n" +
                    f"- EPS:  {fmt.hbold(fundam_data['EPS'])} \n" +
                    f"{fmt.hbold('Рентабельность: ')} \n" +
                    f"- ROA:  {fmt.hbold(fundam_data['ReturnOnAssetsTTM'])} \n" +
                    f"- ROE:  {fmt.hbold(fundam_data['ReturnOnEquityTTM'])} \n" 
                ),
                reply_markup=keyboard
                )
            else:
                await message.answer('ОШИБКА: Нет данных для этого актива')
        else:
            await message.answer('ОШИБКА: Для этого типа актива такого функционала нет')
