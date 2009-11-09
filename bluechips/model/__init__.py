"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from bluechips.model.user import User
from bluechips.model.expenditure import Expenditure
from bluechips.model.split import Split
from bluechips.model.subitem import Subitem
from bluechips.model.transfer import Transfer

from bluechips.model import meta
from bluechips.model import types

from datetime import datetime

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    sm = orm.sessionmaker(autoflush=True, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

### Database Schemas ###

users = sa.Table('users', meta.metadata,
                 sa.Column('id', sa.types.Integer, primary_key=True),
                 sa.Column('username', sa.types.Unicode(32), nullable=False),
                 sa.Column('name', sa.types.Unicode(64)),
                 sa.Column('resident', sa.types.Boolean, default=True),
                 sa.Column('email', sa.types.Unicode(64)),
                 sa.Column('password', sa.types.Unicode(64)),
                 )

expenditures = sa.Table('expenditures', meta.metadata,
                        sa.Column('id', sa.types.Integer, primary_key=True),
                        sa.Column('spender_id', sa.types.Integer,
                                  sa.ForeignKey('users.id'), nullable=False),
                        sa.Column('amount', types.DBCurrency, nullable=False),
                        sa.Column('description', sa.types.Text),
                        sa.Column('date', sa.types.Date, default=datetime.now),
                        sa.Column('entered_time', sa.types.DateTime, 
                                  default=datetime.utcnow)
                        )

splits = sa.Table('splits', meta.metadata,
                  sa.Column('id', sa.types.Integer, primary_key=True),
                  sa.Column('expenditure_id', sa.types.Integer,
                            sa.ForeignKey('expenditures.id'), nullable=False),
                  sa.Column('user_id', sa.types.Integer,
                            sa.ForeignKey('users.id'), nullable=False),
                  sa.Column('share', types.DBCurrency, nullable=False)
                  )

subitems = sa.Table('subitems', meta.metadata,
                    sa.Column('id', sa.types.Integer, primary_key=True),
                    sa.Column('expenditure_id', sa.types.Integer,
                              sa.ForeignKey('expenditures.id'), nullable=False),
                    sa.Column('user_id', sa.types.Integer,
                              sa.ForeignKey('users.id'), nullable=False),
                    sa.Column('amount', types.DBCurrency, nullable=False)
                    )

transfers = sa.Table('transfers', meta.metadata,
                     sa.Column('id', sa.types.Integer, primary_key=True),
                     sa.Column('debtor_id', sa.types.Integer,
                               sa.ForeignKey('users.id'), nullable=False),
                     sa.Column('creditor_id', sa.types.Integer,
                               sa.ForeignKey('users.id'), nullable=False),
                     sa.Column('amount', types.DBCurrency, nullable=False),
                     sa.Column('description', sa.Text, default=None),
                     sa.Column('date', sa.types.Date, default=datetime.now),
                     sa.Column('entered_time', sa.types.DateTime,
                               default=datetime.utcnow)
                     )

### DB/Class Mapping ###

orm.mapper(User, users,
           properties={
        'expenditures': orm.relation(Expenditure,
                                     backref='spender')
})

orm.mapper(Expenditure, expenditures,
           order_by=[expenditures.c.date.desc(), expenditures.c.entered_time.desc()],
           properties={
        'splits': orm.relation(Split, backref='expenditure',
                               cascade='all, delete'),
        'subitems': orm.relation(Subitem, backref='expenditure',
                                 cascade='all, delete')
})

orm.mapper(Split, splits, properties={
        'user': orm.relation(User)
})

orm.mapper(Subitem, subitems, properties={
        'user': orm.relation(User)
})

orm.mapper(Transfer, transfers,
           order_by=[transfers.c.date.desc(), transfers.c.entered_time.desc()],
           properties={
        'debtor': orm.relation(User,
                               primaryjoin=(transfers.c.debtor_id==\
                                                users.c.id)),
        'creditor': orm.relation(User,
                                 primaryjoin=(transfers.c.creditor_id==\
                                                  users.c.id))
})

__all__ = ['users', 'expenditures', 'splits', 'subitems', 'transfers',
           'User', 'Expenditure', 'Split', 'Subitem', 'Transfer',
           'meta']
