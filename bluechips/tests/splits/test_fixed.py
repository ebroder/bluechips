from unittest import TestCase
from bluechips.tests import *
from bluechips import model
from bluechips.model import meta
from bluechips.model.types import Currency
from decimal import Decimal

class TestSplitFixed(TestCase):
    def test_simpleSplit(self):
        """
        Test simply splitting a $100 expenditure amongst 4 people
        """
        createUsers(4)
        
        e = model.Expenditure(meta.Session.query(model.User).first(),
                              Currency("100"))
        meta.Session.add(e)
        e.even_split()
        meta.Session.commit()
        
        for s in meta.Session.query(model.Split).\
                filter(model.Split.expenditure==e):
            self.assertEqual(s.share, Currency("25.00"))
        
        deleteExpenditures()
        deleteUsers()
    
    def test_uneven(self):
        """
        Test that expenditures can be split non-evenly
        """
        createUsers(2)
        
        users = meta.Session.query(model.User).all()
        
        e = model.Expenditure(users[0], Currency("100"))
        meta.Session.add(e)
        
        split_dict = {users[0]: Decimal("20"),
                      users[1]: Decimal("80")}
        
        amount_dict = {users[0]: Currency("20"),
                       users[1]: Currency("80")}
        
        e.split(split_dict)
        meta.Session.commit()
        
        for s in meta.Session.query(model.Split):
            self.assertEqual(s.share, amount_dict[s.user])
        
        deleteExpenditures()
        deleteUsers()
    
    def test_unevenBadTotal(self):
        """
        Test that transactions get split up properly when the uneven
        split shares don't add to 100%
        """
        createUsers(2)
        
        users = meta.Session.query(model.User).all()
        
        e = model.Expenditure(users[0], Currency("100.00"))
        meta.Session.add(e)
        
        split_dict = {users[0]: Decimal(10),
                      users[1]: Decimal(15)}
        
        amount_dict = {users[0]: Currency("40"),
                       users[1]: Currency("60")}
        
        e.split(split_dict)
        meta.Session.commit()
        
        for s in meta.Session.query(model.Split):
            self.assertEqual(s.share, amount_dict[s.user])
        
        deleteExpenditures()
        deleteUsers()

    def test_negativeExpenditure(self):
        """
        Test that negative expenditures get split correctly
        """
        createUsers(2)

        users = meta.Session.query(model.User).all()

        e = model.Expenditure(users[0], Currency("100.00"))
        meta.Session.add(e)

        # Force a split that will result in needing to distribute
        # pennies
        split_dict = {users[0]: Decimal(1),
                      users[1]: Decimal(2)}
        e.split(split_dict)
        meta.Session.commit()

        self.assertEqual(e.amount, sum(s.share for s in meta.Session.query(model.Split)))

        deleteExpenditures()
        deleteUsers()

    def test_sevenPeople(self):
        """
        Test that expenses are split as evenly as possible with lots of people
        """
        createUsers(7)

        users = meta.Session.query(model.User).all()

        e = model.Expenditure(users[0], Currency("24.00"))
        meta.Session.add(e)
        e.even_split()
        meta.Session.commit()

        splits = meta.Session.query(model.Split).all()
        self.assertEqual(e.amount, sum(s.share for s in splits))

        max_split = max(s.share for s in splits)
        min_split = min(s.share for s in splits)

        self.assertTrue(max_split - min_split <= Currency(1))

        deleteExpenditures()
        deleteUsers()
