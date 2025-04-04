import redis
from app.config import Config


class RedisClient:
    def __init__(self):
        # self.client = redis.Redis(host='localhost', port=6379, db=0)
        self.client = redis.Redis.from_url(Config.REDISCLOUD_URL)

    def set_value(self, key, value, expiry):
        self.client.setex(key, expiry, value)

    def get_value(self, key):
        return self.client.get(key)