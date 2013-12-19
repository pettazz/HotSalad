"""unit test for the basic_test_info plugin"""

import os
import sys
import traceback
import unittest

from mock.mock_objects import *
from test_framework.plugins import basic_test_info


class BasicTestInfoTest(unittest.TestCase):
    """
    This test uses the mock objects above to
    create a fake basic_test_info file and check
    that it is exists in the directory it belongs.
    """
    def test_addError(self):
        mock = MockTestSuite()
        plugins = basic_test_info.BasicTestInfo()
        plugins.options = MockOptions
        Options = MockOptions()
        plugins.test_logpath = "unittest_logs/test"
        plugins.log_path = "unittest_logs"
        os.makedirs("unittest_logs/test")
        mock_file_name = 'basic_test_info.log'
        ex = type = details = traceb = None
        try:
            raise Exception("This is an Error!")
        except Exception as ex:
            type, details, traceb = sys.exc_info()
            plugins.addError(mock.test, sys.exc_info())
        self.assertTrue(ex, "Intentional exception was not raised!")

        file_list = os.listdir("unittest_logs/test")
        self.assertTrue(
            mock_file_name in file_list, "Expected file (%s) not present!" % mock_file_name)
        file_info = open("unittest_logs/test/" + mock_file_name, "r")
        contents = file_info.read()
        self.assertTrue(MockDriver.current_url in contents,
                        "current_url %s missing" % MockDriver.current_url)
        self.assertTrue(Options.browser in contents,
                        "browser (%s) missing!" % Options.browser)
        self.assertTrue(Options.servername in contents,
                        "servername (%s) missing!" % Options.servername)
        self.assertTrue(str(type) in contents,
                        "exception type missing!")
        self.assertTrue(str(details) in contents,
                        "exception details missing!")
        self.assertTrue(traceback.format_exc(traceb) in contents,
                        "exception traceback missing!")
        file_info.close()

    def tearDown(self):
        os.remove("unittest_logs/test/basic_test_info.log")
        os.removedirs("unittest_logs/test")

if __name__ == '__main__':
    unittest.main()
