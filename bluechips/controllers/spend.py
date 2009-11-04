"""
Handle expenditures
"""

import logging

from decimal import Decimal, InvalidOperation

from bluechips.lib.base import *

from pylons import request
from pylons.decorators.rest import dispatch_on
from pylons.decorators import validate

from formencode import validators, Schema
from formencode.foreach import ForEach
from formencode.variabledecode import NestedVariables

log = logging.getLogger(__name__)


class ShareSchema(Schema):
    "Validate individual user shares."
    allow_extra_fields = False
    user_id = validators.Int(not_empty=True)
    amount = validators.Number(not_empty=True)


class ExpenditureSchema(Schema):
    "Validate an expenditure."
    allow_extra_fields = False
    pre_validators = [NestedVariables()]
    spender_id = validators.Int(not_empty=True)
    amount = model.types.CurrencyValidator(not_empty=True)
    description = validators.UnicodeString()
    date = validators.DateConverter()
    shares = ForEach(ShareSchema)
    

class SpendController(BaseController):
    def index(self):
        return self.edit()
    
    def edit(self, id=None):
        c.users = meta.Session.query(model.User.id, model.User)
        if id is None:
            c.title = 'Add a New Expenditure'
            c.expenditure = model.Expenditure()
            c.expenditure.spender_id = request.environ['user'].id

            num_residents = meta.Session.query(model.User).\
                    filter_by(resident=True).count()
            # Pre-populate split percentages for an even split.
            c.values = {}
            for ii, user_row in enumerate(c.users):
                user_id, user = user_row
                if user.resident:
                    val = Decimal(100) / Decimal(num_residents)
                else:
                    val = 0
                c.values['shares-%d.amount' % ii] = val
        else:
            c.title = 'Edit an Expenditure'
            c.expenditure = meta.Session.query(model.Expenditure).get(id)
        return render('/spend/index.mako')

    @validate(schema=ExpenditureSchema(), form='edit', variable_decode=True)
    def update(self, id=None):
        # Either create a new object, or, if we're editing, get the
        # old one
        if id is None:
            e = model.Expenditure()
            meta.Session.add(e)
        else:
            e = meta.Session.query(model.Expenditure).get(id)
        
        # Set the fields that were submitted
        shares = self.form_result.pop('shares')
        update_sar(e, self.form_result)
        if e.id is not None:
            e.update_split()

        users = dict(meta.Session.query(model.User.id, model.User).all())
        split_dict = {}
        for share_params in shares:
            user = users[share_params['user_id']]
            split_dict[user] = Decimal(share_params['amount'])
        e.split(split_dict)
        
        meta.Session.commit()
        
        h.flash('Expenditure updated.')
       
        return h.redirect_to('/')
