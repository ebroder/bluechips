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
        c.title = 'Add a New Expenditure'
        
        c.expenditure = dict()
        c.expenditure['spender'] = request.environ['user']
        
        return render('/spend/index.mako')
    
    def edit(self, id):
        c.title = 'Edit an Expenditure'
        
        c.expenditure = meta.Session.query(model.Expenditure).get(id)
        
        return render('/spend/index.mako')
    
    def update(self, id=None):
        # Validate the submission
        if not valid(self, spend.new_spend_form):
            if id is None:
                return self.index()
            else:
                return self.edit(id)
        
        # Either create a new object, or, if we're editing, get the
        # old one
        if id is None:
            e = model.Expenditure()
            meta.Session.add(e)
        else:
            e = meta.Session.query(model.Expenditure).get(id)
        
        # Set the fields that were submitted
        update_sar(e, self.form_result)
        
        if id is None:
            e.even_split()
        else:
            e.update_split()
        
        meta.Session.commit()
        
        h.flash('Expenditure recorded.')
        h.flash("""Want to do something unusual?

<ul id="expenditure_options">
  <li>%s</li>
  <li>%s</li>
</ul>""" % (h.link_to('Change the split', h.url_for(controller='spend',
                                                   action='split',
                                                   id=e.id)),
           h.link_to('Spin off a subitem', h.url_for(controller='spend',
                                                     action='subitem',
                                                     id=e.id))))
        
        return h.redirect_to('/')
    
    @dispatch_on(POST='_post_split',
                 GET='_get_split')
    def split(self, id):
        abort(500)
    
    def _get_split(self, id):
        c.title = 'Change Expenditure Split'
        
        c.expenditure = meta.Session.query(model.Expenditure).get(id)
        c.users = meta.Session.query(model.User)
        
        return render('/spend/split.mako')
    
    def _post_split(self, id):
        c.values = request.params
        c.errors = dict()
        
        split_dict = dict()
        
        for username, percent in c.values.iteritems():
            try:
                user = meta.Session.query(model.User).\
                    filter(model.User.username==username).one()
                split_dict[user] = Decimal(percent)
            except InvalidOperation:
                c.errors[username] = 'Please enter a number'
        if c.errors != dict():
            return self._get_split(id)
        
        e = meta.Session.query(model.Expenditure).get(id)
        e.split(split_dict)
        
        meta.Session.commit()
        
        h.flash('Expenditure redivided')
        
        return h.redirect_to('/')
