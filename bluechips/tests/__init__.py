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

sample_users = [u'Alice', u'Bob', u'Charlie', u'Dave', u'Eve', u'Frank', u'Gina']

def setUpPackage():
    # Invoke websetup with the current config file
    SetupCommand('setup-app').run([config['__file__']])
    
    u1 = bluechips.model.User(u'root', u'Charlie Root', True)
    u1.email = u'charlie@example.com'
    u1.password = u'charliepass'
    u2 = bluechips.model.User(u'ben', u'Ben Bitdiddle', True)
    u3 = bluechips.model.User(u'gotta', u'Gotta Lisp', True)
    u4 = bluechips.model.User(u'rich', u'Rich Scheme', True)

    for u in (u1, u2, u3, u4):
        meta.Session.add(u)
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
        n = random.randint(2, 7)
    for i in xrange(n):
        u = bluechips.model.User(sample_users[i].lower(), resident=True)
        meta.Session.add(u)
    meta.Session.commit()

def createExpenditures(n=None):
    if n is None:
        n = random.randint(5, 20)
    users = meta.Session.query(bluechips.model.User).all()
    for i in xrange(n):
        e = bluechips.model.Expenditure(random.choice(users),
                                        Currency(random.randint(1000, 100000)))
        meta.Session.add(e)
        e.even_split()
    meta.Session.commit()

def deleteUsers():
    map(meta.Session.delete, meta.Session.query(bluechips.model.User))

def deleteExpenditures():
    map(meta.Session.delete, meta.Session.query(bluechips.model.Expenditure))
