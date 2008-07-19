from unittest import TestCase
from bluechips.tests import *
from bluechips.model.types import Currency
from decimal import Decimal

class TestCurrency(TestCase):
    def test_initialization(self):
        """
        Make sure the constructor for Currency works
        """
        self.assert_(Currency(1) is Currency(1), 
                     "Currency objects not interned")
        self.assert_(Currency("0.01") is Currency(1),
                     "Currency string conversion breaks")
    
    def test_additionMath(self):
        """
        Confirm that addition works over currency types and ints
        """
        self.assertEqual(Currency(2) + 2, Currency(4))
        self.assertEqual(2 + Currency(2), Currency(4))
        self.assertEqual(Currency(2) + Currency(2), Currency(4))
    
    def test_additionType(self):
        """
        Check that adding Currencies or a Currency and an int yields a
        Currency
        """
        self.assertEqual(type(Currency(2) + 2), Currency)
        self.assertEqual(type(2 + Currency(2)), Currency)
        self.assertEqual(type(Currency(2) + Currency(2)), Currency)
        
    def test_multiplication(self):
        """
        This test tests the same 3 things as ``test_addition``, but
        for multiplication
        """
        assert Currency(100) * Decimal(0.25) is Currency(25), \
            "Currency * Decimal is Currency"
        assert Decimal(0.25) * Currency(100) is Currency(25), \
            "Decimal * Currency is Currency"
