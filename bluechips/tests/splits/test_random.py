from bluechips.tests import *
from bluechips import model
from bluechips.model import meta
from bluechips.model.types import Currency
from webhelpers.number import standard_deviation as std_dev
import random

class TestSplitRandom(TestController):
    @classmethod
    def setUpClass(cls):
        for i in xrange(random.randint(2, 5)):
            u = model.User()
            u.username = sample_users[i].lower()
            u.name = sample_users[i]
            u.resident = 1
            meta.Session.save(u)
        meta.Session.commit()
        
    def setUp(self):
        users = meta.Session.query(model.User).all()
        for i in xrange(random.randint(5, 20)):
            e = model.Expenditure()
            e.spender = random.choice(users)
            e.amount = Currency(random.randint(1000, 100000))
            meta.Session.save(e)
            e.even_split()
        meta.Session.commit()
    
    def test_splitTotal(self):
        for e in meta.Session.query(model.Expenditure):
            assert sum(s.share for s in e.splits) == e.amount,\
                "Total of splits is not the same as the expenditure total"
    
    def test_splitDistribution(self):
        for e in meta.Session.query(model.Expenditure):
            even_total = (e.amount / meta.Session.query(model.User).count())
            assert std_dev(list(s.share for s in e.splits)) <= even_total, \
                "Expenditure doesn't appear to be evenly distributed"
