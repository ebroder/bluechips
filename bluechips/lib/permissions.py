"""
authkit authorization permission objects for BlueChips
"""

from authkit.authenticate import AddDictToEnviron
from authkit.authorize import NotAuthenticatedError, NotAuthorizedError
from authkit.permissions import RequestPermission

from bluechips import model
from bluechips.model import meta

class BlueChipUser(RequestPermission):
    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated') # pragma: nocover
        environ['user'] = meta.Session.query(model.User).\
            filter_by(username=unicode(environ['REMOTE_USER'])).\
            first()
        if environ['user'] == None:
            raise NotAuthorizedError('You are not allowed access.') # pragma: nocover
        return app(environ, start_response)

class BlueChipResident(RequestPermission):
    def check(self, app, environ, start_response):
        if 'user' not in environ:
            raise NotAuthenticatedError('Not Authenticated')

        if not getattr(environ['user'], 'resident', False):
            raise NotAuthorizedError('You are not allowed access.')

        return app(environ, start_response)

class DummyAuthenticate(AddDictToEnviron):
    """
    Set the authkit.authenticate environment variable so
    authkit.authorize shuts up
    """
    def __init__(self, app, app_conf):
        newenv = {}
        newenv['authkit.authenticate'] = True
        newenv['authkit.config'] = {'setup.enable': True}
        if 'fake_username' in app_conf:
            newenv['REMOTE_USER'] = app_conf['fake_username']
        super(DummyAuthenticate, self).__init__(app, newenv)


def authenticate(environ, username, password):
    user = meta.Session.query(model.User).\
            filter_by(username=unicode(username),
                      password=unicode(password)).first()
    return (user is not None)

__all__ = ['BlueChipUser', 'DummyAuthenticate', 'authenticate']
