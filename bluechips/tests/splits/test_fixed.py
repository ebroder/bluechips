from bluechips.tests import *
from bluechips import model
from bluechips.model import meta
from bluechips.model.types import Currency

class TestSplitFixed(TestController):
    def test_simpleSplit(self):
        createUsers(4)
        
        e = model.Expenditure()
        e.spender = meta.Session.query(model.User).first()
        e.amount = Currency("100.00")
        meta.Session.save(e)
        e.even_split()
        meta.Session.commit()
        
        for s in meta.Session.query(model.Split).\
                filter(model.Split.expenditure==e):
            assert s.share == Currency("25.00"), \
                "$100 expenditure did not split evenly"
        
        deleteExpenditures()
        deleteUsers()
