from pylons import config

from bluechips.tests import *
from bluechips import model
from bluechips.model import meta

class TestUserController(TestController):

    def test_email(self):
        response = self.app.get(url_for(controller='user', action='email'))
        # Test response...
        response.mustcontain('Email Notifications', 'User Settings')
        form = response.form
        form['new_email'] = 'test@example.com'
        response = form.submit().follow()
        response.mustcontain('Updated email address')

        user = meta.Session.query(model.User).\
                filter_by(username=unicode(config['fake_username'])).one()
        assert user.email == 'test@example.com'

    def test_clear_email(self):
        response = self.app.get(url_for(controller='user', action='email'))
        form = response.form
        form['new_email'] = ''
        response = form.submit().follow()
        response.mustcontain('Removed email address')

        user = meta.Session.query(model.User).\
                filter_by(username=unicode(config['fake_username'])).one()
        assert user.email == None

    def test_xsrf_protection(self):
        self.app.post(url_for(controller='user',
                              action='update'),
                      {'new_email': 'malicious@example.com'},
                      status=403)
