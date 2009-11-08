from types import Currency

class Subitem(object):
    def __init__(self, expenditure=None, user=None, amount=Currency(0)):
        self.expenditure = expenditure # pragma: nocover
        self.user = user # pragma: nocover
        self.share = share # pragma: nocover
        
    def __repr__(self):
        return ('<Subitem: expense: %s user: %s cost: %s>' %
                (self.expense, self.user, self.amount)) # pragma: nocover

__all__ = ['Subitem']
