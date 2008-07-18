"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.fixture import TestApp
from paste.script.appinstall import SetupCommand
from pylons import config
from routes import url_for

from bluechips import model
from bluechips.model import meta

__all__ = ['url_for', 'TestController', 'sample_users']

sample_users = [u'Alice', u'Bob', u'Charlie', u'Dave', u'Eve']

def setUpPackage():
    # Invoke websetup with the current config file
    SetupCommand('setup-app').run([config['__file__']])
    
    test_user = model.User()
    test_user.username = u'root'
    test_user.name = u'Charlie Root'
    test_user.resident = True
    meta.Session.save(test_user)
    meta.Session.commit()

def tearDownPackage():
    meta.metadata.drop_all()

class TestController(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:%s' % config['__file__'])
        self.app = TestApp(wsgiapp)
        TestCase.__init__(self, *args, **kwargs)
