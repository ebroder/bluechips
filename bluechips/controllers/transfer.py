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
        c.title = 'Add a New Transfer'
        
        c.transfer = dict()
        c.transfer['debtor'] = request.environ['user']
        
        return render('/transfer/index.mako')
    
    def edit(self, id):
        c.title = 'Edit a Transfer'
        
        c.transfer = meta.Session.query(model.Transfer).get(id)
        
        return render('/transfer/index.mako')
    
    @validate(form=transfer.new_transfer_form, error_handler='index')
    def update(self, id=None):
        # Validate the submission
        if not valid(self, transfer.new_transfer_form):
            if id is None:
                return self.index()
            else:
                return self.edit(id)
        
        if id is None:
            t = model.Transfer()
        else:
            t = meta.Session.query(model.Transfer).get(id)
        
        update_sar(t, self.form_result)
        meta.Session.save_or_update(t)
        meta.Session.commit()
        
        h.flash('Transfer recorded.')
        
        return h.redirect_to('/')
