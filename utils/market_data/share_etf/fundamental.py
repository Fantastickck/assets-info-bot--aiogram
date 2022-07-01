import requests

ALPHA_TOKEN = '7GD0WJ5ZNQPZN5UB'


def get_fundamental(ticker):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo'
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker,
        'apikey': ALPHA_TOKEN
    }
    response = requests.get(url=url, params=params)
    return response.json()


if __name__ == '__main__':
    print(get_fundamental('AApp'))