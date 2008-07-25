"""
Display old transactions
"""

import logging

from bluechips.lib.base import *
from bluechips.lib.totals import *

import sqlalchemy

log = logging.getLogger(__name__)

class HistoryController(BaseController):
    def index(self):
        c.title = 'History'
        
        c.expenditures = meta.Session.query(model.Expenditure).all()
        c.transfers = meta.Session.query(model.Transfer).all()
        
        return render('/history/index.mako')
