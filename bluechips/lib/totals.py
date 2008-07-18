"""
Calculate the total state of the books
"""

from bluechips import model
from bluechips.model import meta

import sqlalchemy

from decimal import Decimal

class DirtyBooks(Exception):
    """
    If the books don't work out, raise this
    """
    pass

def debts():
    # In this scheme, negative numbers represent money the house owes
    # the user, and positive numbers represent money the user owes the
    # house
    users = meta.Session.query(model.User)
    
    debts = {}
    
    # First, credit everyone for expenditures they've made
    for user in users:
        debts[user] = -sum(map((lambda x: x.amount), user.expenditures))
    
    # Next, debit everyone for expenditures that they have an
    # investment in (i.e. splits)
    
    total_splits = meta.Session.query(model.Split).\
        add_column(sqlalchemy.func.sum(model.Split.share).label('total_split')).\
        group_by(model.Split.user_id)
    
    for split, total_cents in total_splits:
        debts[split.user] += (total_cents / 100)
    
    # Finally, move transfers around appropriately
    #
    # To keep this from getting to be expensive, have SQL sum up
    # transfers for us
    
    transfer_q = meta.Session.query(model.Transfer).\
        add_column(sqlalchemy.func.sum(model.Transfer.amount).label('total_amount'))
    total_debits = transfer_q.group_by(model.Transfer.debtor_id)
    total_credits = transfer_q.group_by(model.Transfer.creditor_id)
    
    for transfer, total_amount in total_debits:
        debts[transfer.debtor] -= (total_amount / 100)
    for transfer, total_amount in total_credits:
        debts[transfer.creditor] += (total_amount / 100)
    
    return debts

def settle(debts_dict):
    # This algorithm has been shamelessly stolen from Nelson Elhage's
    # <nelhage@mit.edu> implementation for our 2008 summer apartment.
    
    debts_list = [dict(who=user, amount=amount) for user, amount in \
                      debts_dict.iteritems()]
    debts_list.sort(reverse=True, key=(lambda x: abs(x['amount'])))
    
    owes_list = [debt for debt in debts_list if debt['amount'] > 0]
    owed_list = [debt for debt in debts_list if debt['amount'] < 0]
    
    settle = []
    
    while len(owes_list) > 0 and len(owed_list) > 0:
        owes = owes_list[0]
        owed = owed_list[0]
        
        sum = owes['amount'] + owed['amount']
        if sum == 0:
            # Perfect balance!
            owes_list.pop(0)
            owed_list.pop(0)
            val = owes['amount']
        elif sum > 0:
            # person in owes still owes money
            owes['amount'] += owed['amount']
            owed_list.pop(0)
            val = -owed['amount']
        else:
            # person in owed is owed more than owes has to give
            owed['amount'] += owes['amount']
            owes_list.pop(0)
            val = owes['amount']
        
        settle.append((owes['who'], owed['who'], val))
    
    if len(owes_list) > 0:
        raise DirtyBooks, ("People still owe money", owes_list)
    if len(owed_list) > 0:
        raise DirtyBooks, ("People are still owed money", owed_list)
    
    return settle

__all__ = ['debts', 'settle']
