import os
from decimal import Decimal

from tinkoff.invest import Client
from tinkoff.invest.schemas import InstrumentIdType, InstrumentStatus


API_TOKEN = os.getenv('TINVEST_TOKEN')


def get_info_share(ticker, type_asset):
    figi = get_figi_by_search(ticker, type_asset)
    with Client(API_TOKEN) as client:
        instruments = client.instruments
        res = instruments.share_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        return {
            'name': res.instrument.name,
            'sector': res.instrument.sector,
            'currency': res.instrument.currency,
            'country_of_risk': res.instrument.country_of_risk,
            'country_of_risk_name': res.instrument.country_of_risk_name
        }


def get_figi_by_search(ticker, type_asset):
    with Client(API_TOKEN) as client:
        instruments = client.instruments
        search = instruments.find_instrument(query=ticker).instruments
        for instrument in reversed(search):
            if instrument.ticker == ticker and instrument.instrument_type == type_asset:
                return instrument.figi


def get_info_etf(ticker, type_asset):
    figi = get_figi_by_search(ticker, type_asset)
    with Client(API_TOKEN) as client:
        instruments = client.instruments
        res = instruments.etf_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
        return {
            'name': res.instrument.name,
            'focus_type': res.instrument.focus_type,
            'currency': res.instrument.currency,
            'country_of_risk': res.instrument.country_of_risk,
            'country_of_risk_name': res.instrument.country_of_risk_name,
        }


def get_last_price(ticker, type_asset):
    figi = get_figi_by_search(ticker, type_asset)
    with Client(API_TOKEN) as client:
        units = client.market_data.get_last_prices(
            figi=[figi]).last_prices[0].price.units
        nano = client.market_data.get_last_prices(
            figi=[figi]).last_prices[0].price.nano
        last_price = Decimal(str(units) + '.' + str(nano))
        return last_price


if __name__ == '__main__':
    print(get_info_etf('FXRB', 'etf'))
