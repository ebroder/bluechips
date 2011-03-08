from bluechips.model.user import User
from bluechips.model.split import Split
from bluechips.model import meta
from bluechips.model.types import Currency
from decimal import Decimal
from datetime import datetime
import random

class Expenditure(object):
    def __init__(self, spender=None, amount=Currency(0), description=u"",
                 date=None):
        self.spender = spender
        self.amount = amount
        self.description = description
        if self.date == None:
            self.date = datetime.now()
    
    def __repr__(self):
        return '<Expenditure: spender: %s spent: %s>' % (self.spender,
                                                         self.amount)

    def even_split(self):
        """
        Split up an expenditure evenly among the resident users
        """
        
        residents = meta.Session.query(User).filter(User.resident==True)
        split_percentage = Decimal(100) / Decimal(residents.count())
        self.split(dict((resident, split_percentage) for resident in residents))
    
    def split(self, split_dict):
        """
        Split up an expenditure.
        
        split_dict should be a dict mapping from bluechips.model:User
        objects to a decimal:Decimal object representing the percentage
        that user is responsible for.
        
        Percentages will be normalized to sum to 100%.
        
        If the split leaks or gains money due to rounding errors, the
        pennies will be randomly distributed to a subset of the users.
        
        I mean, come on. You're already living together. Are you really
        going to squabble over a few pennies?
        """
        
        map(meta.Session.delete, meta.Session.query(Split).\
                filter_by(expenditure_id=self.id))
        
        total = sum(split_dict.itervalues())
        
        for user, share in split_dict.items():
            if share == 0:
                del split_dict[user]
            
        amounts_dict = dict()
        
        for user, share in split_dict.iteritems():
            amounts_dict[user] = Currency((share * self.amount) / total)
        
        difference = self.amount - sum(amounts_dict.itervalues())

        winners = random.sample(amounts_dict.keys(), abs(int(difference)))
        for winner in winners:
            amounts_dict[winner] += Currency(1) if difference > 0 else Currency(-1)
        
        for user, share in amounts_dict.iteritems():
            s = Split(self, user, share)
            meta.Session.add(s)

    def involves(self, user):
        "Returns True if ``user`` is involved in this expenditure."
        return (any((split.user == user) and (split.share != 0)
                    for split in self.splits) or
                (self.spender == user))

    def share(self, user):
        "Return the share corresponding to ``user``."
        shares = dict((split.user, split.share)
                      for split in self.splits)
        return shares.get(user, Currency(0))

__all__ = ['Expenditure']
