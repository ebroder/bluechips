"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from bluechips.model import meta
from bluechips.model import types

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)

    sm = orm.sessionmaker(autoflush=True, transactional=True, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

### Database Schemas ###

users = sa.Table('users', meta.metadata,
                 sa.Column('id', sa.types.Integer, primary_key=True),
                 sa.Column('username', sa.types.Unicode(32), nullable=False),
                 sa.Column('name', sa.types.Unicode(64)),
                 sa.Column('resident', sa.types.Boolean, default=True)
                 )

expenditures = sa.Table('expenditures', meta.metadata,
                        sa.Column('id', sa.types.Integer, primary_key=True),
                        sa.Column('spender_id', sa.types.Integer,
                                  sa.ForeignKey('users.id'), nullable=False),
                        sa.Column('amount', types.Currency, nullable=False),
                        sa.Column('date', sa.types.Date, default=sa.func.now),
                        sa.Column('entered_time', sa.types.DateTime, 
                                  default=sa.func.now)
                        )

splits = sa.Table('splits', meta.metadata,
                  sa.Column('id', sa.types.Integer, primary_key=True),
                  sa.Column('expenditure_id', sa.types.Integer,
                            sa.ForeignKey('expenditures.id'), nullable=False),
                  sa.Column('user_id', sa.types.Integer,
                            sa.ForeignKey('users.id'), nullable=False),
                  sa.Column('share', sa.types.Integer, nullable=False)
                  )

subitems = sa.Table('subitems', meta.metadata,
                    sa.Column('id', sa.types.Integer, primary_key=True),
                    sa.Column('expenditure_id', sa.types.Integer,
                              sa.ForeignKey('expenditures.id'), nullable=False),
                    sa.Column('user_id', sa.types.Integer,
                              sa.ForeignKey('users.id'), nullable=False),
                    sa.Column('amount', types.Currency, nullable=False)
                    )

transfers = sa.Table('transfers', meta.metadata,
                     sa.Column('id', sa.types.Integer, primary_key=True),
                     sa.Column('debtor_id', sa.types.Integer,
                               sa.ForeignKey('users.id'), nullable=False),
                     sa.Column('creditor_id', sa.types.Integer,
                               sa.ForeignKey('users.id'), nullable=False),
                     sa.Column('amount', types.Currency, nullable=False),
                     sa.Column('date', sa.types.Date, default=sa.func.now),
                     sa.Column('entered_time', sa.types.DateTime,
                               default=sa.func.now),
                     sa.Column('desc', sa.Text, default=None)
                     )

### ORM Classes ###

class User(object):
    def __repr__(self):
        return '<User: %w>' % (self.username)

class Expenditure(object):
    def __repr__(self):
        return '<Expenditure: spender: %s spent: %s>' % (self.spender,
                                               self.amount)

class Split(object):
    def __repr__(self):
        return '<Split: expense: %s user: %s share: %s%%>' % (self.expenditure,
                                                              self.user,
                                                              self.share)

class Subitem(object):
    def __repr__(self):
        return '<Subitem: expense: %s user: %s cost: %s>' % (self.expense,
                                                             self.user,
                                                             self.amount)

class Transfer(object):
    def __repr__(self):
        return '<Transfer: from %s to %s for %s>' % (self.debtor,
                                                     self.creditor,
                                                     self.amount)

### DB/Class Mapping ###

orm.mapper(User, users)

orm.mapper(Expenditure, expenditures, properties={
        'spender': orm.relation(User, backref='expenditures')
})

orm.mapper(Split, splits, properties={
        'expenditure': orm.relation(Expenditure, backref='splits'),
        'user': orm.relation(User)
})

orm.mapper(Subitem, subitems, properties={
        'expenditure': orm.relation(Expenditure, backref='subitems'),
        'user': orm.relation(User)
})

orm.mapper(Transfer, transfers, properties={
        'debtor': orm.relation(User),
        'creditor': orm.relation(User)
})

__all__ = [users, expenditures, splits, subitems, transfers,
           User, Expenditure, Split, Subitem, Transfer,
           meta]
