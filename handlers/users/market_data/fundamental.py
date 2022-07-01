import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from loader import dp
from keyboards.default.params_share import share_keyboard
from messages.config import CMD_EMOJI
from states.asset_state import AssetState


@dp.message_handler(filters.Text(equals=CMD_EMOJI.get('fundamentals')), state=AssetState)
async def get_share_fund_info(message: types.Message, state: FSMContext):
    keyboard = share_keyboard
    async with state.proxy() as data:
        if data['type_asset'] == 'share' and data['ticker_asset'] != '':
            ticker = data['ticker_asset']
            fundam_data = ticker
            await message.answer(f'Фундаментальные показатели, {ticker.upper()}: P/E: {fundam_data}', reply_markup=keyboard)
            await message.answer('Функционал еще не готов!')
        else:
            await message.answer('ОШИБКА: Для этого типа актива такого функционала нет')
