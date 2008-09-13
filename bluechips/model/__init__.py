"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from bluechips.model.account import Account
from bluechips.model.expenditure import Expenditure
from bluechips.model.debit import Debit
from bluechips.model.credit import Credit
from bluechips.model.subitem import Subitem

from bluechips.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    sm = orm.sessionmaker(autoflush=True, transactional=True, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

__all__ = ['Account', 'Expenditure', 'Debit', 'Credit', 'Subitem',
           'meta']
