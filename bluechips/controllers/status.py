"""
Calculate the current state of the books
"""

import logging

from bluechips.lib.base import *
from bluechips.lib.totals import *

import sqlalchemy

from datetime import date, timedelta

from bluechips.model.types import Currency

from pylons import request

log = logging.getLogger(__name__)

class StatusController(BaseController):
    def index(self):
        c.debts = debts()
        c.settle = settle(c.debts)
        
        c.total = self._total()
        
        year = date.today() - timedelta(days=365)
        this_year = date.today().replace(month=1, day=1)
        this_month = date.today().replace(day=1)
        last_month = (date.today() - timedelta(days=30)).replace(day=1)
        
        c.year_total, c.this_year_total, c.this_month_total = \
            [self._total(model.Expenditure.date >= i)
             for i in [year, this_year, this_month]]
        

        c.last_month_total = self._total(sqlalchemy.and_(
                    model.Expenditure.date >= last_month,
                    model.Expenditure.date < this_month))
        
        c.expenditures = meta.Session.query(model.Expenditure).\
            filter(model.Expenditure.spender==request.environ['user']).\
            limit(10).all()
        c.transfers = meta.Session.query(model.Transfer).\
            filter(sqlalchemy.or_(
                model.Transfer.debtor==request.environ['user'],
                model.Transfer.creditor==request.environ['user'])).\
                limit(10).all()
        
        return render('/status/index.mako')
    
    def _total(self, conditions=None):
        q = meta.Session.query(sqlalchemy.func.SUM(
            model.Expenditure.amount))
        if conditions is not None:
            q = q.filter(conditions)
        return q.scalar()
