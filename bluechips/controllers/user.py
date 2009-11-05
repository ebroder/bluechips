"""
Calculate the current state of the books
"""

import logging

from bluechips.lib.base import *

import sqlalchemy
from sqlalchemy import orm

from pylons import request
from pylons.decorators import validate

from formencode import validators, Schema

log = logging.getLogger(__name__)


class EmailSchema(Schema):
    "Validate email updates."
    allow_extra_fields = False
    new_email = validators.Email()


class UserController(BaseController):
    def index(self):
        return render('/user/index.mako')

    @validate(schema=EmailSchema(), form='index')
    def update(self):
        new_email = self.form_result['new_email']
        if new_email == '':
            new_email = None
        request.environ['user'].email = new_email
        meta.Session.commit()
        if new_email is None:
            h.flash("Removed email address.")
        else:
            h.flash("Updated email address to '%s'." % new_email)
        return h.redirect_to('/')
