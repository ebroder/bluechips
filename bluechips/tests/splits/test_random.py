from bluechips.tests import *
from bluechips import model
from bluechips.model import meta
from webhelpers.number import standard_deviation as std_dev

class TestSplitRandom(TestController):
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
            assert sum(s.share for s in e.splits) == e.amount,\
                "Total of splits is not the same as the expenditure total"
    
    def test_splitDistribution(self):
        for e in meta.Session.query(model.Expenditure):
            even_total = (e.amount / meta.Session.query(model.User).count())
            assert std_dev(list(s.share for s in e.splits)) <= even_total, \
                "Expenditure doesn't appear to be evenly distributed"
