from bluechips.tests import *

class TestHistoryController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='history',
                                        action='index'))
        # Test response...
