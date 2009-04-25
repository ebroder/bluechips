"""
authkit authorization permission objects for BlueChips
"""

from authkit.authenticate import AddDictToEnviron
from authkit.authorize import NotAuthenticatedError, NotAuthorizedError
from authkit.permissions import RequestPermission

from sqlalchemy.exceptions import InvalidRequestError

from bluechips import model
from bluechips.model import meta

class BlueChipUser(RequestPermission):
    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        try:
            environ['user'] = meta.Session.query(model.User).\
                filter_by(username=unicode(environ['REMOTE_USER'])).\
                one()
        except InvalidRequestError:
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

__all__ = ['BlueChipUser', 'DummyAuthenticate']
