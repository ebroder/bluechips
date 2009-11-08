from unittest import TestCase
from bluechips.model import types

class TestCurrency(TestCase):
    def setUp(self):
        self.c = types.Currency('12.34')

    def test_currency_float(self):
        assert float(self.c) == 1234.

    def test_currency_int(self):
        val = int(self.c)
        assert val == 1234
        assert type(val) == int

    def test_currency_long(self):
        val = long(self.c)
        assert val == 1234
        assert type(val) == long
