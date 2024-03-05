import os
import logging
import requests
import datetime
from dotenv import load_dotenv
from requests.exceptions import HTTPError
from app.utils.errors import InvalidCurrencyCode, UnprocessableEntityError, OperationForbiddenError

load_dotenv()

class CurrencyService:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.app_id = os.getenv("APP_ID")

    def validate_currency_code(self, code):
    
        if len(code) != 3:
            raise InvalidCurrencyCode(f"Invalid currency code: {code}")


    def get_conversion_rate(self, from_currency, to_currency):
        self.validate_currency_code(from_currency)
        self.validate_currency_code(to_currency)

        print(from_currency)
        print(to_currency)

        cache_key = f"{from_currency}_{to_currency}"
        cached = self.redis_client.get_value(cache_key).decode('utf-8') if self.redis_client.get_value(cache_key) else None

        if cached:
            print(f"{from_currency}/{to_currency} is already cached")

            rate, timestamp = cached.split('|')
            return {'rate': float(rate), 'timestamp': timestamp}
     
        try:
            url = f"https://openexchangerates.org/api/latest.json?app_id={self.app_id}&base={from_currency}&symbols={to_currency}&prettyprint=false&show_alternative=false"
            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            actual_res = response.json()

            print("actual response below")
            print(actual_res)

            if not actual_res.get("rates") or to_currency not in actual_res["rates"]:
                raise InvalidCurrencyCode(f"{from_currency} || {to_currency}")

            rate = actual_res["rates"][to_currency]
            timestamp = datetime.datetime.utcnow().isoformat() + "Z"

            self.redis_client.set_value(cache_key, f"{rate}|{timestamp}", 3600)  # Cache for 1 hour
            return {'rate': rate, 'timestamp': timestamp}
        
        except HTTPError as http_err:
            logging.error(f"HTTPError: {http_err}")
            raise InvalidCurrencyCode(f"Invalid currency code: {http_err}")
        except Exception as err:
            logging.error(f"ExceptionError: {err}")
            raise InvalidCurrencyCode(f"Invalid currency code: {err}")