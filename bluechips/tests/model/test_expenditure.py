from unittest import TestCase
from bluechips import model
from bluechips.model.types import Currency

class TestExpenditure(TestCase):
    def setUp(self):
        self.u = model.User('chaz', u'Charles Root', False)
        self.e = model.Expenditure(self.u, Currency('445.27'),
                                   u'chaz buys lunch')

    def test_constructor(self):
        assert self.e.spender == self.u
        assert self.e.amount == Currency('445.27')
        assert self.e.description == u'chaz buys lunch'

    def test_repr(self):
        assert (repr(self.e) == 
                '<Expenditure: spender: Charles Root spent: $445.27>')
