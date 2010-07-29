"""
Calculate the current state of the books
"""

import logging

from bluechips.lib.base import *
from bluechips.lib.totals import *

import sqlalchemy
from sqlalchemy import orm

from datetime import date, timedelta

from bluechips.model.types import Currency

from pylons import request

log = logging.getLogger(__name__)

class StatusController(BaseController):
    def index(self):
        c.debts = debts()
        c.settle = settle(c.debts)

        c.net = 0
        for from_user, to_user, amount in c.settle:
            if from_user == request.environ['user']:
                c.net -= amount
            elif to_user == request.environ['user']:
                c.net += amount
        
        periods = {}
        periods['Total'] = (None, None)
        periods['Past year'] = (date.today() - timedelta(days=365), None)
        periods['Year to date'] = (date.today().replace(month=1, day=1), None)
        periods['Month to date'] = (date.today().replace(day=1), None)
        periods['Last month'] = ((date.today() -
                                  timedelta(days=30)).replace(day=1),
                                 periods['Month to date'][0])
        
        c.totals = {}
        for period in periods.keys():
            c.totals[period] = {}
            start, end = periods[period]
            conds = []
            if start is not None:
                conds.append(model.Expenditure.date >= start)
            if end is not None:
                conds.append(model.Expenditure.date < end)
            if len(conds) > 1:
                conds = sqlalchemy.and_(*conds)
            elif len(conds) > 0:
                conds = conds[0]
            else:
                conds = None

            for scope in ('all', 'mine'):
                meth = getattr(self, '_total_%s' % scope)
                c.totals[period][scope] = meth(conds)

        c.expenditures = meta.Session.query(model.Expenditure).\
                filter(sqlalchemy.or_(
                    model.Expenditure.spender == request.environ['user'],
                    model.Expenditure.splits.any(
                        sqlalchemy.and_(
                            model.Split.user == request.environ['user'],
                            model.Split.share != 0)))).\
                options(orm.eagerload('splits')).\
                limit(10).all()
        c.transfers = meta.Session.query(model.Transfer).\
            filter(sqlalchemy.or_(
                model.Transfer.debtor==request.environ['user'],
                model.Transfer.creditor==request.environ['user'])).\
                limit(10).all()
        c.users = get_users()
        
        return render('/status/index.mako')
    
    def _total_all(self, conditions=None):
        q = meta.Session.query(sqlalchemy.func.SUM(
            model.Expenditure.amount))
        if conditions is not None:
            q = q.filter(conditions)
        return q.scalar()

    def _total_mine(self, conditions=None):
        q = meta.Session.query(sqlalchemy.func.SUM(
            model.Split.share)).join(model.Split.expenditure).\
                filter(model.Split.user == request.environ['user'])
        if conditions is not None:
            q = q.filter(conditions)
        return q.scalar()
