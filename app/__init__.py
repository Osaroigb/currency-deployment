from flask import Flask
from flask_cors import CORS
from .cache.redis_client import RedisClient

# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)

# Initialize Redis Client
app.redis_client = RedisClient()

# Register Flask routes
from .routes import *
