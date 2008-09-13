"""
Calculate the total state of the books
"""

from bluechips import model
from bluechips.model import meta

from bluechips.model.types import Currency

import sqlalchemy

class DirtyBooks(Exception):
    """
    If the books don't work out, raise this
    """
    pass

def debts():
    # In this scheme, positive numbers represent money the house owes
    # the account, and negative numbers represent money the account
    # owes the house
    accounts = meta.Session.query(model.Account)
    
    debts_dict = {}
    
    for account in accounts:
        debts_dict[account] = sum(c.amount for c in account.credits)
        debts_dict[account] -= sum(d.amount for d in account.debits)
    
    return debts_dict

def settle(debts_dict):
    # This algorithm has been shamelessly stolen from Nelson Elhage's
    # <nelhage@mit.edu> implementation for our 2008 summer apartment.
    
    debts_list = [dict(who=user, amount=amount) for user, amount in \
                      debts_dict.iteritems()]
    debts_list.sort(reverse=True, key=(lambda x: abs(x['amount'])))
    
    owes_list = [debt for debt in debts_list if debt['amount'] < 0]
    owed_list = [debt for debt in debts_list if debt['amount'] > 0]
    
    settle_list = []
    
    while len(owes_list) > 0 and len(owed_list) > 0:
        owes = owes_list[0]
        owed = owed_list[0]
        
        sum = owes['amount'] + owed['amount']
        if sum == 0:
            # Perfect balance!
            owes_list.pop(0)
            owed_list.pop(0)
            val = owes['amount']
        elif sum < 0:
            # person in owes still owes money
            owes['amount'] += owed['amount']
            owed_list.pop(0)
            val = owed['amount']
        else:
            # person in owed is owed more than owes has to give
            owed['amount'] += owes['amount']
            owes_list.pop(0)
            val = -owes['amount']
        
        settle_list.append((owes['who'], owed['who'], val))
    
    if len(owes_list) > 0:
        raise DirtyBooks, ("People still owe money", owes_list)
    if len(owed_list) > 0:
        raise DirtyBooks, ("People are still owed money", owed_list)
    
    return settle_list

__all__ = ['debts', 'settle']
