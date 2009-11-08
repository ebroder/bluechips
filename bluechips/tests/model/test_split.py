from unittest import TestCase
from bluechips import model
from bluechips.model.types import Currency

class TestSplit(TestCase):
    def setUp(self):
        self.u = model.User('chaz', u'Charles Root', False)
        self.e = model.Expenditure(self.u, Currency('12.34'),
                                   u'A test expenditure')
        self.sp = model.Split(self.e, self.u, Currency('5.55'))

    def test_constructor(self):
        assert self.sp.expenditure == self.e
        assert self.sp.user == self.u
        assert self.sp.share == Currency('5.55')

    def test_repr(self):
        assert (repr(self.sp) == '<Split: expense: %s user: %s share: %s>' %
                (self.sp.expenditure, self.sp.user, self.sp.share))
