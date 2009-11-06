import cgi

from pylons import request, tmpl_context as c

from bluechips.lib.base import BaseController, render

class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.
    
    """
    def document(self):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')
        c.code = cgi.escape(request.GET.get('code', resp.status))
        return render('/error.mako')
