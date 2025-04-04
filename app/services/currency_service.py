import requests
import datetime
from app.config import logging, Config
from requests.exceptions import HTTPError
from app.utils.errors import UnprocessableEntityError, NotFoundError, BadRequestError, OperationForbiddenError


class CurrencyService:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.open_xr_app_id = Config.OPEN_XR_APP_ID
        self.open_xr_base_url = Config.OPEN_XR_BASE_URL


    def validate_currency_code(self, code):
    
        if len(code) != 3:
            raise UnprocessableEntityError(f"Invalid currency code: {code}")


    def get_conversion_rate(self, from_currency, to_currency):
        self.validate_currency_code(from_currency)
        self.validate_currency_code(to_currency)

        logging.info(from_currency)
        logging.info(to_currency)

        cache_key = f"{from_currency}_{to_currency}"
        cached = self.redis_client.get_value(cache_key).decode('utf-8') if self.redis_client.get_value(cache_key) else None

        if cached:
            logging.info(f"{from_currency}/{to_currency} is already cached.")

            rate, timestamp = cached.split('|')
            return {'rate': float(rate), 'timestamp': timestamp}
     
        try:
            url = f"{self.open_xr_base_url}?app_id={self.open_xr_app_id}&base={from_currency}&symbols={to_currency}&prettyprint=false&show_alternative=false"
            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            actual_res = response.json()

            logging.warning("actual response below")
            logging.info(actual_res)

            if not actual_res.get("rates") or to_currency not in actual_res["rates"]:
                raise NotFoundError(f"{from_currency} || {to_currency}")

            rate = actual_res["rates"][to_currency]
            timestamp = datetime.datetime.utcnow().isoformat() + "Z"

            self.redis_client.set_value(cache_key, f"{rate}|{timestamp}", 3600)  # Cache for 1 hour
            return {'rate': rate, 'timestamp': timestamp}
        
        except HTTPError as http_err:
            logging.error(f"HTTPError: {http_err}")
            raise OperationForbiddenError(f"Invalid currency code: {http_err}")
        except Exception as err:
            logging.error(f"ExceptionError: {err}")
            raise BadRequestError(f"Invalid currency code: {err}")