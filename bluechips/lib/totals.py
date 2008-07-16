"""
Calculate the total state of the books
"""

from bluechips import model
from bluechips.model.meta import Session

import sqlalchemy

from decimal import Decimal

def debts():
    # In this scheme, negative numbers represent money the house owes
    # the user, and positive numbers represent money the user owes the
    # house
    users = Session.query(model.User)
    
    debts = {}
    
    # First, credit everyone for expenditures they've made
    for user in users:
        debts[user] = -sum(map((lambda x: x.amount), user.expenditures))
    
    # Next, debit everyone for expenditures that they have an
    # investment in (i.e. splits)
    
    total_splits = Session.query(model.Split).\
        add_column(sqlalchemy.func.sum(model.Split.share), 'total_split').\
        group_by(model.Split.user_id)
    
    for split, total_cents in total_splits:
        debts[split.user] += (total_cents / 100)
    
    # Finally, move transfers around appropriately
    #
    # To keep this from getting to be expensive, have SQL sum up
    # transfers for us
    
    transfer_q = Session.query(model.Transfer).\
        add_column(sqlalchemy.func.sum(model.Transfer.amount), 'total_amount')
    total_debits = transfer_q.group_by(model.Transfer.debtor_id)
    total_credits = transfer_q.group_by(model.Transfer.creditor_id)
    
    for transfer, total_amount in total_debits:
        debts[transfer.debtor] -= total_amount
    for transfer, total_amount in total_credits:
        debts[transfer.creditor] += total_amount
    
    return debts
