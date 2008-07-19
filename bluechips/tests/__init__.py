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

import bluechips.model
from bluechips.model import meta
from bluechips.model.types import Currency

import random

__all__ = ['url_for', 'TestController',
           'createUsers', 'createExpenditures',
           'deleteUsers', 'deleteExpenditures']

sample_users = [u'Alice', u'Bob', u'Charlie', u'Dave', u'Eve']

def setUpPackage():
    # Invoke websetup with the current config file
    SetupCommand('setup-app').run([config['__file__']])
    
    test_user = bluechips.model.User()
    test_user.username = u'root'
    test_user.name = u'Charlie Root'
    test_user.resident = False
    meta.Session.save(test_user)
    meta.Session.commit()

def tearDownPackage():
    meta.metadata.drop_all()

class TestController(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:%s' % config['__file__'])
        self.app = TestApp(wsgiapp)
        TestCase.__init__(self, *args, **kwargs)

def createUsers(n=None):
    if n is None:
        n = random.randint(2, 5)
    for i in xrange(n):
        u = bluechips.model.User()
        u.username = sample_users[i].lower()
        u.name = sample_users[i]
        u.resident = 1
        meta.Session.save(u)
    meta.Session.commit()

def createExpenditures(n=None):
    if n is None:
        n = random.randint(5, 20)
    users = meta.Session.query(bluechips.model.User).all()
    for i in xrange(n):
        e = bluechips.model.Expenditure()
        e.spender = random.choice(users)
        e.amount = Currency(random.randint(1000, 100000))
        meta.Session.save(e)
        e.even_split()
    meta.Session.commit()

def deleteUsers():
    map(meta.Session.delete, meta.Session.query(bluechips.model.User))

def deleteExpenditures():
    map(meta.Session.delete, meta.Session.query(bluechips.model.Expenditure))
