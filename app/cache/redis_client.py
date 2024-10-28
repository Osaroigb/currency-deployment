import os
import redis
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    def __init__(self):
        # self.client = redis.Redis(host='localhost', port=6379, db=0)
        REDISCLOUD_URL = os.getenv("REDISCLOUD_URL")
        self.client = redis.Redis.from_url(REDISCLOUD_URL)

    def set_value(self, key, value, expiry):
        self.client.setex(key, expiry, value)

    def get_value(self, key):
        return self.client.get(key)