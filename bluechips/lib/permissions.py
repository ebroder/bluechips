"""
authkit authorization permission objects for BlueChips
"""

from authkit.authenticate import AddDictToEnviron
from authkit.authorize import NotAuthorizedError
from authkit.permissions import RequestPermission

from sqlalchemy.exceptions import InvalidRequestError

from bluechips import model
from bluechips.model import meta

class BlueChipUser(RequestPermission):
    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        try:
            user = meta.Session.query(model.User).\
                filter_by(username=environ['REMOTE_USER']).\
                one()
        except InvalidRequestError:
            raise NotAuthorizedError('You are not allowed access.')
        return app(environ, start_response)

class DummyAuthenticate(AddDictToEnviron):
    """
    Set the authkit.authenticate environment variable so
    authkit.authorize shuts up
    """
    def __init__(self, app):
        super(DummyAuthenticate, self).__init__(app, {
                'authkit.authenticate': True})

__all__ = ['BlueChipUser', 'DummyAuthenticate']
