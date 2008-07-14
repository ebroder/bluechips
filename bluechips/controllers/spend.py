"""
Handle expenditures
"""

import logging

from bluechips.lib.base import *
from bluechips.widgets import spend
from bluechips.lib.split import *

log = logging.getLogger(__name__)

class SpendController(BaseController):
    def index(self):
        return render('/spend/index.mako')
    
    @validate(form=spend.new_spend_form, error_handler='index')
    def new(self):
        e = model.Expenditure()
        update_sar(e, self.form_result)
        meta.Session.save(e)
        
        even_split(e)
        meta.Session.commit()
        
        c.expenditure = e
        
        return render('/spend/new.mako')
