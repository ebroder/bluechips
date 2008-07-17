"""
Fake a REMOTE_USER value so that you can do things from the shell and
run tests.
"""

class FakeAuth(object):
    
    def __init__(self, application, global_conf, username='root'):
        self.application = application
        self.username = username
    
    def __call__(self, environ, start_response):
        environ['REMOTE_USER'] = 'root'
        return self.application(environ, start_response)
