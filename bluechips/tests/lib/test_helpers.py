from unittest import TestCase
from pylons import request
from datetime import date
from bluechips.lib import helpers as h

class TestHelpers(TestCase):
    def test_grab_real_object(self):
        class Foo(object):
            pass
        foo = Foo()
        foo.bar = 'some string'
        assert h.grab(foo, 'bar') == 'some string'
        try:
            h.grab(foo, 'baz')
        except AttributeError:
            pass
        else:
            raise AssertionError

    def test_grab_any_fake(self):
        assert h.grab(None, 'nonexistent') == ''
        assert h.grab('', 'nonexistent') == ''

    def test_grab_date(self):
        assert h.grab(None, 'date') == date.today()

    def test_grab_user(self):
        class FakeRequest(object):
            pass
        class FakeUser(object):
            pass
        class SomeObject(object):
            pass
        req = FakeRequest()
        req.environ = {}
        req.environ['user'] = FakeUser()
        test_obj = SomeObject()
        req.environ['user'].id = test_obj
        request._push_object(req)
        assert h.grab(None, 'spender_id') == test_obj
        assert h.grab(None, 'creditor_id') == test_obj
        assert h.grab(None, 'debtor_id') == test_obj
        request._pop_object()

    def test_grab_amount(self):
        assert h.grab(None, 'amount') == 0
