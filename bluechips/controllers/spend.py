"""
Handle expenditures
"""

import logging

from bluechips.lib.base import *
from bluechips.widgets import spend

from pylons import request

log = logging.getLogger(__name__)

class SpendController(BaseController):
    def index(self):
        c.expenditure = dict()
        c.expenditure['spender'] = request.environ['user']
        
        return render('/spend/index.mako')
    
    @validate(form=spend.new_spend_form, error_handler='index')
    def new(self):
        e = model.Expenditure()
        update_sar(e, self.form_result)
        meta.Session.save(e)
        
        e.even_split()
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
