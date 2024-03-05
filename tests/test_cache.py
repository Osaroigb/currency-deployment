import unittest
from unittest.mock import patch
from app.cache.redis_client import RedisClient

class TestRedisClient(unittest.TestCase):

    @patch('cache.redis_client.redis')
    def test_set_get_value(self, mock_redis):
        
        # Setup
        client = RedisClient()
        mock_redis.from_url.return_value = mock_redis

        test_key = "test_key"
        test_value = "test_value"
        expiry = 3600

        # Test set_value
        client.set_value(test_key, test_value, expiry)
        mock_redis.setex.assert_called_once_with(test_key, expiry, test_value)

        # Test get_value
        mock_redis.get.return_value = test_value.encode('utf-8')
        value = client.get_value(test_key)
        self.assertEqual(value, test_value)

        # Test get_value for non-existent key
        mock_redis.get.return_value = None
        value = client.get_value("non_existent_key")
        self.assertIsNone(value)

if __name__ == '__main__':
    unittest.main()