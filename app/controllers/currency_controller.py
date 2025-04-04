from app import app
from flask import Blueprint, request
from app.services.currency_service import CurrencyService
from app.utils.api_responses import build_success_response, build_error_response

VERSION_ONE_PREFIX = "/v1"
VERSION_TWO_PREFIX = "/v2"
currency_bp = Blueprint('currency', __name__)


@currency_bp.route(VERSION_ONE_PREFIX + "/conversion", methods=['GET'])
def version_one_conversion():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    
    try:
        currency_service = CurrencyService(app.redis_client)
        conversion_rate = currency_service.get_conversion_rate(from_currency.upper(), to_currency.upper())

        response = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "rate": conversion_rate['rate'],
            "timestamp": conversion_rate['timestamp']
        }

        return build_success_response(message="currency converted successfully", data=response)
    
    except Exception as e:
        return build_error_response(message="Invalid currency code provided.", status=400, data=str(e))
    

# TODO: complete version 2
# @app.route(VERSION_TWO_PREFIX + "/conversion", methods=['GET'])
# def version_two_conversion():