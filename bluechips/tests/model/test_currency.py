from unittest import TestCase
from bluechips.tests import *
from bluechips.model.types import Currency
from decimal import Decimal

class TestCurrency(TestCase):
    def test_addition(self):
        """
        Each of these tests tests 3 things:
        
        1) That the math works
        2) That the result is converted to a Currency type
        3) That multiple Currency instances with the same value are
           the same object
        """
        assert Currency(2) + 2 is Currency(4), "Currency + int is Currency"
        assert 2 + Currency(2) is Currency(4), "int + Currency is Currency"
        assert Currency(2) + Currency(2) == Currency(4), \
            "Currency + Currency is Currency"
    
    def test_multiplication(self):
        """
        This test tests the same 3 things as ``test_addition``, but
        for multiplication
        """
        assert Currency(100) * Decimal(0.25) is Currency(25), \
            "Currency * Decimal is Currency"
        assert Decimal(0.25) * Currency(100) is Currency(25), \
            "Decimal * Currency is Currency"
