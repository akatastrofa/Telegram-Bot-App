import requests
import json
from keys_and_token import keys

class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def converter(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты {base}.\
\nНажмите /help, чтобы узнать, как пользоваться ботом')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}\
\nНажмите /help, чтобы узнать, как пользоваться ботом')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}\
\nНажмите /help, чтобы узнать, как пользоваться ботом')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество валюты {amount}\
\nНажмите /help, чтобы узнать, как пользоваться ботом')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
