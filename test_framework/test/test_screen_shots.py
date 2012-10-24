"""unit test for the screen shots plugin"""

import os
import unittest

from mock.mock_objects import MockTestSuite
from mock.mock_objects import MockOptions
from test_framework.plugins import screen_shots

        
class ScreenShotsTest(unittest.TestCase):
    """
    This test uses the mock object info above to
    create a fake screenshot file and check
    that it is exists in the directory it belongs.
    """        
    def test_addError(self):
        
        mock = MockTestSuite()
        plugins = screen_shots.ScreenShots()
        plugins.options = MockOptions()
        plugins.test_logpath = "unittest_logs/test"
        plugins.log_path = "unittest_logs"
        os.makedirs("unittest_logs/test")
        mock_file_name = "screenshot.jpg"
        plugins.addError(mock.test, None)
        file_list = os.listdir("unittest_logs/test/")
        found = False
        if mock_file_name in file_list:
            found = True
        self.assertTrue(found, "file not present")
        
    def tearDown(self):
        os.remove("unittest_logs/test/screenshot.jpg")
        os.removedirs("unittest_logs/test")
        
        
if __name__ == '__main__':
    unittest.main()
        
       
