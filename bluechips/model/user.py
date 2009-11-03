class User(object):
    def __init__(self, username, name=u"", resident=True):
        self.username = username
        self.name = name
        self.resident = resident
    
    def __repr__(self):
        return '<User: %s>' % (self.username)

    def __str__(self):
        return self.name

__all__ = ['User']
