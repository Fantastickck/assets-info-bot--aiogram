from aiogram.dispatcher.filters.state import State, StatesGroup


class AssetState(StatesGroup):
    type_asset = State()
    ticker_asset = State()