class Subitem(object):
    def __repr__(self):
        return '<Subitem: expense: %s user: %s cost: %s>' % (self.expense,
                                                             self.user,
                                                             self.amount)

__all__ = ['Subitem']
