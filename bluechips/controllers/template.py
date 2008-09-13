"""
Render templates that are mostly static
"""

import logging

from bluechips.lib.base import *

from mako.exceptions import TopLevelLookupException
from pylons.controllers.util import abort

log = logging.getLogger(__name__)

class TemplateController(BaseController):
    def index(self, url=''):
        try:
            return render('/%s.mako' % url)
        except TopLevelLookupException:
            abort(404)
