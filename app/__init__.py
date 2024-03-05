from flask import Flask
from .cache.redis_client import RedisClient
from .utils.rate_limiting import RateLimiter
from .services.currency_service import CurrencyService

# Initialize the Flask application
app = Flask(__name__)

# Initialize Redis Client
app.redis_client = RedisClient()

# Register Flask routes
from . import routes
