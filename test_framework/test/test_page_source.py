""" unit test for the page source plugin"""

import os
import unittest

from mock.mock_objects import MockTestSuite
from mock.mock_objects import MockOptions
from test_framework.plugins import page_source
        
class PageSourceTest(unittest.TestCase):
    """
    This test creates uses the mock object info above
    to create an html file, add page source info, 
    and confirm that the file exists and is properly populated.
    """
   
    def test_addError(self):
            
        mock = MockTestSuite()
        plugins = page_source.PageSource()
        plugins.options = MockOptions()
        plugins.test_logpath = "unittest_logs/test"
        plugins.log_path = "unittest_logs"
        os.makedirs("unittest_logs/test")
        mock_file_name = 'page_source.html'
        plugins.addError(mock.test, None)
        file_list = os.listdir("unittest_logs/test")
        found = False
        if mock_file_name in file_list:
            found = True
        self.assertTrue(found, "expected file not present")
        file_info = open("unittest_logs/test/" + mock_file_name, "r")
        contents = file_info.read()
        equals = False
        expected = "source code"
        if contents == expected:
            equals = True
        file_info.close()
        self.assertTrue(equals, "found file doesn't match")
        

    def tearDown(self):
        os.remove("unittest_logs/test/page_source.html")
        os.removedirs("unittest_logs/test")
        
        
if __name__ == '__main__':
    unittest.main()
        
       
