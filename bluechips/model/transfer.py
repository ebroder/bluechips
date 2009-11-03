from types import Currency

class Transfer(object):
    def __init__(self, debtor=None, creditor=None, amount=Currency(0)):
        self.debtor = debtor
        self.creditor = creditor
        self.amount = amount
    
    def __repr__(self):
        return '<Transfer: from %s to %s for %s>' % (self.debtor,
                                                     self.creditor,
                                                     self.amount)

    def involves(self, user):
        return (self.debtor == user) or (self.creditor == user)

__all__ = ['Transfer']
