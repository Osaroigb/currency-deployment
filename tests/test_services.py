import unittest
from unittest.mock import Mock, patch
from app.services.currency_service import CurrencyService
from app.utils.errors import InvalidCurrencyCode, UnprocessableEntityError

class TestCurrencyService(unittest.TestCase):
    
    @patch('services.currency_service.requests.get')
    def test_get_conversion_rate(self, mock_get):
       
        # Setup
        mock_redis_client = Mock()
        service = CurrencyService(mock_redis_client)
        mock_get.return_value.json.return_value = {
            "meta": {"timestamp": 1449885661, "rate": 1.383702},
            "response": 27673.975864
        }

        # Test successful retrieval
        result = service.get_conversion_rate("GBP", "EUR")
        self.assertEqual(result['rate'], 1.383702)
        self.assertIn('timestamp', result)

        # Test invalid currency code
        with self.assertRaises(InvalidCurrencyCode):
            service.get_conversion_rate("FAKE", "EUR")

        # Test HTTP error handling
        mock_get.side_effect = Exception("HTTP Error")
        with self.assertRaises(UnprocessableEntityError):
            service.get_conversion_rate("GBP", "EUR")

if __name__ == '__main__':
    unittest.main()