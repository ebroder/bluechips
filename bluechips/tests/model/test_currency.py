from unittest import TestCase
from bluechips.tests import *
from bluechips.model.types import Currency
from decimal import Decimal

class TestCurrency(TestCase):
    def test_initInt(self):
        """
        Make sure the constructor for Currency works
        """
        self.assert_(Currency(1) is Currency(1), 
                     "Currency objects not interned")
    def test_initString(self):
        """
        Make sure the constructor for Currency works with strings
        """
        self.assertEqual(Currency("0.01"), Currency(1))
        self.assert_(Currency("0.01") is Currency(1),
                     "string and int constructors return different values")
    
    def test_string(self):
        """
        Test converting a Currency to a string
        """
        self.assertEqual(str(Currency(1)), "$0.01")
        self.assertEqual(str(Currency(100)), "$1.00")
        self.assertEqual(str(Currency(101)), "$1.01")
        self.assertEqual(str(Currency(-1)), "-$0.01")
        self.assertEqual(str(Currency(-100)), "-$1.00")
        self.assertEqual(str(Currency(-101)), "-$1.01")
    
    def test_additionMath(self):
        """
        Confirm that addition works over currency types and ints
        """
        self.assertEqual(Currency(2) + 2, Currency(4))
        self.assertEqual(2 + Currency(2), Currency(4))
        self.assertEqual(Currency(2) + Currency(2), Currency(4))
    
    def test_additionType(self):
        """
        Adding Currencies or a Currency and an int should yield a
        Currency
        """
        self.assertEqual(type(Currency(2) + 2), Currency)
        self.assertEqual(type(2 + Currency(2)), Currency)
        self.assertEqual(type(Currency(2) + Currency(2)), Currency)
        
    def test_multMath(self):
        """
        This test tests the same 3 things as ``test_addition``, but
        for multiplication
        """
        self.assertEqual(Currency(100) * Decimal("0.25"), Currency(25))
        self.assertEqual(Decimal("0.25") * Currency(100), Currency(25))
        self.assertEqual(Currency(10) * Currency(10), Currency(100))
    
    def test_multType(self):
        """
        The result of multiplying a Currency with something else
        should be a currency
        """
        self.assertEqual(type(Currency(100) * Decimal("0.25")), Currency)
        self.assertEqual(type(Decimal("0.25") * Currency(100)), Currency)
        self.assertEqual(type(Currency(100) * Currency(100)), Currency)
