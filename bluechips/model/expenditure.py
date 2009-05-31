import sqlalchemy as sa
from sqlalchemy.orm import relation
from bluechips.model.base import Base, BlueChipsTable
from bluechips.model import types
from bluechips.model import meta
from bluechips.model.account import Account
from bluechips.model.debit import Debit
from bluechips.model.types import Currency

from decimal import Decimal
from datetime import datetime
import random

class Expenditure(Base):
    __tablename__ = 'expenditures'
    
    id = sa.Column(types.Integer, primary_key=True)
    description = sa.Column(types.Text, nullable=False)
    date = sa.Column(types.Date, nullable=False, default=datetime.utcnow)
    
    credits = relation('Credit', backref='expenditure',
                       cascade='all, delete-orphan')
    debits = relation('Debit', backref='expenditure',
                      cascade='all, delete-orphan')
    subitems = relation('Subitem', backref='expenditure',
                        cascade='all, delete-orphan')
    
    __mapper_args__ = dict(order_by=date.desc())
    
    def __repr__(self):
        return '<Expenditure: %s>' % self.description
    
    def even_split(self):
        """
        Split up the debits from an expenditure evenly among the
        resident users
        """
        
        residents = meta.Session.query(Account).filter(Account.kind==u'RESIDENT')
        split_percentage = Decimal(100) / Decimal(residents.count())
        self.split(dict((resident, split_percentage) for resident in residents))
    
    def update_split(self):
        """
        Re-split the debits from an expenditure using the same ratios
        as are currently in the database
        """
        
        old_debits = meta.Session.query(Debit).filter(Debit.expenditure==self)
        ratios = dict((s.account, Decimal(int(s.amount))) for s in old_debits)
        self.split(ratios)
    
    def split(self, ratios):
        """
        Split up an expenditure.
        
        ratios should be a dict mapping from bluechips.model:Account
        objects to a decimal:Decimal object representing the
        percentage that account is responsible for.
        
        Percentages will be normalized to sum to 100%.
        
        If the split leaks or gains money due to rounding errors, the
        pennies will be randomly distributed to one of the accounts.
        
        I mean, come on. You're already living together. Are you really
        going to squabble over a few pennies?
        """
        
        map(meta.Session.delete, meta.Session.query(Debit).\
                filter(Debit.expenditure==self))
        
        total = sum(c.amount for c in self.credits)
        ratio_total = sum(ratios.itervalues())
        
        # Using ratios.items instead of ratios.iteritems lets me
        # delete things from the dict. And it's bound to be a small
        # dict, so the efficiency hit won't be noticeable
        for account, share in ratios.items():
            if share == 0:
                del ratios[account]
            else:
                ratios[account] = share / ratio_total
        
        amounts_dict = dict()
        
        for account, share in ratios.iteritems():
            amounts_dict[account] = Currency(ratios[account] * total)
        
        difference = total - sum(amounts_dict.itervalues())
        
        if difference > 0:
            for i in xrange(difference):
                winner = random.choice(amounts_dict.keys())
                amounts_dict[winner] += Currency(1)
        elif difference < 0:
            for i in xrange(-difference):
                winner = random.choice(amounts_dict.keys())
                amounts_dict[winner] -= Currency(1)
        
        for account, amount in amounts_dict.iteritems():
            d = Debit(expenditure=self,
                      account=account,
                      amount=amount)
            meta.Session.save(d)

__all__ = ['Expenditure']
