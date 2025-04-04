import requests
import datetime
from app.config import logging, Config
from requests.exceptions import HTTPError
from app.utils.errors import ServiceUnavailableError, UnauthorizedError, UnprocessableEntityError, NotFoundError, BadRequestError, OperationForbiddenError


class CurrencyService:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.open_xr_app_id = Config.OPEN_XR_APP_ID
        self.open_xr_base_url = Config.OPEN_XR_BASE_URL

        self.xecd_api_id = Config.XECD_API_ID
        self.xecd_api_key = Config.XECD_API_KEY
        self.xecd_base_url = Config.XECD_BASE_URL
    

    def validate_currency_code(self, code):
    
        if len(code) != 3:
            raise UnprocessableEntityError(f"Invalid currency code: {code}")


    def get_conversion_rate_v1(self, from_currency, to_currency):
        self.validate_currency_code(from_currency)
        self.validate_currency_code(to_currency)

        logging.info(f"[V1] {from_currency}")
        logging.warning(f"[V1] {to_currency}")

        cache_key = f"v1_{from_currency}_{to_currency}"
        cached = self.redis_client.get_value(cache_key).decode('utf-8') if self.redis_client.get_value(cache_key) else None

        if cached:
            logging.info(f"[V1] {from_currency}/{to_currency} is already cached.")

            rate, timestamp = cached.split('|')
            return {'rate': float(rate), 'timestamp': timestamp}
     
        try:
            url = f"{self.open_xr_base_url}?app_id={self.open_xr_app_id}&base={from_currency}&symbols={to_currency}&prettyprint=false&show_alternative=false"
            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            actual_res = response.json()

            logging.warning("[V1] actual OPEN exhange response:")
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
        
    
    def get_conversion_rate_v2(self, from_currency, to_currency):
        self.validate_currency_code(from_currency)
        self.validate_currency_code(to_currency)

        logging.info(f"[V2] {from_currency}")
        logging.warning(f"[V2] {to_currency}")

        cache_key = f"v2_{from_currency}_{to_currency}"
        cached = self.redis_client.get_value(cache_key).decode('utf-8') if self.redis_client.get_value(cache_key) else None

        if cached:
            logging.info(f"[V2] {from_currency}/{to_currency} is already cached.")
            rate, timestamp = cached.split('|')

            return {'rate': float(rate), 'timestamp': timestamp}

        try:
            url = f"{self.xecd_base_url}/convert_from.json?from={from_currency}&to={to_currency}&amount=1"

            response = requests.get(url, auth=(self.xecd_api_id, self.xecd_api_key))
            
            logging.warning("[V2] Actual XE API response:")
            logging.info(response.json())

            if response.status_code == 401:
                raise UnauthorizedError("Invalid XE API credentials.")
            
            elif response.status_code == 400:
                raise BadRequestError("Bad request to XE API.")
            
            elif response.status_code == 404:
                raise NotFoundError(f"Currency {from_currency} to {to_currency} not found.")
            
            elif response.status_code == 429:
                raise OperationForbiddenError("Rate limit exceeded with XE API.")
            
            elif response.status_code >= 500:
                raise ServiceUnavailableError("XE API is currently unavailable.")

            data = response.json()

            # Get the rate for the specific target currency
            target_data = next((item for item in data["to"] if item["quotecurrency"] == to_currency), None)

            if not target_data:
                raise NotFoundError(f"No conversion rate found for {from_currency} to {to_currency}.")

            rate = target_data["mid"]
            timestamp = data.get("timestamp", datetime.datetime.utcnow().isoformat() + "Z")

            self.redis_client.set_value(cache_key, f"{rate}|{timestamp}", 3600)
            return {'rate': rate, 'timestamp': timestamp}

        except requests.exceptions.RequestException as e:
            logging.error(f"[V2] Request error: {e}")
            raise ServiceUnavailableError("Could not connect to XE API.")
        
        except Exception as e:
            logging.error(f"[V2] General exception: {e}")
            raise BadRequestError(str(e))
        

    def get_account_info(self): 
        try:
            url = f"{self.xecd_base_url}/account_info/"
            response = requests.get(url, auth=(self.xecd_api_id, self.xecd_api_key))

            logging.info("[V2] Account Info response:")
            logging.info(response.text)

            if response.status_code == 401:
                raise UnauthorizedError("Invalid XE API credentials.")
            elif response.status_code >= 500:
                raise ServiceUnavailableError("XE API is currently unavailable.")
            elif response.status_code != 200:
                raise BadRequestError(f"Unexpected error: {response.text}")

            return response.json()

        except requests.exceptions.RequestException as e:
            logging.error(f"[V2] Request error in account info: {e}")
            raise ServiceUnavailableError("Could not connect to XE API.")
        except Exception as e:
            logging.error(f"[V2] Account info error: {e}")
            raise BadRequestError(str(e))


    def get_currencies(self, iso=None, obsolete=False, language="en", additional_info=None, crypto=False):
        try:
            params = {
                "obsolete": str(obsolete).lower(),
                "language": language,
                "crypto": str(crypto).lower()
            }

            if iso:
                params["iso"] = iso
            if additional_info:
                params["additionalInfo"] = additional_info

            url = f"{self.xecd_base_url}/currencies"
            response = requests.get(url, params=params, auth=(self.xecd_api_id, self.xecd_api_key))

            logging.info("[V2] Currencies list response:")
            logging.info(response.text)

            if response.status_code == 401:
                raise UnauthorizedError("Invalid XE API credentials.")
            elif response.status_code >= 500:
                raise ServiceUnavailableError("XE API is currently unavailable.")
            elif response.status_code != 200:
                raise BadRequestError(f"Unexpected error: {response.text}")

            return response.json()

        except requests.exceptions.RequestException as e:
            logging.error(f"[V2] Request error in currencies list: {e}")
            raise ServiceUnavailableError("Could not connect to XE API.")
        except Exception as e:
            logging.error(f"[V2] Currencies fetch error: {e}")
            raise BadRequestError(str(e))