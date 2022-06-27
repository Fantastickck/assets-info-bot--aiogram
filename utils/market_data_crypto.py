from decimal import Decimal

from binance.spot import Spot 


spot_client = Spot(base_url="https://api.binance.com")

def get_last_price_crypto(ticker):
    last_price = Decimal(spot_client.ticker_price(ticker)['price'])
    return last_price.quantize(Decimal('1.0000'))


if __name__ == '__main__':
    print(get_last_price_crypto('BTCUSDT'))