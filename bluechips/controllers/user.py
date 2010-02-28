"""
Calculate the current state of the books
"""

import logging

from bluechips.lib.base import *
from bluechips.lib.permissions import BlueChipResident

import sqlalchemy
from sqlalchemy import orm

from authkit.authorize.pylons_adaptors import authorize

from pylons import request
from pylons.decorators import validate
from pylons.decorators.secure import authenticate_form

from formencode import validators, Schema, FancyValidator, Invalid

log = logging.getLogger(__name__)


class EmailSchema(Schema):
    "Validate email updates."
    allow_extra_fields = False
    new_email = validators.Email()


class UniqueUsername(FancyValidator):
    def _to_python(self, value, state):
        u = meta.Session.query(model.User).\
            filter(model.User.username == value).\
            first()
        if u:
            raise Invalid(
                'That username already exists',
                value, state)
        return value


class NewUserSchema(Schema):
    "Validate new users."
    allow_extra_fields = False
    username = UniqueUsername(not_empty=True)
    password = validators.String(if_missing=None)
    confirm_password = validators.String(if_missing=None)
    name = validators.String(not_empty=False)
    resident = validators.StringBoolean(not_empty=True)
    chained_validators = [
        validators.FieldsMatch('password', 'confirm_password'),
        ]


class UserController(BaseController):
    def index(self):
        c.title = 'User Settings'
        return render('/user/index.mako')

    def email(self):
        c.title = 'User Settings'
        return render('/user/email.mako')

    @authenticate_form
    @validate(schema=EmailSchema(), form='index')
    def update(self):
        new_email = self.form_result['new_email']
        request.environ['user'].email = new_email
        meta.Session.commit()
        if new_email is None:
            h.flash("Removed email address.")
        else:
            h.flash("Updated email address to '%s'." % new_email)
        return h.redirect_to('/')

    @authorize(BlueChipResident())
    def new(self):
        c.title = 'Register a New User'
        return render('/user/new.mako')

    @authenticate_form
    @authorize(BlueChipResident())
    @validate(schema=NewUserSchema(), form='new')
    def create(self):
        u = model.User(username=self.form_result['username'],
                       resident=self.form_result['resident'])

        if self.form_result['name']:
            u.name = self.form_result['name']
        else:
            u.name = self.form_result['username']

        if self.form_result['password'] is not None:
            u.password = self.form_result['password']

        meta.Session.add(u)
        meta.Session.commit()

        h.flash('Successfully created new user %s' % u.username)
        return h.redirect_to('/')
