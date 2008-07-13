"""
Handle expenditures
"""

import logging

from bluechips.lib.base import *
from bluechips.widgets import spend

log = logging.getLogger(__name__)

class SpendController(BaseController):
    def index(self):
        return render('/spend/index.mako')
