"""
Display old transactions
"""

import logging

from bluechips.lib.base import *
from bluechips.lib.totals import *

import sqlalchemy
from sqlalchemy import orm

log = logging.getLogger(__name__)

class HistoryController(BaseController):
    def index(self):
        c.title = 'History'
        
        c.expenditures = meta.Session.query(model.Expenditure).\
                options(orm.eagerload('splits')).all()
        c.transfers = meta.Session.query(model.Transfer).all()

        return render('/history/index.mako')
