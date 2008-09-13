import sqlalchemy as sa
from sqlalchemy.orm import relation
from bluechips.model.base import Base, BlueChipsTable
from bluechips.model import types

class Subitem(Base):
    __tablename__ = 'subitems'
    
    id = sa.Column(types.Integer, primary_key=True)
    expenditure_id = sa.Column(sa.ForeignKey('expenditures.id'), nullable=False)
    account_id = sa.Column(sa.ForeignKey('accounts.id'), nullable=False)
    description = sa.Column(sa.Text)
    amount = sa.Column(types.DBCurrency, nullable=False, default=types.Currency(0))
    
    def __repr__(self):
        return '<Subitem: expense: %s user: %s cost: %s>' % (self.expenditure,
                                                             self.user,
                                                             self.amount)
Subitem = BlueChipsTable(Subitem)

__all__ = ['Subitem']
