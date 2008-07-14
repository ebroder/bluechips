"""
Functions for handling splitting expenditures between people
"""

from bluechips import model
from bluechips.model.meta import Session
from bluechips.lib.helpers import round_currency
from decimal import Decimal
import random

def even_split(e):
    """
    Split up an expenditure evenly among the resident users
    
    e should be a bluechips.model:Expenditure object
    """
    
    residents = Session.query(model.User).filter(model.User.resident==True)
    split_percentage = Decimal(100) / Decimal(residents.count())
    split(e, dict((resident, split_percentage) for resident in residents))

def split(e, split_dict):
    """
    Split up an expenditure.
    
    e should be a bluechips.model:Expenditure object.
    
    split_dict should be a dict mapping from bluechips.model:User
    objects to a decimal:Decimal object representing the percentage
    that user is responsible for.
    
    Percentages will be normalized to sum to 100%.
    
    If the split leaks or gains money due to rounding errors, the
    pennies will be randomly distributed to one of the users.
    
    I mean, come on. You're already living together. Are you really
    going to squabble over a few pennies?
    """
    
    total = sum(split_dict.itervalues())
    
    for user, share in split_dict.iteritems():
        split_dict[user] = share / total
    
    amounts_dict = dict()
    
    for user, share in split_dict.iteritems():
        amounts_dict[user] = round_currency(split_dict[user] * e.amount)
    
    difference = e.amount - sum(amounts_dict.itervalues())
    
    if difference > 0:
        for i in xrange(difference * 100):
            winner = random.choice(amounts_dict.keys())
            amounts_dict[winner] += Decimal('0.01')
    elif difference < 0:
        for i in xrange(difference * -100):
            winner = random.choice(amounts_dict.keys())
            amounts_dict[winner] -= Decimal('0.01')
    
    for user, share in amounts_dict.iteritems():
        s = model.Split()
        s.expenditure = e
        s.user = user
        s.share = share
        Session.save(s)

__all__ = ['split', 'even_split']
