class User(object):
    def __init__(self, username, name=u"", resident=True):
        self.username = username
        self.name = name
        self.resident = resident
    
    def __repr__(self):
        return '<User: %s>' % (self.username)

__all__ = ['User']
