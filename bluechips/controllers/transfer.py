"""
Handle transfers
"""

import logging

from datetime import date

from bluechips.lib.base import *

from pylons import request, app_globals as g
from pylons.decorators import validate
from pylons.controllers.util import abort

from formencode import Schema, validators

from mailer import Message

log = logging.getLogger(__name__)


class TransferSchema(Schema):
    "Validate a transfer."
    allow_extra_fields = False
    debtor_id = validators.Int(not_empty=True)
    creditor_id = validators.Int(not_empty=True)
    amount = model.types.CurrencyValidator(not_empty=True)
    description = validators.UnicodeString()
    date = validators.DateConverter()
 

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
            if c.transfer is None:
                abort(404)
        return render('/transfer/index.mako')
    
    @validate(schema=TransferSchema(), form='edit')
    def update(self, id=None):
        if id is None:
            t = model.Transfer()
            meta.Session.add(t)
            op = 'created'
        else:
            t = meta.Session.query(model.Transfer).get(id)
            if t is None:
                abort(404)
            op = 'updated'
        
        update_sar(t, self.form_result)
        meta.Session.commit()
       
        show = ('Transfer of %s from %s to %s %s.' %
                (t.amount, t.debtor, t.creditor, op))
        h.flash(show)

        # Send email notification to involved users if they have an email set.
        body = render('/emails/transfer.txt', extra_vars={'transfer': t,
                                                          'op': op})
        g.handle_notification((t.debtor, t.creditor), show, body)

        return h.redirect_to('/')
