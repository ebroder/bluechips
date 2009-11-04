"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from routes import url_for, redirect_to
from webhelpers.html import escape, literal, url_escape
from webhelpers.html.tags import *

from webhelpers.pylonslib import Flash as _Flash

from decimal import Decimal

def bluechips():
    return '<span class="bluechips">BlueChips</span>'

def currency(name, value, *args, **kwargs):
    if 'class_' not in kwargs:
        kwargs['class_'] = ''
    kwargs['class_'] += 'currency'
    value = "%0.2f" % (int(value) / 100.)
    return text(name, value, *args, **kwargs)

flash = _Flash()
