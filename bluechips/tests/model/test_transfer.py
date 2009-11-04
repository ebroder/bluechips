from unittest import TestCase
from bluechips import model

class TestTransfer(TestCase):
    def setUp(self):
        self.u1 = model.User('chaz', u'Charles Root', False)
        self.u2 = model.User('boo', u'Boo Ghost', True)
        self.t = model.Transfer(self.u1, self.u2, 1234)

    def test_constructor(self):
        assert self.t.debtor == self.u1
        assert self.t.creditor == self.u2
        assert self.t.amount == 1234

    def test_repr(self):
        assert (repr(self.t) == 
                '<Transfer: from Charles Root to Boo Ghost for 1234>')

    def test_involves(self):
        other_u = model.User('jim', u'Jimbo James', True)
        assert self.t.involves(other_u) == False
        assert self.t.involves(self.u1)
        assert self.t.involves(self.u2)
