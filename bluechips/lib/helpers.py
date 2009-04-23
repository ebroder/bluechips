"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from routes import url_for, redirect_to
from webhelpers.html import escape, literal, url_escape, HTML
from webhelpers.html.tags import *

from webhelpers.pylonslib import Flash as _Flash

from decimal import Decimal

def bluechips():
    return '<span class="bluechips">BlueChips</span>'

def popupLink(text, url, *args, **kwargs):
    kwargs['onclick'] = 'return popupLink(%s)' % url
    return HTML.a(text, href=url, *args, **kwargs)

flash = _Flash()
