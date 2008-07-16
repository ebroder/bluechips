"""
Calculate the current state of the books
"""

import logging

from bluechips.lib.base import *

log = logging.getLogger(__name__)

class StatusController(BaseController):
    def index(self):
        return 'Hello World'
