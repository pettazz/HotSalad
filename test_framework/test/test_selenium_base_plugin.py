# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest

import mock.mock_driver as mock_driver
from mock.mock_objects import MockOptions
from mock.mock_objects import MockTestSuite
from test_framework.plugins import selenium_plugin


class BasePluginTestCase(unittest.TestCase):
    def test_before_test(self):
        selenium_plugin.webdriver = mock_driver
        plugin = selenium_plugin.SeleniumBase()
        plugin.options = MockOptions()
        plugin.options.browser = "firefox"
        test = MockTestSuite()
        plugin.beforeTest(test)
        self.assertEquals(plugin.driver.browser, "firefox")
    
    def test_after_test(self):
        test = MockTestSuite()
        test.test.driver = mock_driver.Firefox()
        selenium_plugin.webdriver = mock_driver
        plugin = selenium_plugin.SeleniumBase()
        plugin.driver = test.test.driver
        self.assertEquals(plugin.afterTest(test), None)




if __name__ == '__main__':
    unittest.main()
