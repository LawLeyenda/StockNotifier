import unittest
from unittest.mock import patch
from stocks import Stocks
import StockData


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.data = StockData.read('test_myStockData.csv')
        self.test = Stocks(self.data)

    def test_price(self):
        with patch('stocks.Stock(ticker).get_price') as mock:
            mock = 300.00
            self.test.price('AAPL')
            self.assertEqual(self.test.myStockData.at["price", 'AAPL'], 300)


if __name__ == '__main__':
    unittest.main()
