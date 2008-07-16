"""
Handle transfers
"""

import logging

from bluechips.lib.base import *
from bluechips.widgets import transfer

from pylons import request

log = logging.getLogger(__name__)

class TransferController(BaseController):
    def index(self):
        c.transfer = dict()
        c.transfer['debtor'] = request.environ['user']
        
        return render('/transfer/index.mako')
    
    @validate(form=transfer.new_transfer_form, error_handler='index')
    def new(self):
        t = model.Transfer()
        update_sar(t, self.form_result)
        meta.Session.save(t)
        
        h.flash('Transfer recorded.')
        
        return h.redirect_to('/')
