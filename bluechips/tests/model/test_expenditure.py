from decimal import Decimal

from unittest import TestCase
from bluechips import model
from bluechips.model import meta
from bluechips.model.types import Currency

class TestExpenditure(TestCase):
    def setUp(self):
        self.u = model.User(u'chaz', u'Charles Root', False)
        self.e = model.Expenditure(self.u, Currency('444.88'),
                                   u'chaz buys lunch')
        meta.Session.add(self.u)
        meta.Session.add(self.e)
        meta.Session.commit()

    def test_constructor(self):
        assert self.e.spender == self.u
        assert self.e.amount == Currency('444.88')
        assert self.e.description == u'chaz buys lunch'

    def test_repr(self):
        assert (repr(self.e) == 
                '<Expenditure: spender: Charles Root spent: $444.88>')

    def test_even_split(self):
        self.e.even_split()
        meta.Session.commit()
        for sp in self.e.splits:
            assert sp.share == Currency('111.22')

    def test_split_change_to_zero(self):
        self.e.even_split()
        meta.Session.commit()
        users = meta.Session.query(model.User).all()
        split_dict = dict((user, Decimal('0')) for user in users)
        split_dict[self.u] = Decimal(1)
        self.e.split(split_dict)

    def _two_way_split_test(self, amount, min, max):
        e2 = model.Expenditure(self.u, amount,
                              u'testing splits')
        u2 = model.User(u'bo', u'Bo Jangles', False)
        meta.Session.add(u2)
        meta.Session.add(e2)
        meta.Session.commit()
        split_dict = {}
        split_dict[self.u] = Decimal(1)
        split_dict[u2] = Decimal(1)
        e2.split(split_dict)
        assert min <= e2.share(u2) <= max
        meta.Session.delete(e2)
        meta.Session.delete(u2)
        meta.Session.commit()

    def test_split_rounds_down(self):
        self._two_way_split_test(Currency('40.01'),
                                 Currency('20.00'),
                                 Currency('20.01'))

    def test_split_rounds_up(self):
        self._two_way_split_test(Currency('39.99'),
                                 Currency('19.99'),
                                 Currency('20.00'))

    def test_split_small(self):
        self._two_way_split_test(Currency('0.01'),
                                 Currency('0.00'),
                                 Currency('0.01'))

    def test_split_small_negative(self):
        self._two_way_split_test(Currency('-0.01'),
                                 Currency('-0.01'),
                                 Currency('-0.00'))

    def test_split_irrational_rounding(self):
        e2 = model.Expenditure(self.u, Decimal('2375.00'),
                               u'rounding test')
        u2 = model.User(u'rat', u'Irrational Rat', False)
        meta.Session.add(u2)
        meta.Session.add(e2)
        meta.Session.commit()
        split_dict = {}
        split_dict[u2] = Decimal('750.00')
        split_dict[self.u] = Decimal('4000.00')
        e2.split(split_dict)
        assert e2.share(u2) == Decimal('375.00')
        meta.Session.delete(e2)
        meta.Session.delete(u2)
        meta.Session.commit()

    def tearDown(self):
        meta.Session.delete(self.e)
        meta.Session.delete(self.u)
        meta.Session.commit()
