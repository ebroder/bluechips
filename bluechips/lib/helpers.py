"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from datetime import date
from decimal import Decimal

from pylons import request
from pylons.controllers.util import redirect
from routes import url_for
from webhelpers.html import escape, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.pylonslib.secure_form import *

from webhelpers.pylonslib import Flash as _Flash


def redirect_to(*args, **kwargs):
    redirect(url_for(*args, **kwargs))


def currency(name, value, *args, **kwargs):
    if 'class_' not in kwargs:
        kwargs['class_'] = ''
    kwargs['class_'] += 'currency'
    value = "%0.2f" % (int(value) / 100.)
    return text(name, value, *args, **kwargs)


def grab(obj, attr):
    if obj:
        return getattr(obj, attr)
    else:
        if attr == 'date':
            return date.today()
        elif attr in ('spender_id', 'creditor_id', 'debtor_id'):
            return request.environ['user'].id
        elif attr == 'amount':
            return 0
        else:
            return ''

flash = _Flash()
