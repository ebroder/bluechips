from bluechips.tests import *

class TestStatusController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='status',
                                        action='index'))
        # Test response...
