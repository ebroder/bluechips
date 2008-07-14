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
    
    @validate(form=spend.new_spend_form, error_handler='index')
    def new(self):
        return str(self.form_result)
