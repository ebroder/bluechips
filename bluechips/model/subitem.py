from types import Currency

class Subitem(object):
    def __init__(self, expenditure=None, user=None, amount=Currency(0)):
        self.expenditure = expenditure
        self.user = user
        self.share = share
        
    def __repr__(self):
        return '<Subitem: expense: %s user: %s cost: %s>' % (self.expense,
                                                             self.user,
                                                             self.amount)

__all__ = ['Subitem']
