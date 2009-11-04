from unittest import TestCase
from bluechips import model

class TestUser(TestCase):
    def setUp(self):
        self.u = model.User('chaz', u'Charles Root', False)

    def test_constructor(self):
        assert self.u.username == 'chaz'
        assert self.u.name == u'Charles Root'
        assert self.u.resident == False

    def test_repr(self):
        assert repr(self.u) == '<User: chaz>'

    def test_str(self):
        assert str(self.u) == 'Charles Root'
