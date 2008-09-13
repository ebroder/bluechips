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
        
        c.total = self._total(sqlalchemy.text('1=1'))
        
        year = date.today() - timedelta(days=365)
        this_year = date.today().replace(month=1, day=1)
        this_month = date.today().replace(day=1)
        last_month = (date.today() - timedelta(days=30)).replace(day=1)
        
        c.year_total, c.this_year_total, c.this_month_total = \
            [self._total(model.Expenditure.date >= i)
             for i in [year, this_year, this_month]]
        

        c.last_month_total = self._total(sqlalchemy.and_(
                model.Expenditure.date>=last_month,
                model.Expenditure.date<this_month))
        
        account = request.environ['user']
        c.expenditures = meta.Session.query(model.Expenditure).join('credits').\
            reset_joinpoint().join('debits').filter(sqlalchemy.or_(
                model.Credit.account==account,
                model.Debit.account==account)).\
                group_by(model.Expenditure.id).limit(10)
        
        return render('/status/index.mako')
    
    def _total(self, where):
        return Currency(meta.Session.execute(sqlalchemy.select(
                    [
                        sqlalchemy.func.sum(model.Credit.__table__.c.amount).\
                            label('total')],
                    from_obj=[
                        model.Credit.__table__.join(model.Expenditure.__table__)]).\
                    where(where)).scalar() or 0)
