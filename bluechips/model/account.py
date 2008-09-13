import sqlalchemy as sa
from sqlalchemy.orm import relation
from bluechips.model.base import Base, BlueChipsTable
from bluechips.model import types

class Account(Base):
    __tablename__ = 'accounts'
    
    id = sa.Column(types.Integer, primary_key=True)
    username = sa.Column(types.Unicode(32), nullable=False)
    name = sa.Column(types.Unicode(64))
    kind = sa.Column(types.Enum(['RESIDENT', 'BILLER'], empty_to_none=True))
    
    credits = relation('Credit', backref='account')
    debits = relation('Debit', backref='account')
    subitems = relation('Subitem', backref='account')
    
    def __repr__(self):
        return '<Account: %s>' % (self.username)
Account = BlueChipsTable(Account)

__all__ = ['Account']
