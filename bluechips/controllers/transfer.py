"""
Handle transfers
"""

import logging

from datetime import date

from bluechips.lib.base import *

from pylons import request
from pylons.decorators import validate

from formencode import Schema, validators

log = logging.getLogger(__name__)


class TransferSchema(Schema):
    "Validate a transfer."
    allow_extra_fields = False
    debtor_id = validators.Int(not_empty=True)
    creditor_id = validators.Int(not_empty=True)
    amount = validators.Number(not_empty=True)
    description = validators.UnicodeString()
    date = validators.String()
 

class TransferController(BaseController):
    def index(self):
       return self.edit()
    
    def edit(self, id=None):
        c.users = meta.Session.query(model.User.id, model.User.name)
        if id is None:
            c.title = 'Add a New Transfer'
            c.transfer = model.Transfer()
            c.transfer.debtor_id = request.environ['user'].id
            c.transfer.date = date.today()
        else:
            c.title = 'Edit a Transfer'
            c.transfer = meta.Session.query(model.Transfer).get(id)
        return render('/transfer/index.mako')
    
    @validate(schema=TransferSchema(), form='edit')
    def update(self, id=None):
        if id is None:
            t = model.Transfer()
            meta.Session.add(t)
        else:
            t = meta.Session.query(model.Transfer).get(id)
        
        t.amount = self.form_result.pop('amount') * 100
        update_sar(t, self.form_result)
        meta.Session.commit()
        
        h.flash('Transfer updated.')
        
        return h.redirect_to('/')
