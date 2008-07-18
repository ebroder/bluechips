class Expenditure(object):
    def __repr__(self):
        return '<Expenditure: spender: %s spent: %s>' % (self.spender,
                                                         self.amount)

__all__ = ['Expenditure']
