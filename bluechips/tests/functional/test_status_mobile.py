from bluechips.tests import *

class TestMobileController(TestController):
    def setUp(self):
        self.ua = ('Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) '
                   'AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 '
                   'Mobile/1A543a Safari/419.3')
        self.app.extra_environ['HTTP_USER_AGENT'] = self.ua

    def test_switch_interfaces(self):
        response = self.app.get('/')
        response.mustcontain('apple-touch-icon')
        response.mustcontain('Use non mobile interface')
        response = response.click('Use non mobile interface')
        response.mustcontain('Use mobile interface')
        response = response.click('Use mobile interface')

    def test_view_nonmobile(self):
        self.app.get(url_for(controller='history',
                             action='index'))
