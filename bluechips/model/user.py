class User(object):
    def __repr__(self):
        return '<User: %s>' % (self.username)

__all__ = ['User']
