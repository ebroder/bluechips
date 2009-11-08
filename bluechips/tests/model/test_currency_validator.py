from unittest import TestCase
from formencode import Invalid

from bluechips.model import types

class TestCurrencyValidator(TestCase):
    def setUp(self):
        self.v = types.CurrencyValidator()

    def test_currency_validator_good(self):
        assert (self.v.to_python('12.34') ==
                types.Currency('12.34'))

    def test_currency_validator_nonzero(self):
        try:
            self.v.to_python('0')
        except Invalid:
            pass

    def test_currency_validator_precision(self):
        try:
            self.v.to_python('12.345')
        except Invalid:
            pass

    def test_currency_validator_amount(self):
        try:
            self.v.to_python('foo')
        except Invalid:
            pass
