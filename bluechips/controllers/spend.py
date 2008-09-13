"""
Handle expenditures
"""

import logging

from bluechips.lib.base import *
from bluechips.widgets import spend

from pylons import request
from pylons.decorators.rest import dispatch_on

from decimal import Decimal, InvalidOperation

log = logging.getLogger(__name__)

class SpendController(BaseController):
    def index(self):
        return h.redirect_to(h.url_for(action='simple'))
    
    @dispatch_on(GET='_simple_get',
                 POST='_simple_post')
    def simple(self, id=None):
        abort(500)
    
    def _simple_get(self, id=None):
        c.title = "Add a Simple Expenditure"
        
        c.expenditure = {}
        if id is not None:
            e = meta.Session.query(model.Expenditure).get(id)
            if len(e.credits) > 1:
                return h.redirect_to(h.url_for(action='complex'))
            for field in e.c:
                c.expenditure[field.name] = getattr(e, field.name)
            c.expenditure['amount'] = e.credits[0].amount
            c.expenditure['spender'] = e.credits[0].account
        
        return render('/spend/simple.mako')
    
    def _simple_post(self, id=None):
        if not valid(self, spend.simple_spend_form):
            return self._simple_get(id)
        
        if id is None:
            e = model.Expenditure(description=self.form_result['description'],
                                  date=self.form_result['date'])
            c = model.Credit(expenditure=e,
                             account=self.form_result['account'],
                             amount=self.form_result['amount'])
            
            e.even_split()
        else:
            e = meta.Session.query(model.Expenditure).get(id)
            e.description = self.form_result['description']
            e.date = self.form_result['date']
            
            if len(e.credits) == 1:
                c = e.credits[0]
            else:
                c = model.Credit()
                e.credits = [c]
            
            c.expenditure = e
            c.account = self.form_result['account']
            c.amount = self.form_result['amount']
            
            e.update_split()
        
        meta.Session.add_all([e, c])
        meta.Session.commit()
        
        return h.redirect_to(h.url_for(controller='status',
                                       action=None,
                                       id=None))
