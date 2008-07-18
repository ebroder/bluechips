class Transfer(object):
    def __repr__(self):
        return '<Transfer: from %s to %s for %s>' % (self.debtor,
                                                     self.creditor,
                                                     self.amount)

__all__ = ['Transfer']
