from unittest import TestCase
from bluechips.tests import *
from bluechips import model
from bluechips.model import meta
from webhelpers.number import standard_deviation as std_dev

class TestSplitRandom(TestCase):
    @classmethod
    def setUpClass(cls):
        createUsers()
    
    @classmethod
    def tearDownClass(cls):
        deleteUsers()
    
    def setUp(self):
        createExpenditures()
    
    def tearDown(self):
        deleteExpenditures()
    
    def test_splitTotal(self):
        for e in meta.Session.query(model.Expenditure):
            self.assertEqual(sum(s.share for s in e.splits), e.amount)
    
    def test_splitDistribution(self):
        user_count = meta.Session.query(model.User).count()
        for e in meta.Session.query(model.Expenditure):
            even_total = (e.amount / user_count) * user_count
            difference = abs(even_total - e.amount)
            self.assert_(std_dev(list(int(s.share) for s in e.splits)) <= difference, \
                "Expenditure doesn't appear to be evenly distributed")
