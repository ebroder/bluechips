from bluechips.tests import *

class TestTransferController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='transfer'))
        # Test response...
