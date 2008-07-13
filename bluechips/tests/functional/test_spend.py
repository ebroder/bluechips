from bluechips.tests import *

class TestSpendController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='spend'))
        # Test response...
