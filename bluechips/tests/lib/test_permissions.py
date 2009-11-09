from unittest import TestCase
from bluechips.lib import permissions

class TestReorderingSettle(TestCase):
    def test_authenticate(self):
        assert permissions.authenticate({}, u'root', u'charliepass')
        assert not permissions.authenticate({}, u'root', u'blah')
        assert not permissions.authenticate({}, u'blah', u'charliepass')
        assert not permissions.authenticate({}, u'blah', u'blah')
