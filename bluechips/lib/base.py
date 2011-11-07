"""The base Controller API

Provides the BaseController class for subclassing.
"""

# Monkey-patch around a webhelpers/Pylons incompatibility
try:
    import webhelpers.pylonslib.secure_form
    import webhelpers.html
    webhelpers.html.secure_form = webhelpers.pylonslib.secure_form
except ImportError:
    pass

from decorator import decorator

from pylons import request, session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.i18n import _, ungettext, N_
from pylons.templating import render_mako

from mako.exceptions import TopLevelLookupException

import bluechips.lib.helpers as h
from bluechips import model
from bluechips.model import meta


class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

def update_sar(record, form_result):
    """
    Update a SQLAlchemy record with the results of a validated form submission
    """
    for key, value in form_result.items():
        setattr(record, key, value)

def redirect_on_get(action):
    """
    Decorator for a controller action. If the action is called with a GET
    method, 302 redirect to the action specified.
    """

    @decorator
    def redirect_on_get_wrap(func, *args, **kwargs):
        if request.method == 'GET':
            controller = request.environ['pylons.routes_dict']['controller']
            return h.redirect_to(controller=controller, action=action)
        else:
            return func(*args, **kwargs)
    return redirect_on_get_wrap

def render(name, *args, **kwargs):
    if request.user_agent and any([x in request.user_agent for x in ('iPhone','webOS', 'Android')]):
        if 'use_non_mobile' in request.params:
            session['use_non_mobile'] = (request.params['use_non_mobile'] ==
                                         'yes')
        if session.get('use_non_mobile'):
            c.mobile_client = True
        else:
            try:
                return render_mako('/mobile' + name, *args, **kwargs)
            except TopLevelLookupException:
                # If a mobile template doesn't exist for this page, don't show
                # the 'use mobile interface' link.
                c.mobile_client = False
    return render_mako(name, *args, **kwargs)

def get_users():
    return meta.Session.query(model.User.id, model.User).\
        order_by(model.User.resident.desc(), model.User.username)

__all__ = ['c', 'h', 'render', 'model', 'meta', '_', 'ungettext', 'N_',
           'BaseController', 'update_sar', 'redirect_on_get', 'get_users']
