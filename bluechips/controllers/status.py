"""
Calculate the current state of the books
"""

import logging

from bluechips.lib.base import *
from bluechips.lib.totals import *

log = logging.getLogger(__name__)

class StatusController(BaseController):
    def index(self):
        c.debts = debts()
        c.settle = settle(c.debts)
        
        return render('/status/index.mako')
