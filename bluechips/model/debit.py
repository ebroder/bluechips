import sqlalchemy as sa
from sqlalchemy.orm import relation
from bluechips.model.base import Base, BlueChipsTable
from bluechips.model import types

class Debit(Base):
    __tablename__ = 'debits'
    
    id = sa.Column(types.Integer, primary_key=True)
    expenditure_id = sa.Column(sa.ForeignKey('expenditures.id'), nullable=False)
    account_id = sa.Column(sa.ForeignKey('accounts.id'), nullable=False)
    amount = sa.Column(types.DBCurrency, nullable=False, default=types.Currency(0))
    
    unique_debits = sa.UniqueConstraint('expenditure_id', 'account_id')
    
    def __repr__(self):
        return '<Debit: expense: %s account: %s amount: %s>' % (self.expenditure,
                                                                self.account,
                                                                self.amount)
Debit = BlueChipsTable(Debit)

__all__ = ['Debit']
